# TASK_E2E_TESTS_AND_SAMPLES

## 输入契约
- 示例数据：`demo_application/user_application.json` 及其变体
- UI/Agent 可运行

## 输出契约
- 新增 3-5 个 JSON 变体（缺失字段、异常值、边界年龄/里程）
- 手工或脚本化 E2E 步骤清单

## 实现约束
- 不引入重型测试框架；先以手工+轻量脚本为主
- 记录每个样例的期望 `overall_risk_tier` 与关键因子（人工设定）

## 依赖关系
- 前置：`TASK_STREAMLIT_UI`
- 后置：`TASK_DOCS_README`

## 验收标准
- 样例可在 UI 中跑通并稳定展示结果与步骤链
- 记录一次端到端演示流程
