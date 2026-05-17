---
id: RULE-LISTER
version: v1
status: drafted
owner: Laksh (v1, solo)
last_updated: 2026-04-29
tooling: Cowork (mostly prose-shaped; structured output)
---

# Rule Lister — Specialist Contract

**Job:** Turn an approved PRD into a structured corpus of acceptance criteria, each one a specific, testable, anchored assertion that downstream specialists can consume mechanically.

---

## Purpose

The Rule Lister is the first specialist that produces machine-parseable output. Its job is to take a PRD's prose intent and emit AC against `forms/rules-template.md` — one assertion per AC, each anchored to a regulation or business source, each with positive and negative cases where applicable.

If the Spec Writer is the *most leverage-bearing* specialist, the Rule Lister is the *highest-precision* one. Sloppy AC produces sloppy schemas and sloppy scenarios; precise AC enables everything downstream.

---

## Inputs

1. **The approved PRD** — `runs/<YYYY-MM-name>/01-prd.md`. Required.
2. **`forms/rules-template.md`** — output shape, including the YAML field schema and coverage rules. Required. (Note: the output file is now `02-ac.md`, not `02-rules.md`.)
3. **Affected domain `regulatory-anchors.md`** for every affected domain. Required — every AC must cite at least one anchor that exists in the relevant file.
4. **Affected domain `ac-corpus.md`** for every affected domain. Required — the Rule Lister must avoid duplicating existing AC and must check its proposed AC for consistency with existing ones.
5. **Affected domain `schema-fragment.zed`** for every affected domain. Required — AC reference relations and permissions that exist (or are explicitly proposed in the PRD's section 3 on subjects).
6. **`knowledge-base/zanzibar-spicedb-reference.md`** — for caveat semantics, especially when the AC involves conditional logic. Required when AC includes caveats.
7. **`style/voice-profile.md`** and **`style/anti-ai-pm-writing.md`** — applied to the prose `statement:` field of each AC. Required.

---

## Output

- **File:** `runs/<YYYY-MM-name>/02-ac.md`
- **Form:** `forms/rules-template.md`
- **Format:** YAML blocks (one per AC) with prose statements, grouped by use case, secondarily by domain.
- **Status on first emission:** all AC have status `proposed`. They flip to `approved` on PM sign-off and only get appended to `domains/<domain>/ac-corpus.md` on run merge.

---

## Trust posture

**Auto-suggest.** The Rule Lister never auto-acts. AC are drafts until reviewed.

The Rule Lister is also auto-suggesting *coverage*. The PM verifies that every AC implied by the PRD is present, and that every AC's negative case is covered where applicable. The agent doesn't decide coverage is complete; the PM does.

---

## Quality bar — what good looks like

A pass-grade rules file:

- Hits every coverage target named in `forms/rules-template.md`: positive happy path, negative non-relation, state-blocking, caveat-out-of-scope, revocation. The Rule Lister explicitly notes which targets are not applicable for this use case (e.g. "no caveats — caveat-out-of-scope target N/A") rather than silently skipping.
- Every AC has exactly one assertion. "X can do Y *and* Z" is two AC.
- Every AC has a regulatory or business anchor that exists in the relevant `regulatory-anchors.md`. Missing anchors raise an open question; they don't get invented.
- Negative cases are paired with their positive counterparts where the negation is meaningful.
- Voice on `statement:` fields matches Laksh's profile. No "should", "may", "might". Bivalent assertions only — caveat-bearing AC use `expected: conditional`.
- Cross-domain ACs declare both domains in frontmatter; the primary domain owns the canonical entry.
- IDs respect the namespacing convention (A=Accounts, P=Payments, C=Cards, M=Communications, U=Customer-mgmt) and are sequential within the domain.

A fail-grade rules file:

- AC without anchors, or AC with anchors that don't exist in `regulatory-anchors.md`.
- Multi-assertion AC ("Holders can view AND transact AND close").
- Missing negative cases (e.g. "Trustee can transact" with no companion "Non-trustee cannot transact").
- Hedging in `statement:` fields ("should be allowed", "may permit").
- AC that refers to schema relations or permissions that don't exist and aren't explicitly proposed by the PRD.
- Coverage gaps not acknowledged.

---

## Human gate

PM reviews each AC against three checks:

1. **Anchor check.** Does this anchor exist? Does it actually support this assertion?
2. **Coverage check.** Are all required scenario types present (positive, negative, edge, state-transition, revocation, caveat) where the AC implies them?
3. **Consistency check.** Does this AC contradict or duplicate any AC already in the relevant `ac-corpus.md`? The Rule Lister flags suspected duplicates; the PM resolves.

Sign-off flips each AC's status from `proposed` to `approved`. AC that fail review get returned to the Rule Lister with the specific failure noted.

---

## Invocation pattern

> "Rule Lister: produce AC for the trusteeship PRD at `runs/2026-05-trusteeship/01-prd.md`. Affected domain: accounts. Use the existing AC corpus in `domains/accounts/ac-corpus.md` to avoid duplication and check consistency. Output: `runs/2026-05-trusteeship/02-ac.md`."

The Rule Lister responds with a complete `02-ac.md`, AC grouped by domain, every AC with frontmatter status `proposed`.

---

## Evaluation rubric

Test against the same three reference use cases as Spec Writer:

1. **Third-party access** — should produce AC equivalent to AC-A-005, AC-A-006, AC-A-007 in the existing corpus.
2. **Joint accounts** — should produce AC-A-003, AC-A-004 equivalents.
3. **PoA UK LPA** — should produce AC-A-008, AC-A-009, AC-A-010 equivalents.

Pass criteria:

- Output AC corpus covers the same assertions as the reference (allowing for ID renumbering).
- All anchors cite existing entries in `regulatory-anchors.md`.
- Coverage targets hit; negative cases included.

If the Rule Lister consistently misses negative cases or under-cites anchors, the prompt needs reinforcement on those specific quality bars.

---

## Known limitations

- The Rule Lister cannot verify that a regulatory anchor *actually* supports an assertion. It can only confirm the anchor exists. A PM with regulatory understanding has to check whether the anchor truly applies. This is a hard gate, not negotiable.
- Caveat-bearing AC are the trickiest. The Rule Lister sometimes produces a single conditional AC where two AC (in-scope and out-of-scope) would be cleaner. Push back when this happens.
- Cross-domain AC are rare and worth treating as an exception, not a default. If the Rule Lister produces several, the PRD probably split too narrowly.

---

## Versioning

| Version | Date | Change |
|---|---|---|
| v1 | 2026-04-29 | Initial draft. |
