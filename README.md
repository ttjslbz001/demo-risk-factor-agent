# Demo: Insurance Risk Factor Agent

## Quick Start
1. Create venv and install deps:

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
```

2. Set environment variables:

```bash
cp .env.example .env
# edit .env to add TELENAV_API_KEY
```

3. Verify environment:

```bash
python -m src.health_check
```

## Docs
- Design: docs/insurance_risk_factor_agent/DESIGN_insurance_risk_factor_agent.md
- Consensus: docs/insurance_risk_factor_agent/CONSENSUS_insurance_risk_factor_agent.md
- Tasks: docs/insurance_risk_factor_agent/tasks/TASKS_OVERVIEW.md

## Notes
- Do not commit real API keys. Use `.env` locally only.
