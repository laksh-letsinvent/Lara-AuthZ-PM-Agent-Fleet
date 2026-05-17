---
domain: payments
sme: TBD
last_reviewed: 2026-04-29
status: stub — not yet populated
---

# Payments Domain (stub)

Not populated in v1. The shape this folder will take when filled is identical to `domains/accounts/`:

```
domains/payments/
├── README.md
├── ac-corpus.md             ← use case registry + approved AC (populated by merging runs)
├── schema-fragment.zed
├── regulatory-anchors.md
```

## What this domain will own

- Payment-specific permissions: `can_initiate`, `can_initiate_on_me`, `can_setup_payee`, `can_setup_direct_debit`, `can_cancel_standing_order`, `can_cancel_direct_debit`, `can_modify_limits`, `can_approve`, `can_approve_3ds`.
- Payment-specific caveats: `payment_limit` (delegate transaction caps).
- The `payment` definition that derives most of its permissions from `account` via the `source_account` relation.

## What this domain will not own

- `account#can_transact` — that's the gate. It lives in `domains/accounts/`.
- Card-level permissions on the funding card. Lives in `domains/cards/`.
- Notification routing for payment events. Lives in `domains/communications/`.

## Regulatory anchors expected

- PSD2 / PSR 2017 — SCA, Open Banking PISP scope.
- FCA payments rules.
- FATF travel rule (for relevant payment types).

## When this gets populated

After v1 ships and the framework is at work. The Payments SME copies the shape of `domains/accounts/`, populates use cases (e.g., maker-checker for high-value payments, scheduled payments, Open Banking PISP consent), and signs off.
