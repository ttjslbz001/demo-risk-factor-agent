# TASK_RISK_FACTOR_AGENT

## 输入契约
- `RiskProfile` from parser
- `RuleDocument[]` from rule loader
- `ReasoningEngine.run_reasoning` 可用

## 输出契约
- 模块：`src/agents/risk_factor_agent.py`
- 函数：`assess(profile: RiskProfile, product_code: str) -> AssessmentResult`
- 行为：加载规则 → 组织提示上下文 → 调用推理引擎 → 组装 `AssessmentResult`

## 实现约束
- 产品包默认 `Monthly-Comfort`
- 组装结果时保留 `issues`（如需要在 policy_analysis 标注）
- 错误分类：RuleLoadError, ReasoningError, AssemblyError

## 依赖关系
- 前置：`TASK_PROMPT_AND_REASONING`, `TASK_RULE_LOADER`, `TASK_DATA_PARSER`
- 后置：`TASK_STREAMLIT_UI`, `TASK_E2E_TESTS_AND_SAMPLES`

## 验收标准
- 最少一次成功评估完整链路；产出包含 steps 与 confidence
- 异常路径返回可读错误并不中断进程（由上层处理）
