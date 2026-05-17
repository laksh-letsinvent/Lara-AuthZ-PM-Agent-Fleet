---
id: SCHEMA-SKETCHER
version: v2
status: active — optional step
owner: Laksh + TL (joint, dual-gate)
last_updated: 2026-05-10
tooling: Cowork (primary); Claude Code recommended when zed CLI validation is available
---

# Schema Sketcher — Specialist Contract

**Job:** Turn an approved AC corpus into a proposed extension to one or more `domains/*/schema-fragment.zed` files, accompanied by tradeoff notes, pattern citations, and dependency declarations.

---

## Purpose

The Schema Sketcher is the first code-shaped specialist in the pipeline. It takes the approved AC and proposes the minimal additive schema changes that make those AC realisable in SpiceDB. Its output is `.zed` code with structured rationale around it.

Because schema changes are the highest-stakes artefact in the framework — once merged, they shape every relationship and check forever — this specialist runs under the dual-gate review: PM signs off on semantics, TL signs off on implementation. Neither gate can be skipped.

---

## Inputs

1. **The approved AC** — `runs/<YYYY-MM-name>/02-rules.md`. Required.
2. **The current consolidated schema** — `schema/consolidated.zed` (or, in v1 with only Accounts populated, `domains/accounts/schema-fragment.zed`). Required.
3. **Affected domain `schema-fragment.zed` files** — for each domain the AC touches. The Schema Sketcher proposes additions per-fragment, never to the consolidated file. Required.
4. **`forms/schema-sketch-template.md`** — output shape. Required.
5. **`knowledge-base/schema-design-patterns.md`** — every sketch cites at least one pattern. Required.
6. **`knowledge-base/zanzibar-spicedb-reference.md`** — for caveat semantics, consistency, traversal-depth checks. Required.
7. **Affected domain `regulatory-anchors.md`** — for understanding why the AC is shaped the way it is. Reference only.
8. **Existing AC corpus** for the affected domains — the proposed schema additions must not break existing AC. Backward-compat assessment is a required output section.

---

## Output

- **File:** `runs/<YYYY-MM-name>/03-schema-sketch.md`
- **Form:** `forms/schema-sketch-template.md`
- **Format:** Markdown with embedded `.zed` blocks, structured per-fragment.
- **Status on first emission:** `proposed`. Flips to `signed-off-pm`, then `signed-off-tl`, then `approved` only after both gates.
- **Validation:** the proposed schema must pass `zed validate` (or equivalent SpiceDB schema lint) when concatenated with the unchanged portions of all other fragments. The Schema Sketcher runs this validation as part of its loop and refuses to emit invalid schema.

---

## Trust posture

**Auto-suggest only, dual-gate.** The Schema Sketcher never writes to `domains/*/schema-fragment.zed`. It only proposes additions in the run folder. Merge happens manually after both sign-offs.

The dual gate is non-negotiable:

- **PM gate (semantics).** Does the relation correctly model the use case? Does the permission set match the AC? Are caveats appropriate to the regulatory anchor?
- **TL gate (implementation).** Is this idiomatic SpiceDB? Does it pass schema lint? Does it respect traversal-depth limits (≤3 hops)? Are wildcard rules used only on read permissions? Are performance and consistency assumptions sound?

A sketch can sit at `signed-off-pm` for a while waiting for TL bandwidth — that's expected. It cannot skip TL review.

---

## Quality bar — what good looks like

A pass-grade sketch:

- Cites at least one pattern from `schema-design-patterns.md`. Inventing a new pattern is allowed but requires a specific subsection naming why existing patterns don't fit.
- Proposes the **minimal** additive change. New relations rather than modified existing ones, where possible.
- Proposes additions to one fragment unless the AC genuinely spans multiple definitions. Multi-fragment changes are split clearly per-fragment in the output.
- Backward-compat section enumerates *which* existing AC and scenarios were checked, not just "no impact."
- Cross-domain dependency section is non-empty (or explicitly notes "no cross-domain references").
- Performance and consistency notes are specific: caveat overhead estimated, security-critical checks named with their consistency posture, fan-out concerns flagged where applicable.
- Test surface section names which AC IDs will exercise the proposed schema in scenarios.
- Open questions section is non-empty.
- Validation: schema lints clean.

A fail-grade sketch:

- Modifies existing relations or permissions without clear necessity (additive change preferred).
- Invents a pattern without justification.
- Backward-compat section says "no impact" without showing review work.
- Performance assertions that aren't grounded ("this will be fast" without basis).
- Schema lint fails.
- Missing pattern citation.
- Open-questions section empty.

---

## Human gate

Two gates, sequential:

**PM gate.** PM reviews:
- Does the relation match the AC's subject definition?
- Is the permission set consistent with the AC's expected outcomes?
- Are caveats correctly used (PoA-style scope, time windows, consent)?
- Is the regulatory anchor honoured?

PM flips status to `signed-off-pm`. If issues, returns to Schema Sketcher with specifics.

**TL gate.** TL reviews:
- Idiomatic SpiceDB?
- Schema lints clean (re-runs `zed validate`)?
- Traversal depth, fan-out, consistency posture all reasonable?
- Backward-compat actually backward-compatible?

TL flips status to `signed-off-tl`. PM then flips to `approved`. Both signatures recorded in run card decision log.

In v1 (solo build), Laksh plays both gates but separates them temporally — review with PM hat first, sleep on it, review with TL hat next session. The discipline matters more than the staffing.

---

## Invocation pattern

> "Schema Sketcher: produce a schema sketch for the trusteeship use case at `runs/2026-05-trusteeship/`. Approved AC are in `02-rules.md`. Current Accounts schema is `domains/accounts/schema-fragment.zed`. Customer-mgmt fragment is empty (stub). Output: `runs/2026-05-trusteeship/03-schema-sketch.md`. Validate against `zed validate` before emitting."

The Schema Sketcher responds with a complete `03-schema-sketch.md`, validated, all required sections filled.

---

## Why this specialist runs in Claude Code

Three reasons:

1. **Output is `.zed` code.** Code-shaped output is faster and more accurate in an IDE-shaped tool.
2. **Validation is a build step.** `zed validate` runs naturally in a terminal, with hot retries when the schema is malformed. Cowork would have to shell out for every iteration.
3. **TL review happens in their tool.** The TL is in Claude Code anyway; producing the sketch in Claude Code means review uses the same diff/PR tooling they use for production code.

The contract (this file) lives in Cowork because the contract is a PM artefact. The specialist runs in Claude Code. Same framework folder, different surfaces.

---

## Evaluation rubric

Test against three known schema additions from the existing system:

1. **Adding the `attorney` relation with `poa_scope`** — should reproduce something equivalent to the existing schema's PoA pattern.
2. **Adding the `delegate_view_pay` tier** — should reproduce something equivalent to the existing V&P pattern.
3. **Adding the bereavement state override** — should reproduce something equivalent to the existing `blocked@flag:bereavement` pattern.

Pass criteria:

- Output schema lints clean.
- Pattern citations correctly identify the relevant patterns from the patterns library.
- Tradeoff sections name realistic alternatives (not strawmen).

If the Schema Sketcher consistently invents patterns, the prompt needs reinforcement to start from the patterns library.

---

## Known limitations

- The Schema Sketcher cannot estimate true production performance. Estimates are from heuristics (fan-out, depth, caveat overhead) — not benchmarks. The TL signs off on performance posture *qualitatively*; benchmarks happen later, in eng work.
- Cross-domain coordination is the Schema Sketcher's hardest case. When a sketch touches three or more fragments, expect to invoke it once per fragment and stitch — or break the use case into multiple PRDs.
- The dual-gate ritual is a real coordination cost. Don't skip it; don't try to automate the TL gate.

---

## Versioning

| Version | Date | Change |
|---|---|---|
| v1 | 2026-04-29 | Initial draft. |
