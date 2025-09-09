# 保险风险因子推理Agent项目 - 对齐文档

## 1. 项目上下文分析

### 1.1 现有项目结构
- 项目为全新项目，当前目录为空
- 项目位置: `/Users/hlchen/CodeHub/demo-risk-factor-agent`
- Git仓库已初始化但无提交记录

### 1.2 技术栈规划
- **前端**: Streamlit (Python Web应用框架)
- **后端**: Strands Agents (AI Agent 框架) + Python
- **网关**: OpenAPI + Telenav provider 网关
- **目标**: 展示AI Agent在保险风险因子推理中的应用

### 1.3 业务域理解
**传统保险风险评估流程:**
1. 商务团队提供规则手册(Rule Manual)和费率手册(Rate Manual)
2. 产品经理和程序员将规则和表格翻译成数据库和代码
3. 运行时代码读取用户申请，应用规则产生结果

**AI时代的改进:**
- AI Agent直接阅读规则和费率表格
- 通过推理直接产生最终结果
- 减少人工翻译环节，提高效率和准确性

## 2. 原始需求分析

### 2.1 核心需求
构建一个demo项目，展示insurance risk factor推理过程，对比传统方式与AI Agent方式的差异。

### 2.2 技术要求
- 前端: Streamlit界面
- 后端: Strands Agents (Python)
- 功能: 风险因子推理演示

## 3. 需求理解确认

### 3.1 项目目标
- **主要目标**: 演示AI Agent如何直接处理保险规则和费率表
- **对比展示**: 传统流程 vs AI Agent流程
- **技术验证**: Python Agent + Streamlit的可行性

### 3.2 功能范围(初步理解)
- 用户输入保险申请信息
- AI Agent读取规则手册和费率表
- 实时推理并输出风险评估结果
- 展示推理过程和决策依据

## 4. 需求澄清结果 ✅

### 4.1 已确认的关键决策点
1. **保险类型**: ✅ **汽车保险**
   - 聚焦于汽车保险风险因子推理
   - 涉及驾驶员、车辆、保单等多维度风险评估

2. **输入数据格式**: ✅ **JSON格式用户申请数据**
   - 用户输入：`user_application.json`
   - 包含详细的风险属性值(riskAttributeValues)
   - 涵盖household、drivers、vehicles三大类别

3. **规则存储位置**: ✅ **Demo规则文件（Markdown 为主）**
   - 规则位置：`docs/insurance_risk_factor_agent/demo_rules`
   - Markdown 为主语料，AI Agent 自动解析

4. **Agent框架**: ✅ **Strands Agents（框架） + OpenAPI + Telenav provider（网关）**
   - 使用 Strands Agents 框架 (https://strandsagents.com)
   - 通过 OpenAPI + Telenav provider 网关调用 Claude 3.5 (Bedrock)
   - API端点：`https://us-ailab-api.telenav.com/v1/messages`
   - 模型：`claude3.5-bedrock`

5. **推理过程展示**: ✅ **详细展示推理步骤**
   - 需要展示AI Agent的推理过程
   - 显示每个决策步骤和依据

### 4.2 中等优先级问题
5. **演示数据**:
   - 需要准备哪些示例数据？
   - 是否需要模拟真实的保险场景？

6. **用户交互方式**:
   - 前端提供“粘贴纯 JSON”的表单输入
   - JSON 结构参考 `demo_application/user_application.json`

7. **输出展示**:
   - 结果如何可视化？
   - 是否需要展示推理步骤？

### 4.3 低优先级问题
8. **性能要求**: 响应时间期望？
9. **扩展性**: 是否考虑后续功能扩展？
10. **部署方式**: 本地运行还是需要部署到云端？

## 5. 技术实现初步方案

### 5.1 架构设计
```
Frontend (Streamlit)
    ↓
Backend API
    ↓
Python Agent Engine
    ↓
Rule/Rate Processing Module
    ↓
AI Reasoning Engine
```

### 5.2 核心组件
1. **规则解析器**: 读取并解析 demo_rules 下的 Markdown 规则
2. **费率计算器**: 处理费率表逻辑
3. **推理引擎**: AI Agent核心推理逻辑
4. **结果生成器**: 格式化输出结果
5. **Web界面**: Streamlit前端展示

## 6. 下一步行动计划（已确认关键决策点）

1. 统一文档与实现口径（框架/网关/.env/规则/交互）
2. 创建 demo_rules Markdown 规则示例
3. 实现 JSON 粘贴表单与示例数据校验
4. 集成 Strands Agents 与网关的环境变量配置
5. 生成最终共识文档并进入实现

---

**状态**: 关键决策点已确认，进入实现准备
**创建时间**: $(date)
**更新时间**: $(date)

