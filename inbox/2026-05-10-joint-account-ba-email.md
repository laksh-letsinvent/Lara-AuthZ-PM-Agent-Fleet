---
received: 2026-05-10
from: Emily Carter, BA — Digital Products & Accounts
format: email
status: pending-triage
---

From: Emily Carter <e.carter@larabanks.com>
To: Laksh <l.singhal@larabanks.com>
Date: 10 May 2026
Subject: Joint Current Account — Access & Permissions Brief (Accounts Domain)

Hi Laksh,

Following our session last week, I've put together the access requirements for the
UK joint current account. This is Accounts domain only for now — payments and cards
integration to follow once this baseline is agreed.

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

Happy to discuss. Aiming for first draft AC by end of next week.

Emily
