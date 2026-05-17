---
domain: accounts
last_updated: 2026-05-13
---

# Accounts — AC Corpus and Use Case Registry

Approved ACs for this domain, grouped by use case. Also serves as the use case registry — each section heading is a registered use case.

The Scenario Builder uses this corpus as input. Every AC here produces one or more scenarios in `runs/*/03-scenarios.md`.

---

## Use Case Registry

| ID | Use case | Status | Originating run | Notes |
|---|---|---|---|---|
| UC-A-001 | Joint Current Account — Access and Delegation Baseline | Approved | `runs/2026-05-joint-account` | Either-to-sign, closure, delegate access, survivorship. Accounts domain only. |

---

## Conventions

- AC IDs: `AC-A-NNN` (three-digit, sequential, never reused).
- Status: **approved** (signed off, in corpus) or **proposed** (in a run, not yet merged).
- Every AC cites at least one regulatory or business anchor from `regulatory-anchors.md`.
- Negative cases included where meaningful — "X can do Y" almost always implies "Z cannot."
- New use cases added to the registry table above when a run opens, not when it closes.

---

## How to add a use case or AC

Use cases are registered (in the table above) when a run opens. ACs are added only through the run process:

1. A run produces proposed ACs in `runs/<run-name>/02-ac.md`, status: `proposed`.
2. The domain SME reviews and signs off.
3. On run merge, proposed ACs are appended here with status: `approved` and a back-link to the originating run. Use case status in the registry table flips to `Approved`.

Direct edits are reserved for typo fixes, anchor updates, and status changes (e.g., deprecation).

---

## UC-A-001 — Joint Current Account: Access and Delegation Baseline

> Source run: `runs/2026-05-joint-account` | Merged: 2026-05-13 | AC count: 20

### Group 1: Everyday Either-to-Sign Access

**AC-A-001** — A joint account holder can view balances, transactions, and account documents on the account without the other holder's consent. `account#holder` → `can_view, can_view_documents, can_view_payments` → allow (not blocked). Anchors: BCOBS, GDPR.

**AC-A-002** — A joint account holder can initiate payments on the account (can_transact) without the other holder's approval, provided the account is not in a blocked state. `account#holder` → `can_transact` → allow (not blocked). Anchors: PSD2, BCOBS.

**AC-A-003** — A joint account holder can cancel scheduled payments and standing orders on the account without the other holder's consent. `account#holder` → `can_cancel_scheduled` → allow (not blocked). Anchors: BCOBS, PSD2.

**AC-A-004** — A joint account holder can add, amend, and remove payees on the account without the other holder's consent. `account#holder` → `can_manage_payees` → allow (not blocked). Anchor: BCOBS.

**AC-A-005** — A joint account holder can freeze the account, and either holder can unfreeze the account independently — including unfreezing an account frozen by the other holder. `account#holder` → `can_freeze` → allow (not blocked). Anchors: FCA Consumer Duty, BCOBS.

**AC-A-006** — A joint account holder can grant third-party delegate access (View & Talk or View & Pay tier) to any named individual, without requiring the co-holder's consent. `account#holder` → `can_delegate` → allow (not blocked). Anchors: BCOBS, FCA Consumer Duty.

**AC-A-007** — Either joint account holder can revoke any delegate's access on the account, regardless of which holder originally granted that access. Revocation via DeleteRelationships; CHECK must use at_least_as_fresh(revokeZedToken). `account#holder` → `can_delegate` → allow (not blocked). Anchors: BCOBS, GDPR.

### Group 2: Account Closure

**AC-A-008** — A joint account holder can initiate an account closure request; the schema permits the can_close permission for any holder on a non-blocked account. Dual-consent enforcement is an application-layer concern, not schema-enforced. `account#holder` → `can_close` → allow (not blocked). Anchor: BCOBS.

### Group 3: Delegate Access on a Joint Account

**AC-A-009** — A View & Talk delegate on a joint account can view balances, transactions, and account documents; the scope is the full account (both holders' data), not a holder-scoped view. `account#delegate_view_talk` → `can_view, can_view_documents, can_view_payments` → allow. Anchors: BCOBS, GDPR.

**AC-A-010** — A user with no relation to a joint account is denied access on every permission check against that account. No relation → `can_view` → deny. Anchors: GDPR, BCOBS.

**AC-A-011** — A View & Talk delegate on a joint account cannot initiate payments (can_transact). `account#delegate_view_talk` → `can_transact` → deny. Anchors: PSD2, BCOBS.

**AC-A-012** — A View & Pay delegate on a joint account can initiate payments (can_transact) on a non-blocked account. `account#delegate_view_pay` → `can_transact` → allow (not blocked). Anchors: PSD2, BCOBS.

### Group 4: Bereavement State

**AC-A-013** — When a joint account enters bereavement state (blocked@flag:bereavement), all write operations are denied for all subjects, including the surviving holder. Any subject → `can_transact, can_freeze, can_manage_payees, can_cancel_scheduled, can_close, can_delegate` → deny (blocked@flag:bereavement). Anchors: FCA Consumer Duty, BCOBS.

**AC-A-014** — When a joint account enters bereavement state, the surviving holder retains read access (can_view, can_view_documents, can_view_payments). `account#holder` (surviving) → `can_view, can_view_documents, can_view_payments` → allow (blocked@flag:bereavement). Anchors: FCA Consumer Duty, GDPR.

**AC-A-015** — After survivorship is confirmed — the deceased holder's account#holder relation is removed and the bereavement flag is cleared — the surviving holder regains full write access. CHECK with at_least_as_fresh(survivorshipZedToken). `account#holder` (sole surviving) → all permissions → allow. Anchors: BCOBS, FCA Consumer Duty.

### Group 5: Delegate Boundaries and Default-Deny

**AC-A-016** — A View & Talk delegate cannot cancel scheduled payments or standing orders on the account. `account#delegate_view_talk` → `can_cancel_scheduled` → deny. Anchor: PSD2.

**AC-A-017** — A View & Pay delegate cannot manage payees (add, amend, remove) on the account. `account#delegate_view_pay` → `can_manage_payees` → deny. Anchor: BCOBS.

**AC-A-018** — Neither a View & Talk nor a View & Pay delegate can freeze or unfreeze the account. `account#delegate_view_talk or delegate_view_pay` → `can_freeze` → deny. Anchor: BCOBS.

**AC-A-019** — A delegate (View & Talk or View & Pay) cannot grant or revoke delegate access on the account. `account#delegate_view_talk or delegate_view_pay` → `can_delegate` → deny. Anchors: BCOBS, FCA Consumer Duty.

**AC-A-020** — A delegate (View & Talk or View & Pay) cannot initiate account closure. `account#delegate_view_talk or delegate_view_pay` → `can_close` → deny. Anchor: BCOBS.
