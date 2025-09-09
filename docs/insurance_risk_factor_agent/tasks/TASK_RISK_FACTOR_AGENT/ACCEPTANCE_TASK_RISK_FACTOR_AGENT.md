# 验收记录 - TASK_RISK_FACTOR_AGENT

- 任务文档: [TASK_RISK_FACTOR_AGENT.md](../TASK_RISK_FACTOR_AGENT.md)
- 关联设计: [DESIGN_insurance_risk_factor_agent.md](../../DESIGN_insurance_risk_factor_agent.md)
- 需求确认: [CONSENSUS_insurance_risk_factor_agent.md](../../CONSENSUS_insurance_risk_factor_agent.md)

## 1. 验收清单（6a/5_automate）
- [ ] 执行前检查：接口契约 `assess(profile, product_code) -> AssessmentResult`
- [ ] 实现核心逻辑：加载规则 → 构建提示 → 调用推理引擎 → 组装结果
- [ ] 测试：成功路径、规则缺失、推理异常的降级与提示
- [ ] 异常处理：`RuleLoadError`、`ReasoningError`、`AssemblyError`
- [ ] 文档同步：输入/输出示例，步骤轨迹展示约定
- [ ] 验证完成：产出 `AssessmentResult` 可用于 UI 渲染

## 2. 结果记录
- 关键文件：`src/agents/risk_factor_agent.py`
- 验证证据：样例调用与输出片段

## 3. 风险与问题
- 风险：规则与推理输出对齐问题
- 问题与澄清需求：
  -

## 4. 签署
- 验收人：
- 日期：


