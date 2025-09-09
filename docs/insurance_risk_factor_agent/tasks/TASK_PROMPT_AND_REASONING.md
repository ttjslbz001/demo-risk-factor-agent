# TASK_PROMPT_AND_REASONING

## 输入契约
- 模型客户端：`TASK_MODEL_GATEWAY`
- 规则：`RuleDocument[]` from `TASK_RULE_LOADER`
- 画像：`RiskProfile` from `TASK_DATA_PARSER`
- 设计：`DESIGN_insurance_risk_factor_agent.md` 10.3 模板

## 输出契约
- 模块：`src/agents/reasoning_engine.py`
- 函数：`run_reasoning(model, profile, rules, product_code) -> ReasoningOutput`
- 输出：严格遵循 JSON 模式（final_assessment/steps/confidence）

## 实现约束
- Prompt 按模板与插槽生成；产品包固定 `Monthly-Comfort`
- 健壮解析：模型非严格 JSON 时采用容错提取
- 超时/重试：遵循客户端策略；错误分类并抛出自定义异常

## 依赖关系
- 前置：`TASK_MODEL_GATEWAY`, `TASK_RULE_LOADER`, `TASK_DATA_PARSER`
- 后置：`TASK_RISK_FACTOR_AGENT`

## 验收标准
- 对给定样例可返回结构化结果与步骤链；包含置信度
- 错误路径（鉴权缺失/超时）有清晰错误消息
