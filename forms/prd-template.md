# PRD Form — Template

> The shape every PRD takes. Used by the Spec Writer specialist on the way out, by the Rule Lister on the way in. Tight, AC-feedable, regulator-defensible.

---

## Why this form exists

A PRD for an entitlement use case is not a marketing doc. Its job is to define a use case precisely enough that the Rule Lister can generate AC without re-interpreting the intent. Loose PRDs produce loose AC, which produce loose scenarios, which fail in production.

This template is deliberately structured for downstream parsing. Every section maps to fields the Rule Lister will look for. Skipping or rephrasing sections breaks the pipeline.

---

## Form shape

Every PRD has the following sections, in this order. Frontmatter required.

```yaml
---
id: PRD-<DOMAIN>-<NN>            # e.g. PRD-A-11 for the 11th Accounts PRD
use_case_id: UC-<DOMAIN>-<NN>    # the use case this PRD defines
domains: [<one or more from: accounts, payments, cards, communications, customer-mgmt>]
status: <draft|approved|deprecated>
source_run: runs/<YYYY-MM-name>
last_updated: <YYYY-MM-DD>
---
```

### 1. Problem

One paragraph. What's the user problem or business need that requires this use case? Be specific about who it affects and how often. No "in today's evolving landscape" openings.

### 2. Magnitude

One paragraph or a short table. How big is this? Number of customers affected per year, regulatory exposure if we don't handle it, current workaround cost. If you can't quantify, say so plainly.

### 3. Subject(s)

Who is the new or changed actor in this use case? Name them in plain language and in schema terms.

- **Plain language:** *e.g. Trustee acting on behalf of a trust*
- **Schema relation:** *e.g. `account#trustee` (proposed)*

If the subject is an existing relation, link to its current AC in the relevant `ac-corpus.md`.

### 4. Resource(s)

What resources are affected? Account, Payment, Card, Communication, Customer Profile — or new resource types.

- **Resource type:** *e.g. `account` with state `held_in_trust`*
- **Existing or new:** existing
- **Cross-domain dependencies:** *e.g. `payment` derives via `source_account`*

### 5. Actions

What can the new subject do, and not do? Bullet list, kept terse. Each entry pairs an action with an expected outcome.

```
- View balances and transactions → allow
- Initiate payments → conditional (within trust deed scope)
- Add new payees → conditional (within trust deed scope)
- Close the account → deny
- Change beneficiaries → deny (without unanimous trustee consent — workflow gate)
```

### 6. Conditions and caveats

State-dependent and context-dependent rules. Anything that can't be answered "yes" or "no" without additional context.

- *Trust deed scope* — caveat `trust_scope` (proposed). Action passed in context.
- *Multiple-trustee joint-action requirement* — application-layer workflow, not in schema.
- *Trust validity window* — `delegation_window` reused.

If you propose a new caveat, name it here and explain why an existing caveat won't do.

### 7. Regulatory anchors

Named, specific. No generic "complies with FCA rules."

- Trustee Act 2000 s.34 — duty of care
- Mental Capacity Act 2005 — interaction with PoA on the same trust
- FCA Consumer Duty — vulnerable customer treatment (where the settlor is vulnerable)

If a relevant regulation isn't already in the affected domain's `regulatory-anchors.md`, flag it as an open question (section 11).

### 8. Success criteria

The check that proves this use case is correctly modelled. Phrased as observable outcomes, not features.

- A trustee with `trust_scope: [view, transact]` can initiate FPS up to the daily limit, but cannot add new payees.
- Removing a trustee revokes all access on the next consistency-fresh check.
- A two-trustee account requires both trustee signatures for payments above the trust deed's defined threshold (workflow-gated; schema enables holder check).

### 9. Out of scope

Explicit list of what this PRD does NOT cover. This section is required and almost always longer than people expect.

- Charitable trust accounts (different regulatory regime).
- Trustee onboarding KYC (lives in CustMgmt PRD).
- Tax reporting flows.
- Automatic detection of trustee removal from the trust deed (manual flag for now).

### 10. Risks

Three or four short bullets. What could go wrong, what's the mitigation.

### 11. Open questions

Required. Empty open-questions sections signal incomplete thinking.

- Does a corporate trustee need a separate relation, or is `trustee: user` plus a corporate-account flag enough?
- What's the FCA expectation when a settlor lacks capacity AND is a beneficiary? Likely cross-cuts with PoA.
- Tax reporting on trust accounts — separate workstream or owned here?

---

## Style and voice

- Match the voice profile (`style/voice-profile-laksh.md`) and pass the anti-AI filter (`style/anti-ai-pm-writing-style.md`).
- Outcome-first, problem-first opening. No throat-clearing.
- Trade-offs explicit. Hedging minimal.
- Tables and bullets where they earn their place; prose where they don't.

## Length target

A PRD for a single-domain use case should fit in 1.5–3 pages of plain reading. A multi-domain PRD can stretch to 4–5. If it's longer, the use case is probably two PRDs.

## Worked example

For an example of what an approved PRD looks like, see `LS-AuthZPM/docs/third_party_access.md` (pre-framework PRD, retained for reference). Don't copy its structure literally — that one was written before this form existed — but the level of specificity is the bar.
