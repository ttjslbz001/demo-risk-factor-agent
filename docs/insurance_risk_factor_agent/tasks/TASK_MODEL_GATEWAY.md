# TASK_MODEL_GATEWAY

## 输入契约
- `DESIGN_insurance_risk_factor_agent.md` 10.2 模型网关初始化
- 环境：`TELENAV_API_KEY`, `TELENAV_BASE_URL`, `MODEL_NAME`

## 输出契约
- 一个可复用的模型客户端初始化模块（如 `src/utils/model_client.py`）
- 初始化参数：超时、重试（最多3次，指数退避）说明（实现可逐步到位）

## 实现约束
- 不打印敏感信息；错误信息脱敏
- 对 401/403/5xx 做分类处理与抛出自定义异常（占位可先定义）

## 依赖关系
- 前置：`TASK_ENV_SETUP`
- 后置：`TASK_PROMPT_AND_REASONING`

## 验收标准
- 单元冒烟：初始化客户端对象不抛异常（无真实请求）
- 失败路径：缺失 `TELENAV_API_KEY` 时能给出清晰错误
