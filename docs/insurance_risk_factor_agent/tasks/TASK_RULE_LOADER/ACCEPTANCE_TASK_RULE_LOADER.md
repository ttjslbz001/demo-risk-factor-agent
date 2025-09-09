# 验收记录 - TASK_RULE_LOADER

- 任务文档: [TASK_RULE_LOADER.md](../TASK_RULE_LOADER.md)
- 关联设计: [DESIGN_insurance_risk_factor_agent.md](../../DESIGN_insurance_risk_factor_agent.md)
- 需求确认: [CONSENSUS_insurance_risk_factor_agent.md](../../CONSENSUS_insurance_risk_factor_agent.md)

## 1. 验收清单（6a/5_automate）
- [ ] 执行前检查：输入/输出契约 `load_rules(rules_dir) -> List[RuleDocument]`
- [ ] 实现核心逻辑：读取 Markdown，切分标题段落，生成 `sections` 与摘要
- [ ] 测试：规则目录存在/不存在、IO错误、中文与英文内容
- [ ] 异常处理：`FileNotFoundError`、`IOError` 分类与提示
- [ ] 文档同步：规则结构样例、字段说明
- [ ] 验证完成：与推理引擎提示构建集成通过

## 2. 结果记录
- 关键文件：`src/utils/rule_loader.py`
- 验证证据：加载 `docs/insurance_risk_factor_agent/demo_rules/` 输出 `RuleDocument` 数量与摘要样例

## 3. 风险与问题
- 风险：规则格式不一致导致解析不稳
- 问题与澄清需求：
  -

## 4. 签署
- 验收人：
- 日期：


