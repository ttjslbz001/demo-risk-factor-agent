# TASK_DATA_PARSER

## 输入契约
- 示例：`docs/insurance_risk_factor_agent/demo_application/user_application.json`
- 模型：`src/models/risk_profile.py`

## 输出契约
- 模块：`src/utils/data_parser.py`
- 函数：`parse_application(raw_json: str) -> RiskProfile`
- 产出：`RiskProfile` + `issues`（字符串列表，含枚举化问题码可选）

## 实现约束
- 宽松模式：字段缺失采用安全默认；所有问题收集到 `issues`
- 健壮 JSON 解析；错误消息可读

## 依赖关系
- 前置：`TASK_DOMAIN_MODELS`
- 后置：`TASK_RISK_FACTOR_AGENT`, `TASK_STREAMLIT_UI`

## 验收标准
- 针对 3-5 个样例（正常/缺失/异常值）均能返回结构化 `RiskProfile` 与 `issues`
