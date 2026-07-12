# Source Triage Artifact Schema v0.2

A triage artifact is optional. If written, it is a local JSON record only and must not cause automatic action.

```json
{
  "schema_version": "0.2",
  "run_id": "optional-local-id",
  "created_at": "2026-01-01T00:00:00Z",
  "source": {
    "title": "",
    "path_or_url": "",
    "source_type": "article|pdf|report|book|transcript|url|other",
    "sensitivity": "public|private|unknown"
  },
  "triage_decision": "quick_read_now|read_deep_now|project_relevant_but_not_now|reference_only|defer_or_monitor|do_not_invest_further_now|pending_context",
  "basis": "",
  "input_coverage": "metadata_only|abstract_and_toc|sampled_sections|other",
  "inspected_sections": [],
  "fit_target": "stated target or unknown",
  "expected_deep_read_cost": "low|medium|high|unknown",
  "expected_decision_impact": "low|medium|high|unknown",
  "expected_attention_saved": "low|medium|high|unknown",
  "confidence": "low|medium|high",
  "uncertainty": "",
  "not_inferred": "",
  "revisit_trigger": "",
  "recommended_next_gate": "",
  "writeback_status": "none"
}
```

Rules:

- `schema_version` must be `0.2`; v0.1 artifacts are intentionally rejected by the bundled validator with an explicit version error.
- `inspected_sections` must be a list of nonempty strings.
- `metadata_only` may use an empty `inspected_sections` list; all other coverage values require at least one listed section.
- `recommended_next_gate` is required and must be a recommendation, not evidence of an automatic action.
- `writeback_status` must be `none`.
- The artifact must not include internal routing, durable-writeback, telemetry, or installation keys.
