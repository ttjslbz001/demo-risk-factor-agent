# 验收记录 - TASK_LOGGING_AND_ERRORS

- 任务文档: [TASK_LOGGING_AND_ERRORS.md](../TASK_LOGGING_AND_ERRORS.md)
- 关联设计: [DESIGN_insurance_risk_factor_agent.md](../../DESIGN_insurance_risk_factor_agent.md)
- 需求确认: [CONSENSUS_insurance_risk_factor_agent.md](../../CONSENSUS_insurance_risk_factor_agent.md)

## 1. 验收清单（6a/5_automate）
- [ ] 统一结构日志：请求 ID、产品包、时延、错误类别、因子数量
- [ ] 错误分类：输入校验、规则加载、网关、推理、组装
- [ ] 隐私与安全：屏蔽敏感信息（API KEY、申请敏感项）
- [ ] 运行验证：成功与失败路径各 1 次
- [ ] 文档同步：日志字段、错误码/类别说明
- [ ] 验证完成：可用于 Demo 回放（脱敏）

## 2. 结果记录
- 关键实现与路径：
  - `src/utils/logging.py` 或相关模块
- 运行证据：
  -

## 3. 风险与问题
- 风险：过度日志/敏感泄露风险
- 问题与澄清需求：
  -

## 4. 签署
- 验收人：
- 日期：


