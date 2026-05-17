---
run: runs/2026-05-joint-account
title: Joint Current Account — Access and Delegation Baseline (Accounts Domain)
domain: accounts
status: merged
opened: 2026-05-10
target_close: 2026-05-17
closed: 2026-05-13
---

# Run Card — Joint Current Account — Access and Delegation Baseline

> One-page record of the run. Status, signatories, key dates. Read this first when picking up a run.

## What this run is

This run defines the AuthZ baseline for the UK joint current account, scoped to the Accounts domain. It covers four distinct patterns from Emily Carter's BA brief: (1) everyday access under the either-to-sign model, where either holder acts independently for routine operations; (2) account closure, where either holder can initiate but both must consent before execution; (3) third-party delegate access on a joint account, including grant and revocation authority, and the scope of the delegate's account view; and (4) survivorship — the state transition from joint tenancy to sole account when one holder dies, including the intermediate bereavement state. Payments and cards integration are explicitly out of scope for this run; Emily's note is that those follow once this baseline is agreed. The run produces a PRD, a full AC corpus, runnable scenarios, and a schema handoff brief for the Tech Lead.

## Stakeholder brief (input)

> Source: Emily Carter, BA — Digital Products & Accounts. Email received 2026-05-10. Subject: "Joint Current Account — Access & Permissions Brief (Accounts Domain)"

```
Context
-------
A joint current account has two named holders. Both are legal co-owners. In the UK,
joint current accounts default to a joint tenancy structure — on the death of one holder,
the account passes to the survivor rather than into the deceased's estate. Both holders
are independently identity-verified and onboarded.

Everyday access — either holder acting independently
-----------------------------------------------------
Both holders should be able to:
  - View balances, transactions, and account documents
  - Initiate payments (Faster Payments, BACS, CHAPS)
  - Cancel scheduled payments and standing orders
  - Manage payees (add, amend, remove)
  - Freeze and unfreeze the account (e.g. lost card, suspected fraud)
  - Request statements and correspondence

Either holder acts alone — no approval from the second holder is needed for routine
activity. This is the "either-to-sign" model and it covers the vast majority of
day-to-day use.

Account closure
---------------
This is where it gets complicated. Legally, either holder CAN initiate closure —
but bank policy (and BCOBS good practice) says we should require both holders'
consent before executing a close on a joint account, given the irreversibility.
So: the schema should allow either holder to trigger the closure action, but the
application layer must collect both consents before actually closing.

Delegate access
---------------
Either holder can grant a named third party delegate access (View & Talk or
View & Pay tiers, same as sole accounts). The delegate relationship is granted by
one holder, but either holder can revoke it. We need to be clear about whether
a delegate on a joint account gets access to the full account or a holder-scoped
view — for now, I think full account view is the right call, but flag if that
creates a problem.

Survivorship
------------
When one holder dies, the standard UK joint tenancy rule applies: the account
passes to the surviving holder. Operationally, on notification of death:
  1. The deceased holder's access is blocked immediately
  2. The account enters a bereavement state (all writes blocked, reads allowed)
  3. Once survivorship is confirmed, the deceased holder's relation is removed
     and the surviving holder regains full access as a sole holder

Regulatory notes
----------------
  - FSCS deposit protection applies per person, so each holder is protected up to
    £85k separately on the same account. No authz implication but worth knowing.
  - BCOBS requires that both holders are clearly informed of each other's access
    rights at account opening — not an authz problem but compliance will ask.
  - PSD2 SCA applies to payments initiated by either holder independently.

Open questions I'm flagging for you
------------------------------------
  1. If one holder freezes the account, can the other holder unfreeze it
     independently? My instinct is yes (either-to-sign), but I want your view.
  2. Can either holder grant delegate access, or should it require both holders?
     Lean towards "either can grant" but document the risk.
  3. What happens to an existing delegate when the account enters bereavement state?
     Presumably their access is also blocked — confirm.
```

## Domain and SME

| Domain | SME | Sign-off status |
|---|---|---|
| accounts | Laksh | pending |

## Pipeline status

| Step | Specialist | Output | Status |
|---|---|---|---|
| 1 | Spec Writer | `01-prd.md` | signed-off |
| 2 | Rule Lister | `02-ac.md` | signed-off |
| 3 | Scenario Builder | `03-scenarios.md` | signed-off |
| 4 | Schema Handoff | `04-schema-handoff.md` | ready-for-tl |

## Decisions log

- **2026-05-10** — Run opened via triage from `2026-05-10-joint-account-ba-email.md`. Use case confirmed as new (ac-corpus is empty — first run in pipeline). Domain: accounts only. Payments and cards deferred per Emily's brief.
- **2026-05-13** — All open issues resolved. Decisions: freeze symmetry → either holder can unfreeze (either-to-sign); delegate grant → either holder can grant without co-holder consent (risk documented); delegate view scope → full account view (GDPR basis: joint account agreement); closure consent → async 14-day window (application-layer workflow, not schema); bereavement write boundary → all writes blocked including surviving holder payments. Skills 01–04 executed, 20 ACs approved, 10 scenarios approved, schema handoff issued. No schema changes required. AC merged into ac-corpus. Run status: merged. Matrix sync to follow.

## Open issues

- **Freeze symmetry** — If holder A freezes the account, can holder B unfreeze independently? Emily's instinct is yes (either-to-sign), but needs a confirmed decision before the Spec Writer can model the freeze permission correctly. Owner: Laksh to decide.
- **Delegate grant authority** — Either holder can grant delegate access, or must both consent? Emily leans "either can grant" but flags the risk. Needs a decision — this directly affects the delegate relation model and the revocation asymmetry story. Owner: Laksh to decide.
- **Delegate access during bereavement** — What happens to an existing delegate when the account enters bereavement state? Presumably blocked with all writes — but does the surviving holder retain the power to explicitly revoke or does the bereavement state block that action too? Emily assumes blocked; confirm and make explicit. Owner: Laksh / Emily to confirm.
- **Delegate account view scope** — Emily proposes full account view for delegates (not holder-scoped). This means a delegate appointed by one holder can see the other holder's transactions. GDPR legal basis question: does the non-appointing holder's consent matter? Needs a decision before Spec Writer can write the permission scope. Owner: Laksh + Legal.
- **Closure consent mechanism** — Emily says "both consents required" for closure but the mechanism is unspecified: synchronous (both online simultaneously), asynchronous (one initiates, second receives notification and confirms within a window), or time-limited request (lapses after X days). The schema must support whichever model is chosen. Owner: Emily / Product to decide.
- **Bereavement state write boundary** — Emily says "all writes blocked" during bereavement. Does this include the surviving holder initiating payments? If so, that is a very restrictive interim state — confirm the intended scope. Owner: Emily / Ops to clarify.
