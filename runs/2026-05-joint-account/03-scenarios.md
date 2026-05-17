---
run: runs/2026-05-joint-account
prd_id: PRD-A-01
domains: [accounts]
schema_state: v1 (domains/accounts/schema-fragment.zed — no new schema elements required)
status: approved
ac_coverage_target: 20
ac_ids_covered: [AC-A-001, AC-A-002, AC-A-003, AC-A-004, AC-A-005, AC-A-006, AC-A-007, AC-A-008, AC-A-009, AC-A-010, AC-A-011, AC-A-012, AC-A-013, AC-A-014, AC-A-015, AC-A-016, AC-A-017, AC-A-018, AC-A-019, AC-A-020]
last_updated: 2026-05-13
---

# Scenarios — UC-A-001: Joint Current Account Access and Delegation Baseline

All 20 ACs are covered across 10 scenarios. No SCHEMA-NEEDED flags — the existing accounts schema fragment covers all assertions in this use case without modification.

---

## Setup state

```
PEOPLE:
  alice   — joint holder A on ca_joint_001 (has account#holder relation)
  bob     — joint holder B on ca_joint_001 (has account#holder relation)
  carol   — View & Talk delegate on ca_joint_001 (account#delegate_view_talk)
  dave    — View & Pay delegate on ca_joint_001 (account#delegate_view_pay)
  nobody  — no relation to any account

ACCOUNTS:
  ca_joint_001  — joint current account (alice + bob both hold account#holder)
  flag:bereavement — flag definition used to set blocked state

INITIAL RELATIONS:
  WRITE account:ca_joint_001#holder@user:alice
  WRITE account:ca_joint_001#holder@user:bob
  WRITE account:ca_joint_001#delegate_view_talk@user:carol
  WRITE account:ca_joint_001#delegate_view_pay@user:dave
```

---

## Scenarios

### 1. SC-A-001 — JOINT-EQUALITY: Both holders have symmetric read access [Accounts]

```yaml
id: SC-A-001
ac_ids: [AC-A-001]
domains: [accounts]
type: positive
narrative: |
  Alice and Bob hold ca_joint_001 jointly. Either-to-sign means both have independent,
  equal read access — no second-holder gate. This scenario confirms the symmetric baseline:
  both can view balances and transaction history without consulting each other. The account
  is in a normal (non-blocked) state.
```

**Operations**

```
CHECK user:alice  account:ca_joint_001  can_view              → ALLOW
CHECK user:alice  account:ca_joint_001  can_view_documents    → ALLOW
CHECK user:alice  account:ca_joint_001  can_view_payments     → ALLOW
CHECK user:bob    account:ca_joint_001  can_view              → ALLOW
CHECK user:bob    account:ca_joint_001  can_view_documents    → ALLOW
CHECK user:bob    account:ca_joint_001  can_view_payments     → ALLOW
```

**Expected pattern:** Joint holders are symmetric. No principal is elevated over the other on read operations.

---

### 2. SC-A-002 — EITHER-TO-SIGN WRITES: Both holders transact and manage payees independently [Accounts]

```yaml
id: SC-A-002
ac_ids: [AC-A-002, AC-A-003, AC-A-004, AC-A-005]
domains: [accounts]
type: positive
narrative: |
  Under the either-to-sign model, both holders can initiate payments, cancel scheduled
  payments, manage payees, and freeze/unfreeze the account independently. Alice freezes
  the account; Bob, acting independently later, unfreezes it — demonstrating that
  freeze symmetry is bidirectional. No write requires the other holder's involvement.
```

**Operations**

```
CHECK user:alice  account:ca_joint_001  can_transact          → ALLOW
CHECK user:alice  account:ca_joint_001  can_cancel_scheduled  → ALLOW
CHECK user:alice  account:ca_joint_001  can_manage_payees     → ALLOW
CHECK user:alice  account:ca_joint_001  can_freeze            → ALLOW
CHECK user:bob    account:ca_joint_001  can_transact          → ALLOW
CHECK user:bob    account:ca_joint_001  can_cancel_scheduled  → ALLOW
CHECK user:bob    account:ca_joint_001  can_manage_payees     → ALLOW
CHECK user:bob    account:ca_joint_001  can_freeze            → ALLOW  ← bob can unfreeze even if alice froze
```

**Expected pattern:** All write permissions in writer_base are available to both holders on an unblocked account. Freeze/unfreeze is symmetric — the account does not track who froze it at the schema level.

---

### 3. SC-A-003 — DELEGATE GRANT AND REVOKE: Either holder can grant and revoke delegate access [Accounts]

```yaml
id: SC-A-003
ac_ids: [AC-A-006, AC-A-007]
domains: [accounts]
type: positive
narrative: |
  Bob grants Carol view-and-talk access. Alice, acting independently, later revokes it.
  This demonstrates that grant and revoke authority is symmetric — neither holder needs
  the other's involvement. The revocation uses a ZedToken to ensure consistency.
```

**Operations**

```
CHECK user:bob    account:ca_joint_001  can_delegate          → ALLOW  ← bob can grant
CHECK user:alice  account:ca_joint_001  can_delegate          → ALLOW  ← alice can revoke (same permission)
```

**Revocation consistency posture:**

```
DELETE account:ca_joint_001#delegate_view_talk@user:carol
  → returns revokeZedToken

CHECK user:carol  account:ca_joint_001  can_view
  WITH consistency: at_least_as_fresh(revokeZedToken)          → DENY  ← confirmed revoked
```

**Expected pattern:** can_delegate = holder. Both holders hold this permission. Revocation is immediate on a consistency-fresh check.

---

### 4. SC-A-004 — DELEGATE BOUNDARIES (V&T): View & Talk is read-only [Accounts]

```yaml
id: SC-A-004
ac_ids: [AC-A-009, AC-A-011, AC-A-016, AC-A-018, AC-A-019, AC-A-020]
domains: [accounts]
type: negative
narrative: |
  Carol has delegate_view_talk on ca_joint_001. She can see everything on the account —
  both holders' transactions, documents, balance — but cannot take any write action.
  She cannot transact, cancel scheduled payments, freeze, grant further delegate access,
  or initiate closure. The boundary is sharp: read yes, write no.
```

**Operations**

```
CHECK user:carol  account:ca_joint_001  can_view              → ALLOW
CHECK user:carol  account:ca_joint_001  can_view_documents    → ALLOW
CHECK user:carol  account:ca_joint_001  can_view_payments     → ALLOW
CHECK user:carol  account:ca_joint_001  can_contact_bank      → ALLOW
CHECK user:carol  account:ca_joint_001  can_transact          → DENY
CHECK user:carol  account:ca_joint_001  can_cancel_scheduled  → DENY
CHECK user:carol  account:ca_joint_001  can_manage_payees     → DENY
CHECK user:carol  account:ca_joint_001  can_freeze            → DENY
CHECK user:carol  account:ca_joint_001  can_delegate          → DENY
CHECK user:carol  account:ca_joint_001  can_close             → DENY
```

**Expected pattern:** delegate_view_talk is in viewer (reads allowed) but not in writer_base, not in can_freeze, not in can_delegate, not in can_close derivation. Every write is denied.

---

### 5. SC-A-005 — DELEGATE BOUNDARIES (V&P): View & Pay adds transact, not payee management [Accounts]

```yaml
id: SC-A-005
ac_ids: [AC-A-012, AC-A-017, AC-A-018, AC-A-019, AC-A-020]
domains: [accounts]
type: positive
narrative: |
  Dave has delegate_view_pay on ca_joint_001. He can do everything Carol can, plus initiate
  payments and cancel scheduled payments. He cannot manage payees, freeze the account,
  grant delegate access, or initiate closure. The distinction between V&T and V&P is
  exactly one step: payment initiation capability.
```

**Operations**

```
CHECK user:dave  account:ca_joint_001  can_view              → ALLOW
CHECK user:dave  account:ca_joint_001  can_transact          → ALLOW
CHECK user:dave  account:ca_joint_001  can_cancel_scheduled  → ALLOW
CHECK user:dave  account:ca_joint_001  can_manage_payees     → DENY
CHECK user:dave  account:ca_joint_001  can_freeze            → DENY
CHECK user:dave  account:ca_joint_001  can_delegate          → DENY
CHECK user:dave  account:ca_joint_001  can_close             → DENY
```

**Expected pattern:** delegate_view_pay is in writer_base (transact, cancel_scheduled allowed) but not in can_manage_payees, can_freeze, can_delegate, or can_close. Payee management is holder+ only.

---

### 6. SC-A-006 — DEFAULT DENY: No relation means no access [Accounts]

```yaml
id: SC-A-006
ac_ids: [AC-A-010]
domains: [accounts]
type: negative
narrative: |
  Nobody has no relation to ca_joint_001. Every permission check returns DENY.
  This scenario asserts the structural default-deny property of the Zanzibar model —
  no relation means no permission, with no fallback or default-allow path.
```

**Operations**

```
CHECK user:nobody  account:ca_joint_001  can_view              → DENY
CHECK user:nobody  account:ca_joint_001  can_transact          → DENY
CHECK user:nobody  account:ca_joint_001  can_close             → DENY
CHECK user:nobody  account:ca_joint_001  can_delegate          → DENY
```

**Expected pattern:** Zanzibar structural default-deny. No relation, no permission. No subject type is exempt.

---

### 7. SC-A-007 — ACCOUNT CLOSURE: Either holder can initiate; schema permits the action [Accounts]

```yaml
id: SC-A-007
ac_ids: [AC-A-008, AC-A-020]
domains: [accounts]
type: positive
narrative: |
  Either holder can pass the can_close schema check on a non-blocked account. The schema
  permits the action for holders — the dual-consent workflow is enforced at the application
  layer, not here. Carol and Dave as delegates are denied. This scenario draws a clean
  boundary: can_close is holder-only.
```

**Operations**

```
CHECK user:alice  account:ca_joint_001  can_close  → ALLOW
CHECK user:bob    account:ca_joint_001  can_close  → ALLOW
CHECK user:carol  account:ca_joint_001  can_close  → DENY
CHECK user:dave   account:ca_joint_001  can_close  → DENY
```

**Expected pattern:** can_close = holder - is_blocked. Delegates are not holders. Application layer is responsible for the dual-consent gate before execution.

---

### 8. SC-A-008 — BEREAVEMENT STATE: All writes blocked; surviving holder reads preserved [Accounts]

```yaml
id: SC-A-008
ac_ids: [AC-A-013, AC-A-014]
domains: [accounts]
type: state-transition
narrative: |
  The bank is notified that Alice has died. The bereavement team sets the blocked flag on
  ca_joint_001. From this point, all write operations are denied for all subjects — including
  Bob (the surviving holder) and Dave (View & Pay delegate). Bob retains read access throughout.
  Carol's read access is also preserved. The bereavement state is a total write block.
```

**Setup**

```
WRITE account:ca_joint_001#blocked@flag:bereavement
  → returns bereavementZedToken
```

**Operations** *(all checked with at_least_as_fresh(bereavementZedToken))*

```
CHECK user:bob   account:ca_joint_001  can_transact          → DENY   ← surviving holder blocked for writes
CHECK user:bob   account:ca_joint_001  can_freeze            → DENY
CHECK user:bob   account:ca_joint_001  can_manage_payees     → DENY
CHECK user:bob   account:ca_joint_001  can_cancel_scheduled  → DENY
CHECK user:bob   account:ca_joint_001  can_delegate          → DENY
CHECK user:bob   account:ca_joint_001  can_close             → DENY
CHECK user:dave  account:ca_joint_001  can_transact          → DENY   ← V&P delegate blocked for writes
CHECK user:bob   account:ca_joint_001  can_view              → ALLOW  ← surviving holder retains read
CHECK user:bob   account:ca_joint_001  can_view_payments     → ALLOW
CHECK user:carol account:ca_joint_001  can_view              → ALLOW  ← V&T delegate retains read
```

**Expected pattern:** is_blocked = blocked (any flag). All write-gated permissions deny. Read permissions (can_view etc.) are not gated by is_blocked and are preserved.

---

### 9. SC-A-009 — SURVIVORSHIP: Full access restored after relation deletion and flag clear [Accounts]

```yaml
id: SC-A-009
ac_ids: [AC-A-015]
domains: [accounts]
type: state-transition
narrative: |
  Survivorship is confirmed. The bereavement team removes Alice's holder relation and
  clears the bereavement flag. Bob is now the sole holder. This scenario confirms that
  full write access is restored — the sequence of operations and consistency posture are
  explicit, as this is an irreversible account state change.
```

**Setup** *(continuing from SC-A-008 — bereavement flag already set)*

```
DELETE account:ca_joint_001#holder@user:alice       ← deceased holder's relation removed
  → returns deleteAliceZedToken

DELETE account:ca_joint_001#blocked@flag:bereavement  ← bereavement flag cleared
  → returns survivorshipZedToken
```

**Operations** *(all checked with at_least_as_fresh(survivorshipZedToken))*

```
CHECK user:bob   account:ca_joint_001  can_view              → ALLOW
CHECK user:bob   account:ca_joint_001  can_transact          → ALLOW
CHECK user:bob   account:ca_joint_001  can_manage_payees     → ALLOW
CHECK user:bob   account:ca_joint_001  can_freeze            → ALLOW
CHECK user:bob   account:ca_joint_001  can_delegate          → ALLOW
CHECK user:bob   account:ca_joint_001  can_close             → ALLOW
CHECK user:alice account:ca_joint_001  can_view              → DENY   ← Alice's relation is gone
```

**Expected pattern:** After holder relation deletion and flag clear, sole surviving holder has full access. Deceased holder's relation is fully expunged — no residual access on a consistency-fresh check.

---

### 10. SC-A-010 — V&P BLOCKED DURING BEREAVEMENT: Write-capable delegate loses write access [Accounts]

```yaml
id: SC-A-010
ac_ids: [AC-A-013]
domains: [accounts]
type: state-transition
narrative: |
  Dave is a View & Pay delegate who could previously transact. When the account enters
  bereavement state, Dave's transact permission is blocked along with all other writes.
  This scenario specifically tests the delegate write block during bereavement — it is
  the edge case where an active V&P delegation meets a state transition.
```

**Setup**

```
(Account has: alice#holder, bob#holder, dave#delegate_view_pay, flag:bereavement already set from SC-A-008)
```

**Operations** *(with at_least_as_fresh(bereavementZedToken))*

```
CHECK user:dave  account:ca_joint_001  can_transact          → DENY
CHECK user:dave  account:ca_joint_001  can_view              → ALLOW  ← read still permitted
```

**Expected pattern:** V&P is in writer_base, but writer_base - is_blocked = deny when blocked. The delegate does not escape the state block by having a write relation — is_blocked applies to all write-gated permissions regardless of subject type.
