---
domain: customer-mgmt
sme: TBD
last_reviewed: 2026-04-29
status: stub — not yet populated
---

# Customer Management Domain (stub)

Not populated in v1. Shape mirrors `domains/accounts/`:

```
domains/customer-mgmt/
├── README.md
├── ac-corpus.md             ← use case registry + approved AC (populated by merging runs)
├── schema-fragment.zed
├── regulatory-anchors.md
```

## What this domain will own

- Profile permissions: `can_view_own`, `can_update_own`, `can_view_first_party`, `can_update_first_party`.
- KYC permissions: `can_complete_kyc`, `can_view_kyc`.
- Beneficiary management: `can_manage_beneficiary`.
- Vulnerability handling: `can_view_vulnerability`.
- The `customer_profile` definition.

## Distinctive constraint

This is the most data-sensitive domain. Two separation lines matter:

- **Own profile vs first-party profile.** A user can always view and update their *own* profile. Acting on someone else's profile (a donor under PoA, a customer under ops handling) requires explicit authority and is scope-bound.
- **Vulnerability information is internal.** `can_view_vulnerability` is ops-only by design. Whether the customer is entitled to know they've been flagged is an open question (see `domains/accounts/regulatory-anchors.md` Consumer Duty section).

## What this domain will not own

- The KYC verification process itself. CustMgmt only governs *who can perform / view* KYC.
- Profile data storage. That's a Customer service concern.

## Regulatory anchors expected

- GDPR / DPA 2018 (data subject rights, especially access and rectification).
- FCA Consumer Duty (vulnerable customer treatment).
- Mental Capacity Act 2005 (PoA scope on profile changes).
- AML/KYC obligations.

## When this gets populated

After v1 ships. The Customer Management SME copies the Accounts shape and populates. Worth pairing with Legal early — this domain has more regulatory surface than the others.
