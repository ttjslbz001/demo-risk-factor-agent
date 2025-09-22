from typing import Any

from src.models.risk_profile import RiskProfile
from src.models.assessment_result import AssessmentResult
from src.utils.rule_loader import load_rules
from src.agents.reasoning_engine import run_reasoning
from typing import TYPE_CHECKING

from src.gateway.agent_factory import init_agent, ModelGatewayError

if TYPE_CHECKING:
    # Only for type hints; avoid runtime dependency
    from strands import Agent  # type: ignore[import-not-found]
    from strands.models.openai import OpenAIModel  # type: ignore[import-not-found]


DEFAULT_RULES_DIR = "docs/insurance_risk_factor_agent/3_year_claim_free_discount"


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
    risk_factor = 'three_year_claim_free_discount'
    try:
        # Build agent directly; if strands not available, fall back
        agent = init_agent()
        
        reasoning = run_reasoning(agent, risk_factor, profile, rules, product_code)
        reasoning["risk_factor"] = risk_factor
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"ReasoningError: {e}") from e

    try:
        result = reasoning
        return result
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"AssemblyError: {e}") from e
