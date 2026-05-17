---
id: SPEC-WRITER
version: v1
status: drafted
owner: Laksh (v1, solo)
last_updated: 2026-04-29
tooling: Cowork (prose-shaped output; Claude.ai Project as alternative)
---

# Spec Writer — Specialist Contract

**Job:** Turn a use case description into a structured PRD that the Rule Lister can parse without re-interpreting intent.

---

## Purpose

The Spec Writer is the entry point of the pipeline. It takes raw use-case input — a paragraph, a Slack thread, a stakeholder request — and produces a PRD against `forms/prd-template.md`. The PRD is precise enough that downstream agents can derive AC, schema additions, and scenarios without going back to the source.

If the Spec Writer's output is loose, every downstream artefact compounds the looseness. This is the single most leverage-bearing specialist in the fleet.

---

## Inputs

The Spec Writer reads, in order:

1. **The use case input** — captured in the run card at `runs/<YYYY-MM-name>/00-run-card.md`, in the "Stakeholder brief (input)" section. Required. The Spec Writer reads from the file, not from chat. If a brief is larger than a page, it lives in `runs/<YYYY-MM-name>/_input/` and the run card links to it.
2. **`forms/prd-template.md`** — output shape. Required.
3. **`style/voice-profile-laksh.md`** — voice. Required.
4. **`style/anti-ai-pm-writing-style.md`** — final-pass filter. Required.
5. **Affected domain knowledge slice(s)** — `domains/<domain>/README.md`, `use-cases.md`, `regulatory-anchors.md`, `ac-corpus.md` for every domain the use case touches. Required.
6. **`knowledge-base/banking-domain-context.md`** — for cross-domain context. Required when the use case spans more than one domain.
7. **`knowledge-base/delegation-use-cases.md`** — for any use case involving delegation, PoA, bereavement, guardianship, mandates, minor accounts, appointeeship, or trusteeship. Required when applicable.
8. **The existing PRD example** — `LS-AuthZPM/docs/third_party_access.md` — for level-of-specificity calibration. Reference only.

The PM declares, in the run card frontmatter, which domains the use case touches. The Spec Writer does not infer scope from the brief.

**Why the brief lives in the run card and not in chat.** Reproducibility. If the brief is only ever in chat, the run is not a self-contained artefact — re-opening it months later (for audit, for handover, for porting to work) yields a PRD without the input that produced it. Capturing the brief in the run card is the small bookkeeping cost that makes the run a complete record.

---

## Output

- **File:** `runs/<YYYY-MM-name>/01-prd.md`
- **Form:** `forms/prd-template.md` (all required sections, in order, with frontmatter)
- **Status on first emission:** `draft`

---

## Trust posture

**Auto-suggest.** The Spec Writer never auto-acts. Every PRD it produces is a draft. The PM reviews, edits if needed, and flips status to `approved` before the Rule Lister runs.

In v1 (solo build), the PM is the only reviewer. At port-to-work, affected domain SMEs co-review their domain-scoped sections.

---

## Quality bar — what good looks like

A pass-grade PRD:

- Opens with the problem and its magnitude. First paragraph carries information the reader doesn't already have.
- Names every subject, resource, action, condition, and regulatory anchor explicitly.
- Has an "Out of scope" section longer than two bullets. Empty or one-line out-of-scope sections fail.
- Has at least three open questions. Empty open-questions sections fail.
- Cites at least one regulatory anchor that already exists in the affected domain's `regulatory-anchors.md`. If a new anchor is needed, it appears in the Open Questions section.
- Passes the anti-AI filter — no "delve into", "robust", "leverage", "underscore", "in conclusion", three-adjective lists, comprehensive emptiness, challenges-and-future-outlook closers.
- Length: 1.5–3 pages for single-domain, up to 5 for multi-domain. If longer, the use case is probably two PRDs.

A fail-grade PRD:

- Opens with generic context ("In today's evolving regulatory landscape...").
- States "trade-offs exist" without naming any.
- Lists every domain as affected when the use case clearly touches one or two.
- Uses hedge words ("should", "may", "might consider").
- Has a closing paragraph rather than open questions.
- Inflates significance ("This represents a pivotal shift...").

---

## Human gate

PM reviews against the quality bar and against the original use case input. Two questions:

1. Does this PRD match the use case I gave it? (Fidelity.)
2. Could the Rule Lister produce AC from this without asking me clarifying questions? (Sufficiency.)

If either answer is no, push back to the Spec Writer with a specific note. Don't accept and edit — that defeats the agent loop. Editing manually is a smell that says either the contract or the prompt needs work.

---

## Invocation pattern

A typical invocation, in plain language:

> "Spec Writer: produce a PRD for the trusteeship use case. Affects accounts and customer-mgmt domains. The setup: a customer has a trust-held current account, with multiple trustees. Trustees need scope-bounded transactional access; some actions require unanimous trustee consent. Use case ID: UC-A-11. Run folder: `runs/2026-05-trusteeship/`."

The Spec Writer responds with a complete `01-prd.md` against the template, ready for review.

---

## Evaluation rubric

When tuning this specialist, test against three known use cases (each producing a known-good PRD as reference):

1. **Third-party access** (existing PRD as comparison: `LS-AuthZPM/docs/third_party_access.md`).
2. **Joint accounts (either-to-sign)** — a use case the Accounts AC corpus already covers.
3. **PoA — UK LPA Property and Financial Affairs** — same.

Pass criteria:

- Output PRD matches the reference on the substantive sections (subjects, resources, actions, regulatory anchors).
- Voice matches Laksh's profile on prose sections.
- Out-of-scope section names at least three things the reference also excluded.

If two of three reference use cases produce divergent PRDs, the prompt is wrong, not the references. Tune the prompt.

---

## Known limitations

- The Spec Writer has no view into ongoing runs. If two use cases overlap in scope, it won't surface the overlap. PM must flag.
- The Spec Writer does not write AC. It only produces input *for* the Rule Lister. Any "AC" it includes is illustrative, not authoritative.
- Multi-domain use cases stretch the Spec Writer's coherence. Outputs above 5 pages should be inspected for whether they're really one use case or two.

---

## Versioning

| Version | Date | Change |
|---|---|---|
| v1 | 2026-04-29 | Initial draft. |
