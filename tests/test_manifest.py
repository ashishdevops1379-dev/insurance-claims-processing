"""Regression tests for the agent manifest structure."""
import unittest
from pathlib import Path
import yaml

MANIFEST = Path(__file__).parents[1] / "app" / "insurance-claims-processing.yaml"

class ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with MANIFEST.open(encoding="utf-8") as stream:
            cls.manifest = yaml.safe_load(stream)

    def test_four_expected_agents_exist(self):
        ids = {agent["id"] for agent in self.manifest["spec"]["agents"]}
        self.assertEqual(ids, {"claim-intake-agent", "policy-validation-agent", "claims-assessment-agent", "workflow-recommendation-agent"})

    def test_graph_edges_are_sequential(self):
        edges = self.manifest["spec"]["orchestration"]["edges"]
        self.assertEqual([(e["from"], e["to"]) for e in edges], [("claim-intake-agent", "policy-validation-agent"), ("policy-validation-agent", "claims-assessment-agent"), ("claims-assessment-agent", "workflow-recommendation-agent")])

    def test_human_authorization_guardrail_is_present(self):
        text = "\n".join(agent.get("instructions", "") for agent in self.manifest["spec"]["agents"])
        self.assertIn("human review", text.lower())
        self.assertIn("do not automatically approve", text.lower())

if __name__ == "__main__":
    unittest.main()
