#!/usr/bin/env python3
"""Basic structural checks for the IBM Agentic App Studio manifest."""
import sys
from pathlib import Path
import yaml

EXPECTED_AGENTS = {
    "claim-intake-agent",
    "policy-validation-agent",
    "claims-assessment-agent",
    "workflow-recommendation-agent",
}
EXPECTED_EDGES = [
    ("claim-intake-agent", "policy-validation-agent"),
    ("policy-validation-agent", "claims-assessment-agent"),
    ("claims-assessment-agent", "workflow-recommendation-agent"),
]

def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "app/insurance-claims-processing.yaml")
    with path.open(encoding="utf-8") as stream:
        manifest = yaml.safe_load(stream)
    assert manifest.get("apiVersion") == "aiis.ibm.com/v1alpha1", "Unexpected apiVersion"
    assert manifest.get("kind") == "agent", "Expected kind: agent"
    spec = manifest.get("spec", {})
    assert spec.get("framework") == "langgraph", "Expected langgraph framework"
    orchestration = spec.get("orchestration", {})
    assert orchestration.get("type") == "graph", "Expected graph orchestration"
    agents = spec.get("agents", [])
    agent_ids = {agent.get("id") for agent in agents}
    assert agent_ids == EXPECTED_AGENTS, f"Unexpected agent IDs: {sorted(agent_ids)}"
    actual_edges = [(edge.get("from"), edge.get("to")) for edge in orchestration.get("edges", [])]
    assert actual_edges == EXPECTED_EDGES, f"Unexpected graph edges: {actual_edges}"
    assert orchestration.get("entryPoint") == "claim-intake-agent", "Unexpected entry point"
    print(f"Manifest structure OK: {path}")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, yaml.YAMLError) as exc:
        print(f"Manifest validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
