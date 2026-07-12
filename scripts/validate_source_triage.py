#!/usr/bin/env python3
"""Mechanical validator for source-triage v0.2 artifacts."""

import argparse
import json
import sys
from pathlib import Path

SCHEMA_VERSION = "0.2"
DECISIONS = {
    "quick_read_now",
    "read_deep_now",
    "project_relevant_but_not_now",
    "reference_only",
    "defer_or_monitor",
    "do_not_invest_further_now",
    "pending_context",
}
COVERAGE = {"metadata_only", "abstract_and_toc", "sampled_sections", "other"}
ORDINAL = {"low", "medium", "high", "unknown"}
CONFIDENCE = {"low", "medium", "high"}
FORBIDDEN_KEYS = {
    "durable_writeback",
    "project_route",
    "world" + "_model_writeback",
    "install_skill",
    "telemetry",
    "automatic_action",
}
REQUIRED_TOP_LEVEL = {
    "schema_version",
    "source",
    "triage_decision",
    "basis",
    "input_coverage",
    "inspected_sections",
    "fit_target",
    "expected_deep_read_cost",
    "expected_decision_impact",
    "expected_attention_saved",
    "confidence",
    "uncertainty",
    "not_inferred",
    "revisit_trigger",
    "recommended_next_gate",
    "writeback_status",
}


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def report(status, errors=None, warnings=None):
    return {
        "status": status,
        "schema_version": SCHEMA_VERSION,
        "errors": errors or [],
        "warnings": warnings or [],
    }


def validate_artifact(data):
    errors = []
    if not isinstance(data, dict):
        return report("invalid", ["root must be a JSON object"])

    forbidden = sorted(FORBIDDEN_KEYS.intersection(data))
    if forbidden:
        errors.append("forbidden top-level keys: " + ", ".join(forbidden))

    missing = sorted(key for key in REQUIRED_TOP_LEVEL if key not in data)
    if missing:
        errors.append("missing required keys: " + ", ".join(missing))

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            "unsupported schema_version: expected 0.2; v0.1 artifacts are intentionally not supported"
        )

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        for key in ("title", "path_or_url", "source_type", "sensitivity"):
            if not nonempty_string(source.get(key)):
                errors.append(f"source.{key} must be a nonempty string")

    decision = data.get("triage_decision")
    if decision not in DECISIONS:
        errors.append("triage_decision must be a supported decision")

    coverage = data.get("input_coverage")
    if coverage not in COVERAGE:
        errors.append("input_coverage must be a supported coverage value")

    inspected = data.get("inspected_sections")
    if not isinstance(inspected, list) or not all(nonempty_string(item) for item in inspected):
        errors.append("inspected_sections must be a list of nonempty strings")
    elif coverage in COVERAGE - {"metadata_only"} and not inspected:
        errors.append("inspected_sections must be nonempty unless input_coverage is metadata_only")

    for key in ("basis", "fit_target", "uncertainty", "not_inferred", "revisit_trigger", "recommended_next_gate"):
        if not nonempty_string(data.get(key)):
            errors.append(f"{key} must be a nonempty string")

    for key in ("expected_deep_read_cost", "expected_decision_impact", "expected_attention_saved"):
        if data.get(key) not in ORDINAL:
            errors.append(f"{key} must be one of: low, medium, high, unknown")

    if data.get("confidence") not in CONFIDENCE:
        errors.append("confidence must be one of: low, medium, high")

    if data.get("writeback_status") != "none":
        errors.append("writeback_status must be none")

    if errors:
        return report("invalid", errors)
    return report("valid")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate a source-triage v0.2 JSON artifact")
    parser.add_argument("artifact", help="path to a JSON artifact")
    args = parser.parse_args(argv)
    try:
        with Path(args.artifact).open("r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps(report("usage_or_io_error", [str(exc)]), ensure_ascii=False))
        return 1

    result = validate_artifact(data)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "valid" else 2


if __name__ == "__main__":
    sys.exit(main())
