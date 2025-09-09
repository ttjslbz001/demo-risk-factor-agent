# 保险风险因子推理Agent项目 - 最终共识文档

## 1. 项目概述

### 1.1 项目目标
构建一个demo项目，展示**AI Agent在汽车保险风险因子推理中的自主推理能力**，对比传统规则引擎与AI Agent的差异。

### 1.2 AI Agent在保险领域的应用价值
基于[AI Agent Platform指南](https://fme.safe.com/guides/ai-agent-architecture/ai-agent-platform/)，AI Agent具备以下核心能力：

**传统规则引擎方式**:
```
商务团队制定规则 → 产品经理翻译 → 程序员编码 → 硬编码规则执行
```

**AI Agent智能推理方式**:
```
规则文档 → AI Agent自主理解 → 智能推理 → 自适应决策 → 可解释结果
```

### 1.3 AI Agent核心优势
- **自主推理**: 无需人工编码，直接理解业务规则
- **上下文理解**: 综合考虑多维度风险因子的关联性
- **适应性学习**: 能够处理规则边界情况和例外场景
- **可解释性**: 提供详细的推理过程和决策依据
- **动态调整**: 规则变更时无需重新编程

## 2. 技术规范

### 2.1 技术栈
- **前端**: Streamlit (Python Web应用)
- **后端**: Strands Agents (AI Agent 框架) + Python
- **网关**: OpenAPI + Telenav provider 网关
- **AI模型**: Claude 3.5 (通过Bedrock)
- **数据格式**: JSON

### 2.2 API配置
```python
# 使用环境变量进行配置；通过 OpenAPI + Telenav provider 网关调用 Claude 3.5 (Bedrock)
import os

model = OpenAIModel(
    client_args={
        "api_key": os.environ["TELENAV_API_KEY"],
        "base_url": os.environ.get("TELENAV_BASE_URL", "https://us-ailab-api.telenav.com/v1/messages"),
    },
    model_name=os.environ.get("MODEL_NAME", "claude3.5-bedrock"),
)
```

### 2.3 规则来源与格式（Demo）
- 规则主语料：`docs/insurance_risk_factor_agent/demo_rules` 下的 Markdown 文档
- Agent 策略：Strands Agents 自动解析 Markdown 规则并进行语义推理
- 结构化规则与费率：如需结构化计算，后续再补充 JSON/表格，不作为本次 Demo 必要项

## 3. 数据结构分析

### 3.1 输入数据 (user_application.json)
基于提供的示例数据，包含以下主要结构：

#### 3.1.1 Household Level (家庭层面)
```json
{
  "household": {
    "riskAttributeValues": {
      "homeowner": "Y/N",
      "payment-plan": "MONTHLY",
      "prior-carrier": "NOT LISTED",
      "months-of-continuous-insurance": "55",
      "vehicle-count-at-initial-evaluation": "4",
      // ... 更多家庭风险因子
    }
  }
}
```

#### 3.1.2 Driver Level (驾驶员层面)
```json
{
  "drivers": [
    {
      "riskAttributeValues": {
        "date-of-birth": "1970-12-15",
        "driver-age": "55",
        "gender": "F",
        "marital-status": "M",
        "education-level": "2",
        "occupation-code": "AA4",
        "years-licensed": "3",
        "disclosed-violations": "...",
        // ... 更多驾驶员风险因子
      }
    }
  ]
}
```

#### 3.1.3 Vehicle Level (车辆层面)
```json
{
  "vehicles": [
    {
      "riskAttributeValues": {
        "model-year": "2017",
        "make": "VL",
        "model": "V6",
        "annual-miles": "13999",
        "safety-score": "201",
        "theft-indicator": "N",
        "coll-deductible": "1500",
        // ... 更多车辆风险因子
      }
    }
  ]
}
```

### 3.2 关键风险因子识别
基于数据分析，主要风险因子包括：
1. **驾驶员因子**: 年龄、性别、婚姻状况、教育水平、驾驶经验、违章记录
2. **车辆因子**: 车型年份、品牌型号、安全评分、年行驶里程、防盗指标
3. **保单因子**: 房屋所有权、付款方式、保险历史、保险连续性

## 4. 功能需求

### 4.1 AI Agent核心功能
基于AI Agent的自主推理能力，我们的系统将实现：

1. **智能数据理解**: AI Agent自主解析JSON格式的用户申请数据
2. **规则自主学习**: AI Agent读取并深度理解`demo_rules`目录下的Markdown规则文档
3. **多维度推理**: 综合分析驾驶员、车辆、保单等多个风险维度
4. **自适应决策**: 处理规则边界情况和复杂场景
5. **可解释推理**: 提供详细的推理路径和决策依据
6. **动态调整**: 根据不同保险产品包进行推理策略调整

### 4.6 用户交互（Demo）
- 输入方式：在前端提供“粘贴纯 JSON”的表单输入
- JSON 需符合示例结构（`docs/insurance_risk_factor_agent/demo_application/user_application.json`）

### 4.2 AI Agent推理工作流 ✅
基于确认的需求，AI Agent将执行**复杂的多因子关联分析**和**业务逻辑推理**：

```
用户数据输入 → AI Agent解析数据结构 → 加载业务规则知识 → 
多维度风险分析 → 因子关联性推理 → 业务逻辑验证 → 
边界情况处理 → 生成评估结果 → 详细推理步骤展示
```

### 4.3 推理复杂度要求 ✅
- **✅ 复杂的多因子关联分析**: 分析驾驶员年龄、车辆安全性、保险历史等因子的交互影响
- **✅ 包含业务逻辑推理**: 理解保险业务规则背后的逻辑和例外情况
- **✅ 超越简单规则匹配**: 不仅匹配规则，还要理解规则意图和适用场景

### 4.4 可解释性要求 ✅
- **✅ 详细的推理步骤**: 展示每个决策点的分析过程
- 显示风险因子权重计算
- 展示业务规则应用逻辑
- 说明边界情况的处理方式
- 提供决策依据和置信度

### 4.5 AI Agent自主性边界 ✅
- **✅ 完全自主推理**: AI Agent独立完成整个风险评估过程
- 自主解释复杂的业务场景
- 自主处理数据异常和边界情况
- 自主生成推理报告和建议

### 4.2 演示场景
使用提供的三个保险产品包进行演示：
- **Monthly-Economy**: 基础保险包
- **Monthly-Comfort**: 舒适保险包  
- **Monthly-Turbo**: 高级保险包

## 5. 项目结构

```
demo-risk-factor-agent/
├── docs/
│   └── insurance_risk_factor_agent/
│       ├── ALIGNMENT_insurance_risk_factor_agent.md
│       ├── CONSENSUS_insurance_risk_factor_agent.md
│       ├── demo_application/
│       │   └── user_application.json
│       └── demo_rules/
│           ├── P20_Financial_Responsibility.md
│           └── P22_Financial_Responsibility_Tier.md
├── src/
│   ├── agents/
│   │   ├── risk_factor_agent.py
│   │   └── reasoning_engine.py
│   ├── models/
│   │   ├── risk_profile.py
│   │   └── assessment_result.py
│   ├── utils/
│   │   ├── data_parser.py
│   │   └── rule_loader.py
│   └── streamlit_app.py
├── requirements.txt
└── README.md
```

## 6. 实现计划

### 6.1 阶段1: 基础设置
- [x] 创建项目结构
- [ ] 设置Strands Agents环境
- [ ] 创建演示规则文件
- [ ] 实现数据解析器

### 6.2 阶段2: 核心功能
- [ ] 实现风险因子Agent
- [ ] 构建推理引擎
- [ ] 集成Claude 3.5模型
- [ ] 实现规则解析逻辑

### 6.3 阶段3: 用户界面
- [ ] 开发Streamlit前端
- [ ] 实现数据输入界面
- [ ] 构建结果展示页面
- [ ] 添加推理过程可视化

### 6.4 阶段4: 测试与优化
- [ ] 使用示例数据测试
- [ ] 优化推理逻辑
- [ ] 完善用户体验
- [ ] 文档完善

## 7. 验收标准

### 7.1 功能验收
- ✅ 能够解析user_application.json数据
- ✅ AI Agent能够读取和理解规则文件
- ✅ 生成准确的风险评估结果
- ✅ 清晰展示推理过程和步骤
- ✅ Streamlit界面友好易用

### 7.2 技术验收
- ✅ Strands Agents集成正常
- ✅ Claude 3.5 API调用成功
- ✅ 数据处理准确无误
- ⚠️ 性能与SLO不纳入本次Demo范围

### 7.3 演示验收
- ✅ 能够演示传统vs AI Agent对比
- ✅ 推理过程清晰可理解
- ✅ 支持多个保险产品包演示
- ✅ 结果具有业务意义

## 8. 风险与假设

### 8.1 技术风险
- API连接稳定性
- 模型推理准确性
- 数据格式兼容性

### 8.2 关键假设
- 演示规则足够代表真实业务场景
- Claude 3.5能够理解保险业务逻辑
- JSON数据格式保持稳定

## 9. 成功指标

1. **功能完整性**: 所有核心功能正常工作
2. **推理准确性**: AI Agent推理结果符合业务逻辑
3. **用户体验**: 界面友好，操作流畅
4. **演示效果**: 能够清晰展示AI Agent优势
5. **代码质量**: 代码结构清晰，可维护性强

---

**文档状态**: ✅ 已确认
**创建时间**: 2025年1月
**最后更新**: 2025年1月
**批准状态**: 待开发团队确认
