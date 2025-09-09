# TASK_DOMAIN_MODELS

## 输入契约
- `CONSENSUS_insurance_risk_factor_agent.md` 第3章数据结构
- `DESIGN_insurance_risk_factor_agent.md` 4.6 模型定义

## 输出契约
- 文件：`src/models/risk_profile.py`, `src/models/assessment_result.py`
- 类型：使用 TypedDict（或 pydantic 后续可选），字段与设计一致
- 校验：提供最小的枚举/默认值常量（产品包、风险等级）

## 实现约束
- 命名与设计文档完全一致
- 保持高可读性与注释 docstring

## 依赖关系
- 前置：`TASK_ENV_SETUP`
- 后置：`TASK_DATA_PARSER`, `TASK_PROMPT_AND_REASONING`

## 验收标准
- 通过静态检查（mypy 可选）
- 可被 `parse_application` 与 Agent 顺利导入并使用
