---
domain: cards
sme: TBD
last_reviewed: 2026-04-29
status: stub — not yet populated
---

# Cards Domain (stub)

Not populated in v1. Shape mirrors `domains/accounts/`:

```
domains/cards/
├── README.md
├── ac-corpus.md             ← use case registry + approved AC (populated by merging runs)
├── schema-fragment.zed
├── regulatory-anchors.md
```

## What this domain will own

- Card-specific permissions: `can_view_card`, `can_freeze_card`, `can_change_pin`, `can_change_controls`, `can_report_lost`, `can_request_replacement`, `can_set_card_limits`.
- The `card` definition that links to `account` via the `account` relation and to `user` via `cardholder`.
- Card state overrides (card-level `blocked` flag, distinct from account-level).

## What this domain will not own

- Card-funding payment authorisation. That's `payment` referencing `account#can_transact`.
- Cardholder identity verification. That's `customer-mgmt`.

## Distinctive constraint

Cards are 1:1 to people. Each holder on a joint account gets their own card entity. Permissions like `can_change_pin` are intentionally cardholder-only, not account-derived. Delegates and PoA see *the cardholder's* card details (with restrictions) but cannot change PIN. This isolation pattern is worth carrying forward when the SME populates this folder.

## Regulatory anchors expected

- PSD2 / PSR 2017 (cardholder authentication).
- Card scheme rules (Visa, Mastercard).
- FCA Consumer Duty (vulnerable cardholder considerations).

## When this gets populated

After v1 ships. Cards SME copies the Accounts shape and populates.
