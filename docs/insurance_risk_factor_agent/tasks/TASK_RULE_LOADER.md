# TASK_RULE_LOADER

## 输入契约
- 规则目录：`docs/insurance_risk_factor_agent/demo_rules`
- `DESIGN_insurance_risk_factor_agent.md` 4.3, 10.4

## 输出契约
- 模块：`src/utils/rule_loader.py`
- 类型：`RuleDocument`（id, title, sections, raw_markdown）
- 函数：`load_rules(rules_dir: str) -> List[RuleDocument]`

## 实现约束
- 切分：按一级/二级标题；项目符号保留
- 摘要：每段首句/标题作为短摘要；证据片段 ≤200 字

## 依赖关系
- 前置：`TASK_DEMO_RULES_CURATION`
- 后置：`TASK_PROMPT_AND_REASONING`, `TASK_RISK_FACTOR_AGENT`

## 验收标准
- 能返回规则文档列表，至少包含标题、分段与原文
- 异常：目录不存在/IOError 时抛出清晰错误
