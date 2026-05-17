---
last_synced: 2026-05-13
approved_ac_count: 20
source_runs:
  - runs/2026-05-joint-account
open_issues: 3
---

# Entitlements Permission Matrix

20 approved ACs across 1 domain (Accounts). Last synced: 2026-05-13.

> **State note:** Cell values reflect the normal (non-blocked) account state. All write-gated permissions (`can_transact`, `can_cancel_scheduled`, `can_manage_payees`, `can_freeze`, `can_delegate`, `can_close`) return DENY for all subjects when the account has any blocked flag set (frozen, suspended, bereavement, dormant). Read permissions (`can_view`, `can_view_documents`, `can_view_payments`, `can_contact_bank`) are not gated by account state and remain in effect.
>
> **Column note:** This run distinguishes two delegate tiers — V&T (View & Talk, `account#delegate_view_talk`) and V&P (View & Pay, `account#delegate_view_pay`). Both are sub-types of the View Delegate relation. They are shown as separate columns because their permission sets differ materially.

---

## Subject key

| Column | Relation | Description |
|---|---|---|
| **Owner** | `account#owner` | Sole account holder or primary owner. No approved ACs in this run — column will populate when a sole-account baseline use case is run. |
| **Joint Holder** | `account#holder` | Either holder on a joint account. Symmetric — neither holder is elevated over the other. |
| **View Delegate (V&T)** | `account#delegate_view_talk` | Third party granted View & Talk access. Read-only + contact bank. |
| **View Delegate (V&P)** | `account#delegate_view_pay` | Third party granted View & Pay access. Read + payment initiation + cancel scheduled. |
| **PoA Attorney** | `account#attorney` | Holder of a registered Power of Attorney. No approved ACs in this run — column will populate when the PoA use case is run. |
| **Ops Internal** | `account#ops_agent` | Internal operations staff, subject to `ops_consent` caveat. No approved ACs in this run. |

## Cell key

| Symbol | Meaning |
|---|---|
| `✓` | Allow — approved AC asserts `expected: allow` for this subject × action |
| `✗` | Deny — approved AC asserts `expected: deny` |
| `~` | Conditional — approved AC asserts `expected: conditional`; condition in Notes |
| `—` | Not defined — no approved AC for this pair |
| `?` | Conflict — approved ACs contradict each other; see Open Issues |
| `⚠️` suffix | Schema mismatch — permission not found in schema fragment; see Open Issues |

---

## ACCOUNTS

> Schema: `domains/accounts/schema-fragment.zed` v1
> Use case corpus: `domains/accounts/ac-corpus.md`

### UC-A-001 — Joint Current Account: Access and Delegation Baseline

| Action | Schema permission | Owner | Joint Holder | View Delegate (V&T) | View Delegate (V&P) | PoA Attorney | Ops Internal | Notes |
|---|---|---|---|---|---|---|---|---|
| View balance & transactions | `can_view`, `can_view_payments` | — | ✓<!-- AC-A-001 --> | ✓<!-- AC-A-009 --> | —¹ | — | — | Full account view; both holders' transactions visible to delegates |
| View account documents | `can_view_documents` | — | ✓<!-- AC-A-001 --> | ✓<!-- AC-A-009 --> | —¹ | — | — | |
| Initiate payments | `can_transact` | — | ✓<!-- AC-A-002 --> | ✗<!-- AC-A-011 --> | ✓<!-- AC-A-012 --> | — | — | V&P requires SCA; holder does not require co-holder approval |
| Cancel scheduled payments | `can_cancel_scheduled` | — | ✓<!-- AC-A-003 --> | ✗<!-- AC-A-016 --> | —² | — | — | |
| Manage payees (add / amend / remove) | `can_manage_payees` | — | ✓<!-- AC-A-004 --> | —³ | ✗<!-- AC-A-017 --> | — | — | Holder-level and above only; V&P explicitly denied |
| Freeze / unfreeze account | `can_freeze` | — | ✓<!-- AC-A-005 --> | ✗<!-- AC-A-018 --> | ✗<!-- AC-A-018 --> | — | — | Either holder can unfreeze regardless of who froze |
| Grant delegate access | `can_delegate` | — | ✓<!-- AC-A-006 --> | ✗<!-- AC-A-019 --> | ✗<!-- AC-A-019 --> | — | — | Either holder can grant; no co-holder consent required |
| Revoke delegate access | `can_delegate` (DeleteRelationships) | — | ✓<!-- AC-A-007 --> | ✗<!-- AC-A-019 --> | ✗<!-- AC-A-019 --> | — | — | Either holder can revoke any delegate; use `at_least_as_fresh(revokeZedToken)` |
| Close account | `can_close` | — | ✓<!-- AC-A-008 --> | ✗<!-- AC-A-020 --> | ✗<!-- AC-A-020 --> | — | — | Schema permits; dual-consent (both holders) enforced at application layer |

> ¹ V&P inherits viewer via schema (`delegate_view_pay` is in `viewer` derivation), but no approved AC explicitly asserts V&P × can_view → allow. See Open Issues.
> ² Schema includes `delegate_view_pay` in `can_cancel_scheduled` derivation, but no approved AC explicitly asserts V&P × can_cancel_scheduled → allow. See Open Issues.
> ³ V&T is not in `can_manage_payees` derivation; deny follows from schema, but no explicit AC. See Open Issues.

---

## PAYMENTS

> Status: stub — no approved ACs. Payments schema fragment not yet populated.
> Domain corpus: `domains/payments/` — not yet populated.

| Action | Schema permission | Owner | Joint Holder | View Delegate (V&T) | View Delegate (V&P) | PoA Attorney | Ops Internal | Notes |
|---|---|---|---|---|---|---|---|---|
| *(No approved ACs)* | | — | — | — | — | — | — | Payments use cases are blocked on Accounts baseline. This run establishes `can_transact` as the accounts-domain gate that Payments will derive from. |

---

## CARDS

> Status: stub — no approved ACs. Cards schema fragment not yet populated.

| Action | Schema permission | Owner | Joint Holder | View Delegate (V&T) | View Delegate (V&P) | PoA Attorney | Ops Internal | Notes |
|---|---|---|---|---|---|---|---|---|
| *(No approved ACs)* | | — | — | — | — | — | — | Cards domain deferred post-accounts baseline. |

---

## COMMUNICATIONS

> Status: stub — no approved ACs.

| Action | Schema permission | Owner | Joint Holder | View Delegate (V&T) | View Delegate (V&P) | PoA Attorney | Ops Internal | Notes |
|---|---|---|---|---|---|---|---|---|
| *(No approved ACs)* | | — | — | — | — | — | — | |

---

## CUSTOMER MANAGEMENT

> Status: stub — no approved ACs.

| Action | Schema permission | Owner | Joint Holder | View Delegate (V&T) | View Delegate (V&P) | PoA Attorney | Ops Internal | Notes |
|---|---|---|---|---|---|---|---|---|
| *(No approved ACs)* | | — | — | — | — | — | — | |

---

## Open Issues

*Generated by matrix-sync on 2026-05-13. Requires PM review.*

### Conflicts (? cells)

None.

### Schema mismatches (⚠️ cells)

None. All permission names in UC-A-001 ACs exist in `domains/accounts/schema-fragment.zed`.

### Notable coverage gaps (— cells worth discussing)

| Subject × Action | Why it matters | Suggested next run scope |
|---|---|---|
| View Delegate (V&P) × `can_view` | V&P is in `viewer` derivation (schema permits), but no AC explicitly asserts this. The matrix shows — despite the schema allowing it. | Add V&P read ACs to a follow-on accounts use case or as addenda to UC-A-001. |
| View Delegate (V&P) × `can_cancel_scheduled` | V&P is in `can_cancel_scheduled` derivation, but no explicit AC. Same gap as above. | Same. |
| View Delegate (V&T) × `can_manage_payees` | V&T is not in the derivation (deny follows from schema), but no AC explicitly asserts the deny. | Add to follow-on run. |
| Owner × all actions | No sole-account baseline use case has been run yet. The Owner column is entirely — . Every cell is a design decision not yet formalised in the corpus. | Run a sole-account baseline use case to populate this column. |
| PoA Attorney × all actions | PoA use case is documented in the delegation use cases knowledge base but has not been run through the pipeline. The corpus has no attorney ACs. | PoA use case is the logical next run after sole-account baseline. |
| Ops Internal × all actions | `ops_agent` with `ops_consent` caveat appears in the schema (can_view, some write permissions) but no AC has been written. Ops access during bereavement (question raised in PRD-A-01 section 11) is an open item. | Write Ops access use case or add ops ACs as addenda to existing use cases. |
| Bereavement state row | Bereavement write-block is asserted in AC-A-013/014/015 but the matrix doesn't show a separate state row. The current format collapses normal-state and blocked-state into one cell. For stakeholder readability, a future matrix version could add a conditional row showing `✗ (blocked)` for all write permissions. | Consider a matrix format extension when more use cases land. |
