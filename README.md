# Insurance Claims Processing Agent

Multi-agent insurance claims workflow authored for IBM Consulting Advantage Agentic App Studio.

## Architecture

The manifest under `app/` defines a LangGraph workflow with four agents:
1. Claim Intake Agent
2. Policy Validation Agent
3. Claims Assessment Agent
4. Workflow Recommendation Agent

## Repository structure

```text
.
├── .github/workflows/validate.yml
├── app/insurance-claims-processing.yaml
├── scripts/validate_manifest.py
├── tests/test_manifest.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Validate locally

```bash
python -m pip install -r requirements.txt
python scripts/validate_manifest.py app/insurance-claims-processing.yaml
python -m unittest discover -s tests -v
```

## Important platform notes

- This repository contains the IBM Agentic App Studio agent manifest; it is not a standalone web service or container image.
- The workflow currently has sequential graph edges. It does not configure conditional graph routing.
- No tools are assigned to the agents in the generated manifest. Connect the published Context Studio context using the supported platform integration before relying on live policy or claim data.
- Confirm the supported import/deployment mechanism for your IBM environment before adding a CD deployment step. The included GitHub Actions workflow performs structural checks only.
- Do not commit API keys, MCP gateway tokens, or other secrets. Store credentials in your approved secrets manager.

## Human review safeguard

The agents are instructed not to automatically approve, reject, or authorize payment. Final claim decisions require authorized human review.
