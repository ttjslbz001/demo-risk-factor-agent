from typing import Any

from src.models.risk_profile import RiskProfile
from src.models.assessment_result import AssessmentResult
from src.utils.rule_loader import load_rules
from src.agents.reasoning_engine import run_reasoning
from src.gateway.model_gateway import init_model, ModelGatewayError


DEFAULT_RULES_DIR = "docs/insurance_risk_factor_agent/demo_rules"


def assess(profile: RiskProfile, product_code: str = "Monthly-Comfort") -> AssessmentResult:
    """
    Contract:
    - Input: RiskProfile, 产品包（Monthly-Economy/Comfort/Turbo）。
    - Behavior: 加载规则 -> 组织提示 -> 调用推理引擎 -> 生成 AssessmentResult。
    - Output: AssessmentResult（含可解释步骤轨迹）。
    - Errors: RuleLoadError, ReasoningError, AssemblyError.
    """
    try:
        rules = load_rules(DEFAULT_RULES_DIR)
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"RuleLoadError: {e}") from e

    try:
        try:
            model = init_model()
        except ModelGatewayError:
            model = None  # Reasoning engine will fallback
        reasoning = run_reasoning(model, profile, rules, product_code)
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"ReasoningError: {e}") from e

    try:
        result: AssessmentResult = {
            "product_code": product_code,
            "overall_risk_tier": reasoning.get("final_assessment", {}).get(
                "overall_risk_tier", "MEDIUM"
            ),
            "key_factors": reasoning.get("final_assessment", {}).get("key_factors", []),
            "driver_analysis": [],
            "vehicle_analysis": [],
            "policy_analysis": {},
            "reasoning_steps": reasoning.get("steps", []),
            "confidence": reasoning.get("confidence", 0.5),
        }
        return result
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"AssemblyError: {e}") from e
