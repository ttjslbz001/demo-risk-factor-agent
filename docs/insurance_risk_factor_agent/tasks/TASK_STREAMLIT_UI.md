# TASK_STREAMLIT_UI

## 输入契约
- `AssessmentResult` from Agent
- `parse_application` 接口用于本地校验

## 输出契约
- 应用：`src/streamlit_app.py`
- 功能：
  - 粘贴 JSON 输入框（示例占位）
  - 产品包：默认 `Monthly-Comfort`（隐藏或只读）
  - 结果展示：overall_risk_tier、key_factors、driver/vehicle/policy 分析
  - 推理步骤可视化（steps）与 `issues` 高亮

## 实现约束
- 宽松模式 UI：显示 issues banner，不阻断
- 清晰错误提示（鉴权/网络/解析）

## 依赖关系
- 前置：`TASK_RISK_FACTOR_AGENT`, `TASK_DATA_PARSER`
- 后置：`TASK_E2E_TESTS_AND_SAMPLES`

## 验收标准
- 本地启动可输入示例 JSON 并得到可视化结果
- 错误路径可读、不中断进程
