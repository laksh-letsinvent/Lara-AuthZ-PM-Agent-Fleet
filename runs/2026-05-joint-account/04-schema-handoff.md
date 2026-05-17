---
id: SH-A-01
prd_id: PRD-A-01
ac_ids: [AC-A-001, AC-A-002, AC-A-003, AC-A-004, AC-A-005, AC-A-006, AC-A-007, AC-A-008, AC-A-009, AC-A-010, AC-A-011, AC-A-012, AC-A-013, AC-A-014, AC-A-015, AC-A-016, AC-A-017, AC-A-018, AC-A-019, AC-A-020]
domains: [accounts]
status: ready-for-tl
source_run: runs/2026-05-joint-account
last_updated: 2026-05-13
---

# Schema Handoff — UC-A-001: Joint Current Account Access and Delegation Baseline

## 1. What this is about

This handoff covers the authorisation baseline for UK joint current accounts in the Accounts domain. It is the first approved use case in the ac-corpus. The four patterns in scope: everyday either-to-sign access for both holders, account closure with dual-consent (schema-level vs application-layer distinction), third-party delegation on a joint account, and survivorship when one holder dies.

The good news: no schema changes are required. Every assertion in this use case is satisfied by `domains/accounts/schema-fragment.zed` v1 as it stands. This handoff is a verification brief, not a change request.

## 2. What must be achievable

From `runs/2026-05-joint-account/03-scenarios.md` (approved, 10 scenarios, 20 AC covered):

**Either-to-sign access (SC-A-001, SC-A-002):**
Both holders must be able to view all account data and perform all write operations (transact, manage payees, cancel scheduled, freeze/unfreeze) independently. No second-holder gate. Freeze symmetry: either holder can unfreeze an account frozen by the other — the schema does not track who froze it.

**Delegation (SC-A-003 through SC-A-005):**
Either holder can grant and revoke delegate access without co-holder consent. View & Talk delegates can read everything but write nothing. View & Pay delegates can transact and cancel scheduled payments; they cannot manage payees, freeze, grant further delegation, or close the account. Delegates cannot grant-on-grant.

**Account closure (SC-A-007):**
The schema permits `can_close` for any holder on a non-blocked account. Dual-consent (both holders must confirm before execution) is an application-layer constraint — it is not schema-enforced. The schema does not need to change to support this; the application workflow handles it.

**Bereavement state (SC-A-008, SC-A-010):**
Setting `blocked@flag:bereavement` on the account must deny all write operations for all subjects — including the surviving holder and active View & Pay delegates. Read access (`can_view`, `can_view_documents`, `can_view_payments`) must be preserved for the surviving holder throughout.

**Survivorship (SC-A-009):**
Removing the deceased holder's `account#holder` relation via `DeleteRelationships` and clearing the `blocked@flag:bereavement` relation must restore full write access to the surviving holder on a consistency-fresh check. The deceased holder's relation must have no residual effect after deletion.

## 3. Acceptance criteria

From `runs/2026-05-joint-account/02-ac.md` (approved).

AC count: 20
AC IDs: AC-A-001 through AC-A-020

ACs for TL attention:

- **AC-A-005** (freeze symmetry) — either holder can unfreeze regardless of who froze. The schema models `can_freeze` as a permission, not a stateful toggle. The application layer writes the freeze flag; the schema only gates who can trigger that write. Confirm this understanding is correct before the application-layer team builds the freeze flow.
- **AC-A-007** (revocation consistency) — `CheckPermission` after a delegate revocation must use `at_least_as_fresh(revokeZedToken)` where `revokeZedToken` is from the `DeleteRelationships` response. If the calling service does not implement this, revoked delegates can temporarily pass permission checks on stale reads.
- **AC-A-013 and AC-A-014** (bereavement) — write-gated permissions deny because `is_blocked = blocked` matches any flag value, including `bereavement`. Read permissions (`can_view` etc.) are not in the `- is_blocked` exclusion. This is the existing schema behaviour — confirm it holds for `flag:bereavement` specifically, as the `bereavement` flag value is new.
- **AC-A-015** (survivorship consistency) — the `CheckPermission` confirming restored access must use `at_least_as_fresh(survivorshipZedToken)` from the final `DeleteRelationships` call (the flag clear). Using a token from an earlier step is insufficient.

## 4. Known constraints

- **No schema changes required.** All 20 ACs are satisfied by the existing schema. If the TL finds otherwise during validation, the discrepancy should be flagged before any schema edit is made.
- **Bereavement flag value** — `flag:bereavement` is a new named flag value being introduced in practice, even if the `flag` definition and `blocked` relation already exist. The TL should confirm whether named flag values require explicit registration in the schema, or whether the `flag` type is open (any flag instance is valid). Current schema suggests the latter, but worth verifying.
- **Dual-consent is not in schema** — the `can_close` permission does not enforce two-holder consent. This is by design. If at any point there is a requirement to enforce dual-consent at the schema level (not application layer), the schema would need a `closure_requested_by` relation or similar. That is out of scope for this use case.
- **Delegate view scope is full-account** — the `viewer` permission includes `delegate_view_talk` and `delegate_view_pay` without any per-holder scoping. This is a deliberate design decision, not an oversight. A per-holder scoped view would require schema changes (e.g. `delegate_view_talk_for_alice` vs `delegate_view_talk_for_bob`) and is deferred.
- **Regulatory** — bereavement state transitions are a FCA Consumer Duty requirement. The schema must support the state in a first-class way (not a bespoke flag on a customer profile). The current design satisfies this.

## 5. Out of scope

- Payments domain integration — `can_transact` is the gate; Payments schema is a separate domain handoff.
- Cards — joint account card access is a Cards domain concern.
- PoA on a joint account — separate use case.
- Multi-holder quorum for any action other than closure.
- Executor/probate access — tenants-in-common survivorship pattern is deferred.
- Schema changes — none required for this use case.
- Automatic flag clearing — the bereavement flag and relation deletion are operational system actions triggered by the bereavement team; schema does not model the trigger.

## 6. Open questions for TL

1. **Flag value registration** — does `flag:bereavement` need to be declared anywhere in the schema, or is the `flag` type open to any named instance? If it requires explicit registration, what is the pattern?
2. **Revocation ZedToken propagation** — what is the recommended pattern for passing the `revokeZedToken` from the Entitlements service to the calling service (e.g. mobile app, web channel), so that the calling service can enforce consistency on the next permission check? Is this a response header, a session token update, or another mechanism?
3. **Write flag on freeze** — when the application layer sets a `freeze` flag on the account (via a WriteRelationships call), does it write `account:X#blocked@flag:frozen` using the same `blocked` relation and `flag` type? Or is freeze modelled differently? The scenario assumes the former, but the schema fragment only defines the relation type, not specific flag values.

## 7. Sign-off

| Gate | Owner | Status |
|---|---|---|
| PM (scenarios + AC complete) | Laksh | signed-off |
| TL acknowledged | TBD | pending |
| Schema design complete | TBD | pending — no changes expected; validation only |
