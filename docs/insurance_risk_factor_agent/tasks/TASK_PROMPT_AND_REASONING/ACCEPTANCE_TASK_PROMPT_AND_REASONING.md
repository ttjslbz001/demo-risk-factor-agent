# 验收记录 - TASK_PROMPT_AND_REASONING

- 任务文档: [TASK_PROMPT_AND_REASONING.md](../TASK_PROMPT_AND_REASONING.md)
- 关联设计: [DESIGN_insurance_risk_factor_agent.md](../../DESIGN_insurance_risk_factor_agent.md)
- 需求确认: [CONSENSUS_insurance_risk_factor_agent.md](../../CONSENSUS_insurance_risk_factor_agent.md)

## 1. 验收清单（6a/5_automate）
- [ ] 执行前检查：接口契约 `run_reasoning(...) -> ReasoningOutput` 明确
- [ ] Prompt 模板：包含 `<product_code>`、`<profile_json>`、`<rule_summaries>`、严格 `<output_schema>`
- [ ] 推理输出：包含 `final_assessment`、`steps[]`、`confidence`
- [ ] 测试：
  - 使用网关 mock 或 dry-run 路径
  - 模型输出不规范时的健壮解析与兜底
- [ ] 异常处理：`ModelGatewayError`、`TimeoutError`、`PromptBuildError`
- [ ] 文档同步：模板与示例输出

## 2. 结果记录
- 关键文件：`src/agents/reasoning_engine.py`
- 验证证据：示例输入与标准输出片段

## 3. 风险与问题
- 风险：输出结构漂移、模型不稳定
- 问题与澄清需求：
  -

## 4. 签署
- 验收人：
- 日期：


