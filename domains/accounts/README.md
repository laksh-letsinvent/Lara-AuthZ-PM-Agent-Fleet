---
domain: accounts
sme: Laksh (v1, solo) — to be assigned at port-to-work
last_reviewed: 2026-04-29
status: populated
---

# Accounts Domain

The anchor domain for the Entitlements platform. Every other domain (Payments, Cards, Communications, Customer Mgmt) derives its permissions from Accounts. If the Accounts model is wrong, everything downstream is wrong.

## What this domain owns

- All ownership models for retail accounts: sole, joint, trust-held, minor.
- All delegation tiers and their semantics: View & Talk, View & Pay, Power of Attorney.
- The state machine for account-level overrides: frozen, suspended, investigated, bereavement, dormant, former.
- The relations and permissions that other domains reference (`account#holder`, `account#can_transact`, `account#viewer` etc.).

## What this domain does not own

- Payment-specific permissions (lives in `domains/payments/`).
- Card-specific permissions (lives in `domains/cards/`).
- Communications routing (lives in `domains/communications/`).
- Customer profile and KYC (lives in `domains/customer-mgmt/`).

If a permission can be fully derived from a relation on `account`, it lives here. If it needs its own domain definition (e.g., `payment.can_initiate_on_me`), it lives in that domain and references `account` via relations.

## Files in this folder

| File | What it is |
|---|---|
| `ac-corpus.md` | Use case registry + approved AC grouped by use case. Single source of truth for what this domain promises. Populated by merging approved runs. |
| `schema-fragment.zed` | Source of truth for the Accounts portion of the SpiceDB schema. |
| `regulatory-anchors.md` | Regulations specific to retail account access and delegation. |

Note: `use-cases.md` no longer exists as a separate file. The use case registry lives at the top of `ac-corpus.md`.

## SME ownership note (for port-to-work)

When this framework moves to work, this domain gets a named SME — likely the Accounts product lead. Their responsibilities:

- Reviews and signs off on agent outputs scoped to this domain.
- Owns updates to `use-cases.md`, `schema-fragment.zed`, `regulatory-anchors.md`, and `ac-corpus.md`.
- Surfaces cross-domain dependencies to the Tech Lead and to other domain SMEs.

In v1, Laksh plays this role for all five domains.
