# Triage Rules

## Attention first

Use the smallest reliable input: title/metadata, abstract, table of contents, or clearly named sampled sections. State what was inspected and do not imply a full read.

## Choose one decision

- `quick_read_now`: a 5-15 minute bounded read can change the next decision.
- `read_deep_now`: a present, named decision justifies 30-60+ minutes of deeper reading or research.
- `project_relevant_but_not_now`: direct fit exists, but a current priority blocks attention.
- `reference_only`: reference value exists without a current deep-read commitment.
- `defer_or_monitor`: plausible future value with a concrete revisit trigger.
- `do_not_invest_further_now`: a reversible no-attention decision with a reason and trigger.
- `pending_context`: the source or decision target is too unclear to decide responsibly.

## Inspection rule

`metadata_only` may use `inspected_sections: []`.

For `abstract_and_toc`, `sampled_sections`, or `other`, list the actual inspected material. Do not convert a guessed outline into inspected coverage.

## Decision discipline

- Separate source relevance from source truth.
- Separate project fit from a generic topic match.
- Do not treat a model's own confidence as evidence.
- Do not promise exact time savings; use ordinal estimates only.
- Name what was not inferred.
- Give a next gate, but do not perform it.

## Anti-patterns

- Full-source summary disguised as triage.
- Treating `quick_read_now` as permission for deep research.
- Treating `read_deep_now` as automatic extraction or implementation.
- Calling a source useless from a thin screen.
- Treating user feedback, a model preference, or a benchmark-like example as causal proof.
- Adding project routing, durable memory, or automatic action to this small Skill.
