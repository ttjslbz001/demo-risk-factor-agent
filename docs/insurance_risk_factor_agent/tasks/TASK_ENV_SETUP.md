# TASK_ENV_SETUP

## 输入契约
- 前置文档：`DESIGN_insurance_risk_factor_agent.md` 第10章（架构澄清）
- 环境依赖：
  - Python 3.10+
  - `strands-agents==1.7.1`
  - 访问 Telenav Provider：`https://us-ailab-api.telenav.com/v1/messages`
- 机密：`TELENAV_API_KEY`

## 输出契约
- `.env.example`（包含 `TELENAV_API_KEY`, `TELENAV_BASE_URL`, `MODEL_NAME`）
- `requirements.txt` 增补/确认包含 `strands-agents==1.7.1`
- 本地运行校验说明（README 片段）

## 实现约束
- 不提交真实密钥；示例置空。
- 默认 `MODEL_NAME=claude3.5-bedrock`，可被环境覆盖。
- 提供 MacOS 本地运行指令。

## 依赖关系
- 无前置任务；多数任务依赖本任务（模型网关、UI、Agent）。
- 后置任务：`TASK_MODEL_GATEWAY`, `TASK_STREAMLIT_UI` 等。

## 验收标准
- 能通过环境变量创建模型客户端（冒烟：仅初始化不请求）。
- 本地可读取 `.env` 并注入变量（示例命令）。
- 文档指令准确可用。
