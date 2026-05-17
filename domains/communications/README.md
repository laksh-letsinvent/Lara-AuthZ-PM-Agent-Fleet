---
domain: communications
sme: TBD
last_reviewed: 2026-04-29
status: stub — not yet populated
---

# Communications Domain (stub)

Not populated in v1. Shape mirrors `domains/accounts/`:

```
domains/communications/
├── README.md
├── ac-corpus.md             ← use case registry + approved AC (populated by merging runs)
├── schema-fragment.zed
├── regulatory-anchors.md
```

## What this domain will own

- Communication-routing permissions: `can_view_account_comms`, `can_view_personal`, `can_send_message`, `can_initiate_case`, `can_configure_notifications`, `can_receive_notifications`.
- The `communication` definition that distinguishes account-level comms (statements, DD notifications) from personal comms (security alerts, identity verification challenges).

## Distinctive constraint

The personal vs account-level split is the structural decision in this domain. Account-level comms inherit from `account#can_view_documents` (broadly accessible). Personal comms are restricted to `personal_recipient` (the individual, no delegates, no PoA). This is the GDPR boundary between account data and personal data.

## What this domain will not own

- Notification preference storage (that's a service concern, not an entitlement concern).
- Account-level documents themselves — that's a Documents service. Comms only governs *who can see them*.

## Regulatory anchors expected

- GDPR / DPA 2018 (lawful basis, data subject rights).
- FCA Consumer Duty (clear, timely, accessible communications).
- BCOBS (statement and notification obligations).

## When this gets populated

After v1 ships. Communications SME — likely the customer-comms product lead — copies the Accounts shape and populates.

## Likely v1 pilot domain at port-to-work

Comms is the recommended starter for the first multi-domain run after this framework ports to work. Lower regulatory exposure than Payments, exercises delegation cleanly, surfaces the personal-vs-account-level distinction. If the pattern works on Comms, it works.
