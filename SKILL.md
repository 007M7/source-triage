---
name: source-triage
description: Decide whether a source deserves attention now before reading it deeply. Use when a user asks whether an article, PDF, report, book, transcript, URL, or local file is worth reading, should be skimmed now, is relevant to a stated project, or should be deferred. Returns one bounded attention decision only; it does not summarize, research, verify facts, route projects, install skills, or write memory.
---

# Source Triage

Save attention before deeper reading. Return one decision and stop.

## Decisions

```text
quick_read_now                - spend 5-15 minutes on a bounded scan/read now
read_deep_now                 - justify a 30-60+ minute deep-reading or research commitment
project_relevant_but_not_now  - relevant to a named project, but timing is wrong
reference_only                - keep as reference/index; do not read deeply now
defer_or_monitor              - potentially useful later; revisit on a stated trigger
do_not_invest_further_now     - reversible decision not to invest attention now
pending_context               - insufficient source or decision context to decide
```

`quick_read_now` and `read_deep_now` are deliberately different. A quick read is bounded screening; deep reading is a larger commitment justified by a current decision.

## Required output

Return all fields below in a compact, readable form:

```text
triage_decision:
basis:
input_coverage: metadata_only | abstract_and_toc | sampled_sections | other
inspected_sections: [] or a short list of what was actually inspected
fit_target:
expected_deep_read_cost: low | medium | high | unknown
expected_decision_impact: low | medium | high | unknown
expected_attention_saved: low | medium | high | unknown
confidence: low | medium | high
uncertainty:
not_inferred:
revisit_trigger:
recommended_next_gate:
writeback_status: none
```

Use `inspected_sections: []` only for `metadata_only`. For any richer coverage, name the sections actually inspected. Never invent inspection.

## Boundaries

- This is attention triage, not fact verification, truth judgment, deep research, or a full summary.
- It does not automatically read further, route a project, create a task, write memory, install anything, or take product action.
- It does not infer project value without a stated target.
- It does not claim causal efficacy, exact time savings, or user outcomes from example runs.
- A no-action/defer decision must remain reversible and state a revisit trigger.
- If the user explicitly asks for deep analysis, treat that as a separate request; do not silently downgrade it to triage.

## Voluntary feedback

After using the decision in a real situation, users may optionally follow `FEEDBACK.md`. Feedback is local and voluntary: no telemetry, no automatic source upload, no automatic storage, and no automatic product conclusion.

## Resources

- `references/triage-rules.md` — decision discipline and anti-patterns.
- `references/output-templates.md` — v0.2 artifact schema.
- `scripts/validate_source_triage.py` — mechanical JSON validation.

## Stop boundary

Return the triage decision and `recommended_next_gate`; do not perform that next gate automatically.
