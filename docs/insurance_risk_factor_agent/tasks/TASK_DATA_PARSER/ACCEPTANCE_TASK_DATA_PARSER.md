# 验收记录 - TASK_DATA_PARSER

- 任务文档: [TASK_DATA_PARSER.md](../TASK_DATA_PARSER.md)
- 关联设计: [DESIGN_insurance_risk_factor_agent.md](../../DESIGN_insurance_risk_factor_agent.md)
- 需求确认: [CONSENSUS_insurance_risk_factor_agent.md](../../CONSENSUS_insurance_risk_factor_agent.md)

## 1. 验收清单（6a/5_automate）
- [ ] 执行前检查：输入契约 `parse_application(raw_json: str) -> RiskProfile` 明确
- [ ] 实现核心逻辑：解析 household/drivers/vehicles；缺失字段设安全默认
- [ ] 宽松模式：将结构/取值问题写入 `issues`，不中断流程
- [ ] 测试：
  - 合法示例解析成功
  - 非法 JSON 抛出 `ValueError`
  - 结构缺失收集 `issues`
- [ ] 文档同步：示例输入/输出、边界行为说明
- [ ] 验证完成：与 UI 与 Agent 集成通过

## 2. 结果记录
- 关键文件：`src/utils/data_parser.py`
- 样例与证据：
  - 输入：`docs/insurance_risk_factor_agent/demo_application/user_application.json`
  - 输出：`RiskProfile` 片段与 `issues`

## 3. 风险与问题
- 风险：真实数据差异导致解析脆弱
- 问题与澄清需求：
  -

## 4. 签署
- 验收人：
- 日期：


