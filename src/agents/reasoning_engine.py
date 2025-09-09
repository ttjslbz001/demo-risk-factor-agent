from typing import Any, Dict, List, TypedDict
import json
import re

from src.gateway.model_gateway import init_model, ModelGatewayError
from src.utils.app_logging import get_logger, log_json, start_timer, elapsed_ms

# Best-effort load of local .env so model config can be read
try:
    from dotenv import load_dotenv  # type: ignore[import-not-found]
    load_dotenv()
except Exception:
    pass

logger = get_logger("reasoning_engine")


class ReasoningStep(TypedDict):
    step: str
    rationale: str
    evidence: List[str]


class ReasoningOutput(TypedDict):
    final_assessment: Dict[str, Any]
    steps: List[ReasoningStep]
    confidence: float


def _build_prompt(profile: Any, rules: Any, product_code: str) -> str:
    output_schema = {
        "final_assessment": {
            "overall_risk_tier": "LOW|MEDIUM|HIGH",
            "key_factors": ["string"],
        },
        "steps": [{"step": "string", "rationale": "string", "evidence": ["rule-id"]}],
        "confidence": 0.0,
    }
    rule_summaries: List[str] = []
    for doc in rules:
        for s in doc.get("sections", [])[:2]:
            title = s.get("title", "")
            summary = s.get("summary", "")
            if title or summary:
                rule_summaries.append(f"[{doc['id']}] {title} - {summary}")
    prompt = (
        "系统：你是汽车保险风控专家，依据业务规则做风险因子推理并输出严格 JSON。\n"
        + f"产品包：{product_code}\n"
        + "用户画像（标准化）：\n"
        + json.dumps(profile, ensure_ascii=False)
        + "\n可用规则与条文摘要：\n"
        + "\n".join(rule_summaries[:10])
        + "\n输出：严格遵循下列 JSON Schema，不要输出多余说明。\n"
        + json.dumps(output_schema, ensure_ascii=False)
    )
    return prompt


def _fallback_reasoning(profile: Any, product_code: str) -> ReasoningOutput:
    num_drivers = len(profile.get("drivers", [])) if isinstance(profile, dict) else 0
    num_vehicles = len(profile.get("vehicles", [])) if isinstance(profile, dict) else 0
    tier = "MEDIUM"
    if num_drivers <= 1 and num_vehicles <= 1:
        tier = "LOW"
    elif num_drivers >= 3 or num_vehicles >= 3:
        tier = "HIGH"
    log_json(
        logger,
        "reasoning.fallback",
        {"drivers": num_drivers, "vehicles": num_vehicles, "tier": tier},
    )
    return {
        "final_assessment": {
            "overall_risk_tier": tier,
            "key_factors": [
                f"drivers={num_drivers}",
                f"vehicles={num_vehicles}",
                "model:fallback",
            ],
        },
        "steps": [
            {
                "step": "fallback",
                "rationale": "Model unavailable; used simple heuristic on counts.",
                "evidence": [],
            }
        ],
        "confidence": 0.2,
    }


def run_reasoning(model: Any, profile: Any, rules: Any, product_code: str) -> ReasoningOutput:
    try:
        llm = model if model is not None else init_model()
    except ModelGatewayError:
        log_json(
            logger,
            "reasoning.call.error",
            {"error": "ModelGatewayError"},
        )
        return _fallback_reasoning(profile, product_code)

    t0 = start_timer()
    log_json(
        logger,
        "reasoning.call.start",
        {"product_code": product_code, "rules": len(rules) if isinstance(rules, list) else 0},
    )

    prompt = _build_prompt(profile, rules, product_code)

    try:
        response = llm.complete(prompt)  # type: ignore[attr-defined]
        text = response.text if hasattr(response, "text") else str(response)
        try:
            data: Dict[str, Any] = json.loads(text)
        except Exception:
            # Try to extract first JSON object if the model added prose
            match = re.search(r"\{[\s\S]*\}", text)
            if not match:
                raise ValueError("No JSON found in model output")
            data = json.loads(match.group(0))

        # Normalize output
        data.setdefault("steps", [])
        data.setdefault("confidence", 0.5)
        if "final_assessment" not in data:
            data["final_assessment"] = {}
        data["final_assessment"].setdefault("overall_risk_tier", "MEDIUM")
        data["final_assessment"].setdefault("key_factors", [])

        log_json(
            logger,
            "reasoning.call.done",
            {
                "elapsed_ms": elapsed_ms(t0),
                "tier": data.get("final_assessment", {}).get("overall_risk_tier"),
                "steps": len(data.get("steps", [])),
            },
        )
        return data  # type: ignore[return-value]
    except Exception as e:  # noqa: BLE001
        log_json(
            logger,
            "reasoning.call.error",
            {"elapsed_ms": elapsed_ms(t0), "error": type(e).__name__},
        )
        return _fallback_reasoning(profile, product_code)
