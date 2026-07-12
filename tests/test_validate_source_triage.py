import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATOR = os.path.join(ROOT, "scripts", "validate_source_triage.py")


def valid_artifact(decision="defer_or_monitor", coverage="abstract_and_toc", inspected=None):
    if inspected is None:
        inspected = ["abstract", "table_of_contents"] if coverage != "metadata_only" else []
    return {
        "schema_version": "0.2",
        "run_id": "test-001",
        "created_at": "2026-07-12T00:00:00Z",
        "source": {
            "title": "Example Report",
            "path_or_url": "https://example.com/report.pdf",
            "source_type": "report",
            "sensitivity": "public",
        },
        "triage_decision": decision,
        "basis": "The source has enough relevance for the stated attention decision.",
        "input_coverage": coverage,
        "inspected_sections": inspected,
        "fit_target": "current decision",
        "expected_deep_read_cost": "medium",
        "expected_decision_impact": "medium",
        "expected_attention_saved": "medium",
        "confidence": "medium",
        "uncertainty": "The full source and its factual claims were not verified.",
        "not_inferred": "The source is not treated as proof of a recommendation.",
        "revisit_trigger": "The named decision becomes active or new source evidence appears.",
        "recommended_next_gate": "Read only the named sections before deciding whether to invest further.",
        "writeback_status": "none",
    }


def run_validator(artifact):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "artifact.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(artifact, handle)
        result = subprocess.run(
            [sys.executable, VALIDATOR, path], capture_output=True, text=True, check=False
        )
        return result.returncode, json.loads(result.stdout)


class TestValidateSourceTriage(unittest.TestCase):
    def test_valid_quick_read_now(self):
        code, result = run_validator(valid_artifact("quick_read_now", "sampled_sections", ["summary", "section_4"]))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

    def test_quick_read_missing_next_gate_invalid(self):
        artifact = valid_artifact("quick_read_now")
        artifact["recommended_next_gate"] = ""
        code, result = run_validator(artifact)
        self.assertEqual(code, 2)
        self.assertIn("recommended_next_gate", " ".join(result["errors"]))

    def test_sampled_sections_empty_inspection_invalid(self):
        code, result = run_validator(valid_artifact("quick_read_now", "sampled_sections", []))
        self.assertEqual(code, 2)
        self.assertIn("inspected_sections", " ".join(result["errors"]))

    def test_metadata_only_empty_inspection_valid(self):
        code, result = run_validator(valid_artifact("pending_context", "metadata_only", []))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

    def test_read_deep_now_with_next_gate_valid(self):
        code, result = run_validator(valid_artifact("read_deep_now"))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

    def test_v01_is_rejected_with_version_message(self):
        artifact = valid_artifact()
        artifact["schema_version"] = "0.1"
        code, result = run_validator(artifact)
        self.assertEqual(code, 2)
        self.assertIn("v0.1", " ".join(result["errors"]))

    def test_forbidden_internal_key_invalid(self):
        artifact = valid_artifact()
        artifact["durable_writeback"] = True
        code, result = run_validator(artifact)
        self.assertEqual(code, 2)
        self.assertIn("forbidden", " ".join(result["errors"]))

    def test_wrong_root_type_invalid(self):
        code, result = run_validator(["not", "an", "object"])
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
