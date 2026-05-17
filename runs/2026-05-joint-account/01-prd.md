---
id: PRD-A-01
use_case_id: UC-A-001
domains: [accounts]
status: approved
source_run: runs/2026-05-joint-account
last_updated: 2026-05-13
---

# PRD — Joint Current Account: Access and Delegation Baseline

## 1. Problem

Joint current accounts are the most common multi-party account structure at Lara Banks, covering a material share of the retail customer base. Today, the access rules for joint accounts are enforced through application-layer logic distributed across multiple services — there is no single authoritative record of who can do what, and the rules are inconsistently applied across channels (mobile, web, telephony). The four distinct patterns that need modelling — everyday either-to-sign access, account closure consent, third-party delegation on a joint account, and survivorship on death — are currently handled through a mix of role flags and bespoke workflow code with no shared permission model.

This PRD defines the authorisation baseline for these four patterns, scoped to the Accounts domain. Payments and cards integrations are explicitly deferred to subsequent runs.

## 2. Magnitude

Joint accounts represent a significant portion of Lara Banks' current account base. Every inbound contact about "why can't my partner do this" or "I'm trying to act on my husband's account" is a failure of this layer. The survivorship pattern carries direct regulatory exposure — failure to handle account state transition on bereavement is a recurring FCA supervisory focus. BCOBS requires clear disclosure of access rights at account opening; without a clear permission model, we can't generate that disclosure accurately.

Fixing this also unblocks the Open Banking delegation layer — joint account holder access is a prerequisite for AISP/PISP scoping on joint accounts under PSD2.

## 3. Subjects

This PRD introduces one changed relation and one new state, not new subject types. Both joint holders use the existing `account#holder` relation — the schema already supports this. The patterns below are about what that relation allows and when.

- **Joint holder** — `account#holder` (existing). Both holders on a joint account share this relation symmetrically. Neither holds `account#owner` unless one holds the account in a sole-owner capacity.
- **Third-party delegate** — `account#delegate_view_talk` and `account#delegate_view_pay` (existing). Delegate relations on joint accounts behave identically to sole accounts for most operations. The question of full-account vs. holder-scoped view is resolved below (full account view).
- **Bereavement state flag** — `blocked@flag:bereavement` (existing). A new flag value, applied when a holder's death is notified to the bank.

## 4. Resources

- **Account** (`account`). The joint current account.
- No new resource types. All actions in this PRD operate against the account resource directly.
- **Cross-domain dependency noted:** `can_transact` on the account is what the Payments domain gates on for payment initiation. That dependency exists already in the schema; this PRD does not change it.

## 5. Actions

**Either holder, acting alone:**

```
- View balances, transactions, account documents             → allow
- View account details (sort code, account number)          → allow
- Initiate payments (FPS, BACS, CHAPS)                      → allow
- Cancel scheduled payments and standing orders             → allow
- Manage payees (add, amend, remove)                        → allow
- Freeze / unfreeze the account                             → allow (either holder can unfreeze even if the other froze it)
- Grant third-party delegate access (V&T or V&P tier)       → allow (either holder can grant; risk documented in conditions)
- Revoke any delegate's access                              → allow (either holder can revoke)
- Request statements and correspondence                     → allow
```

**Closure — conditional:**

```
- Initiate account closure                                  → allow (schema level)
- Execute closure                                           → conditional — both holders' consent required (application-layer async flow; one initiates, other confirms within 14 days or request lapses)
```

**Opening a new account:**

```
- Open a new linked account                                 → allow (holder-only; schema permits either holder)
```

**During bereavement state (`blocked@flag:bereavement`):**

```
- All write operations (transact, freeze, payee mgmt, etc.) → deny (all subjects, including surviving holder)
- Read operations (view balance, transactions, documents)    → allow (surviving holder only; delegates blocked for writes per bereavement state)
- Surviving holder's read access                            → preserved (can_view is not gated by is_blocked)
```

**After survivorship confirmed:**

```
- Deceased holder's account#holder relation removed          → system action via DeleteRelationships
- Blocked flag cleared                                      → system action
- Surviving holder regains full sole-holder access          → restored to full permission set
```

## 6. Conditions and caveats

**Freeze symmetry** — Decision: either holder can freeze and either holder can independently unfreeze, regardless of who froze it. This is consistent with the either-to-sign model and avoids a deadlock scenario where one holder becomes unreachable.

**Delegate grant authority** — Decision: either holder can grant and either holder can revoke. Risk: a delegate appointed by one holder can see the other holder's full transaction history. This is accepted as the baseline; the bank's disclosure process at account opening must make this explicit (BCOBS obligation). The schema does not model per-holder data scoping — full account view is the starting point.

**Delegate view scope on joint accounts** — Full account view. A delegate appointed by one holder can see all transactions on the account (both holders' activity). The GDPR legal basis for the non-appointing holder's data being visible to the delegate is covered by the joint account agreement terms. This is not a schema design question; it is a terms question that legal has confirmed is adequate for v1.

**Account closure async consent** — One holder initiates (schema: `can_close = holder - is_blocked` is satisfied). The application layer captures this as a "closure pending" state, notifies the second holder, and requires their confirmation within 14 days. If the second holder does not confirm, the request lapses. The schema does not need to model this workflow — `can_close` remains holder-gated, and the application layer enforces the dual-consent step. A `SCHEMA-NEEDED` flag is raised in scenarios if this understanding is wrong.

**Bereavement write boundary** — All writes are blocked for all subjects (including surviving holder) during bereavement state. This is intentionally restrictive to protect the estate and prevent fraud in the immediate post-death period. The surviving holder retains read access. Ops access during bereavement is subject to the standard `ops_consent` caveat. Duration of bereavement state: until survivorship is confirmed by the bank's bereavement team — this is an operational timeline, not a schema concern.

**Delegate access during bereavement** — Existing delegates are effectively blocked for all write operations when the bereavement flag is set (is_blocked = true). Read access persists for `can_view` (not gated by is_blocked). The surviving holder must explicitly revoke delegate relations post-survivorship if they choose — bereavement state does not auto-expire delegate relations.

## 7. Regulatory anchors

- **BCOBS (Banking Conduct of Business Sourcebook)** — requires clear disclosure of access rights at account opening; requires a process for account state changes including death of a holder. Directly applies to the either-to-sign model and closure consent.
- **PSD2 / Payment Services Regulations 2017** — SCA applies to payment initiation. Both holders are independently authenticated and can initiate independently under the either-to-sign model.
- **GDPR / Data Protection Act 2018** — delegate view of a joint account covers both holders' financial data. Legal basis is the joint account agreement. Data subject rights (access, rectification) persist for both holders independently.
- **FCA Consumer Duty (PRIN 2A)** — bereavement handling is a specific area of FCA supervisory focus. First-class bereavement state with clear documented effects is required.
- **FSCS** — per-person deposit protection; both holders are independently protected up to the relevant limit. Schema does not model this, but holder count is relevant.

## 8. Success criteria

- Both holders on `ca_002` (joint account) can view balances and initiate payments independently — no second-holder gate on routine operations.
- Either holder can grant `delegate_view_talk` to a third party; either holder can revoke it. The delegate can view but not transact. A View & Pay delegate can transact.
- Setting `blocked@flag:bereavement` on the account denies all write operations for all subjects, including holders and delegates, while preserving read access for the surviving holder.
- After removing the deceased holder's `account#holder` relation and clearing the blocked flag, the surviving holder has full sole-holder access including all write operations.
- A subject with no relation to the account is denied access on every permission check.

## 9. Out of scope

- **Payments domain integration** — `can_transact` enables payment initiation; the Payments domain PRD will define what initiation looks like end-to-end. This PRD does not touch Payments schema.
- **Cards** — joint account card ownership (`card:X#account@account:Y`) is a Cards domain concern. This PRD only covers account-level permissions.
- **PoA on a joint account** — joint account with an attorney acting for one holder is a complex pattern that requires its own run. Not modelled here.
- **Scottish Continuing PoA, Deputyship, Guardianship** — deferred to dedicated use cases.
- **Multi-holder quorum for any action other than closure** — either-to-sign governs all actions except closure.
- **PISP/AISP Open Banking consent model** — the Payments domain will model this. This PRD exposes the relations Open Banking will depend on.
- **Executor access post-probate** — survivorship covers the joint tenancy case (automatic transfer to survivor). Tenants-in-common (estate distribution to beneficiaries) and executor access are deferred.
- **FSCS deposit protection calculations** — not an authorisation concern.
- **Automatic trust deed parsing or digital death certificate processing** — both are operational/integration concerns, not schema.

## 10. Risks

- **Delegate grant without co-holder knowledge** — either holder can appoint a delegate who can then view all transactions including the co-holder's. Risk is mitigated by BCOBS disclosure at account opening, but the non-appointing holder has no in-app visibility of delegates they didn't appoint. Flagged for CX to consider a joint account delegate notifications pattern in a subsequent run.
- **Bereavement state duration risk** — if the bereavement state persists too long before survivorship is confirmed, the surviving holder is unable to transact. Operations SLA for survivorship confirmation needs to be short. Not a schema risk but worth flagging to the bereavement ops team.
- **Delegate relation persistence post-bereavement** — after survivorship, existing delegates remain unless explicitly revoked. The surviving holder inherits a delegate set they may not have appointed. This is intentional (revocation is their choice) but requires clear disclosure.
- **Closure lapse period** — the 14-day async consent window creates a "closure pending" UX state. The schema does not enforce this; if the application layer fails to honour it, either holder could complete closure unilaterally. Mitigation: application-layer workflow gate is a requirement, not a nice-to-have.

## 11. Open questions

- **Closure async mechanism** — resolved: asynchronous, 14-day window, lapses if second holder doesn't confirm. This needs product and ops alignment on the UX and the SLA.
- **Delegate notifications for non-appointing holder** — should the co-holder receive a notification when a delegate is appointed by the other holder? Not a schema question, but relevant for CX design. Flagged as an open item for the UX team.
- **Ops access during bereavement for compliance/fraud** — `ops_agent` with `ops_consent` should be able to act during bereavement for fraud investigation purposes. Is `ops_consent` adequate, or does bereavement require a separate ops escalation caveat? Worth confirming with the fraud and bereavement operations teams before the AC are finalised.
