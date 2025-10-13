# Multi-Agent Insurance Rating Engine

## Overview

This project implements a sophisticated multi-agent system for insurance risk assessment and premium calculation using the [Strands Agents](https://strandsagents.com/) Graph orchestration framework. The system demonstrates modern AI agent architecture with specialized agents working together through a directed graph workflow.

## Architecture

### Multi-Agent Graph System

The system follows the architecture design outlined in `docs/multi-agent_system/architecture.md` and implements the PlantUML workflow:

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│  Orchestrator   │───▶│ Product Definition   │───▶│ Risk Factor         │
│  Agent          │    │ Agent                │    │ Reasoning Agent     │
│  (Master)       │    │                      │    │                     │
└─────────────────┘    └──────────────────────┘    └─────────────────────┘
         │                                                        │
         ▼                                                        ▼
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│ Premium         │◀───│ Data Lookup          │◀───│ Risk Assessment     │
│ Calculation     │    │ Agent                │    │ Complete            │
│ Agent           │    │                      │    │                     │
└─────────────────┘    └──────────────────────┘    └─────────────────────┘
```

### Agent Responsibilities

1. **Orchestrator Agent (Master Agent)**
   - Receives and validates insurance applications
   - Manages overall workflow coordination
   - Initializes context (timestamp, product type)
   - Coordinates risk factor processing loop
   - Collects and aggregates risk factor values

2. **Product Definition Agent**
   - Defines required risk factors for products
   - Provides risk factor definitions `<risk_subject, risk_factor_name>[]`
   - Supplies assessment rules for each risk factor
   - Maintains product-specific rule configurations

3. **Risk Factor Reasoning Agent**
   - Applies assessment rules to application data
   - Coordinates with Lookup Agent for mapping values
   - Determines risk tier values
   - Validates rule application results

4. **Data Lookup Agent**
   - Provides mapping values during risk calculation
   - Maps risk tiers to specific values
   - Provides coverage values for premium calculation
   - Maintains lookup tables and mappings

5. **Premium Calculation Agent**
   - Applies premium calculation formulas
   - Processes risk factors and coverage values
   - Calculates final premium amount
   - Validates calculation results

## Implementation Details

### Core Components

#### 1. Graph Orchestration (`src/agents/multi_agent_graph.py`)

The `InsuranceRatingEngine` class implements the main orchestration using Strands Agents Graph pattern:

```python
from src.agents.multi_agent_graph import create_rating_engine

# Create the rating engine
engine = create_rating_engine("Monthly-Comfort")

# Process an application
result = engine.process_application_with_graph(application_json)
```

Key features:
- **Graph-based execution** with dependency management
- **Fallback to sequential processing** when Strands is unavailable
- **Comprehensive error handling** and validation
- **Execution history tracking** for analysis

#### 2. Individual Agent Implementations

Each agent is implemented as a specialized class:

- `OrchestratorAgent` - Workflow coordination
- `ProductDefinitionAgent` - Product and rule management
- `DataLookupAgent` - Lookup tables and mappings
- `PremiumCalculationAgent` - Premium calculations

#### 3. Strands Agents Integration

The system leverages Strands Agents features:

- **GraphBuilder** for creating directed graphs
- **Agent instances** with specialized system prompts
- **Conditional edges** for dynamic workflow control
- **Multi-modal input support** for complex data types

### Data Models

The system uses TypedDict models for type safety:

```python
# Risk Profile
class RiskProfile(TypedDict):
    household: Dict[str, Any]
    drivers: List[Dict[str, Any]]
    vehicles: List[Dict[str, Any]]
    issues: List[str]

# Assessment Result
class AssessmentResult(TypedDict):
    product_code: str
    overall_risk_tier: str
    key_factors: List[str]
    # ... additional fields
```

## Usage Examples

### Basic Usage

```python
from src.agents.multi_agent_graph import create_rating_engine
import json

# Create rating engine
engine = create_rating_engine("Monthly-Comfort")

# Sample application data
application = {
    "household": {"address": "123 Main St"},
    "drivers": [{"name": "John Doe", "age": 35}],
    "vehicles": [{"make": "Toyota", "model": "Camry"}]
}

# Process application
result = engine.process_application_with_graph(json.dumps(application))

print(f"Status: {result.status}")
print(f"Premium: ${result.premium_calculation.get('total_premium', 0):.2f}")
```

### Streamlit Web Interface

Run the enhanced Streamlit app:

```bash
streamlit run src/streamlit_app.py
```

Features:
- **Multi-agent graph processing** with real-time visualization
- **Interactive result exploration** with detailed breakdowns
- **System status monitoring** and agent execution tracking
- **Sample data loading** for quick testing

### Command Line Demo

Run the demonstration script:

```bash
python demo_multi_agent.py
```

This script demonstrates:
- All product variations (Economy, Comfort, Turbo)
- Individual agent capabilities
- End-to-end workflow processing
- Error handling and validation

## Configuration

### Environment Variables

```bash
# Required for model gateway
TELENAV_API_KEY=your_api_key_here
TELENAV_BASE_URL=https://us-ailab-api.telenav.com/v1/messages
MODEL_NAME=claude3.5-bedrock
```

### Product Configuration

Products are defined in `ProductDefinitionAgent`:

- **Monthly-Economy** - Basic coverage with essential risk factors
- **Monthly-Comfort** - Standard coverage with comprehensive assessment
- **Monthly-Turbo** - Premium coverage with advanced features

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run multi-agent specific tests
pytest tests/test_multi_agent_system.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

The test suite covers:
- Individual agent functionality
- Graph orchestration workflows
- Error handling and edge cases
- Integration between components
- End-to-end processing scenarios

## Performance and Scalability

### Graph Execution

- **Parallel processing** where possible (independent agents)
- **Sequential dependencies** respected through graph edges
- **Timeout protection** to prevent infinite loops
- **Resource monitoring** and execution limits

### Fallback Mechanisms

- **Sequential processing** when Strands is unavailable
- **Error isolation** to prevent cascade failures
- **Graceful degradation** with informative messages

## Development

### Adding New Agents

1. Create agent class with required interface:
```python
class NewAgent:
    def __init__(self):
        self.agent = init_agent()
    
    def process(self, input_data):
        # Agent logic here
        return result
```

2. Add to graph in `multi_agent_graph.py`:
```python
builder.add_node(new_agent, "new_agent")
builder.add_edge("previous_agent", "new_agent")
```

3. Update result processing and tests

### Extending Product Definitions

Add new products in `ProductDefinitionAgent`:

```python
def _add_new_product(self):
    new_product = ProductDefinition(
        product_code="New-Product",
        product_name="New Product Package",
        risk_factors=[...],
        assessment_rules={...},
        coverage_options={...}
    )
    self.product_definitions["New-Product"] = new_product
```

## Monitoring and Observability

### Execution Tracking

The system provides comprehensive tracking:

- **Session IDs** for request correlation
- **Execution order** and timing
- **Agent performance** metrics
- **Error categorization** and reporting

### Logging

Structured logging throughout:

```python
logger.info(f"Processing application for {product_code}")
logger.debug(f"Risk factors: {risk_factors}")
logger.error(f"Processing failed: {error}")
```

## Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELENAV_API_KEY=your_key

# Run Streamlit app
streamlit run src/streamlit_app.py
```

### Production Considerations

- **Environment variable management** for API keys
- **Error monitoring** and alerting
- **Performance monitoring** for agent execution times
- **Scalability planning** for concurrent requests

## Troubleshooting

### Common Issues

1. **Strands Agents not available**
   - System falls back to sequential processing
   - Check installation: `pip install strands-agents==1.7.1`

2. **Model gateway errors**
   - Verify `TELENAV_API_KEY` is set
   - Check network connectivity
   - Review API endpoint configuration

3. **Graph execution failures**
   - Check agent dependencies and edge definitions
   - Review timeout settings
   - Examine individual agent logs

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger("src.agents").setLevel(logging.DEBUG)
```

## Contributing

1. Follow the existing code structure and patterns
2. Add comprehensive tests for new functionality
3. Update documentation and README files
4. Ensure backward compatibility with existing interfaces

## License

This project demonstrates multi-agent system architecture using Strands Agents. See the main project README for license information.

---

*Built with ❤️ using [Strands Agents](https://strandsagents.com/) and modern Python practices.*
