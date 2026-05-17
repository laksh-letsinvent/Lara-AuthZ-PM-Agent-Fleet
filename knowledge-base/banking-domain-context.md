> _Maintained copy for the agent fleet. Do not sync from `/knowledge` — that copy is archived._

# Banking Domain Context — Entitlements Consumers

> Reference for the retail banking domains that will consume the Entitlements platform. Use this to understand the business context when designing schemas, writing specs, or evaluating permission models.

---

## The Entitlements Platform and Its Consumers

The Entitlements platform provides fine-grained authorization (who can do what, on which resources, under which conditions) to the consuming domains at Lara Banks. It does not own these domains — it serves them. Each domain has its own product teams, its own regulatory obligations, and its own access patterns. The entitlements platform must be flexible enough to model all of them without becoming a bespoke solution for any single one.

The core question each domain asks the platform: **"Can this subject perform this action on this resource, given these conditions?"**

---

## Domain: Accounts

**What it covers:** Current accounts, savings accounts, fixed deposits, ISAs, joint accounts, minor accounts, trust accounts.

**Why it matters for entitlements:** Accounts are the anchor object in nearly every permission check. Most entitlements resolve to "can this person do X on this account?" The account domain also introduces the most complex ownership models — joint tenancy, tenants in common, sole proprietor, trust-held, and minor accounts with guardian access.

**Key access patterns:**

- View account balance and transaction history
- Initiate and approve transactions (payments, transfers)
- Modify account settings (alerts, limits, standing orders)
- Add or remove account holders (joint account management)
- Close or freeze an account
- Grant delegated access (Power of Attorney, third-party mandates)

**Permission model considerations:**

- Joint accounts need "either to sign" (OR logic) vs "both to sign" (AND logic) — this maps to union vs intersection in Zanzibar terms
- Account tiers may carry different permission scopes (basic current account vs premium)
- Dormant or frozen accounts should have a blanket deny that overrides other permissions
- Deceased holder accounts transition through a specific state machine (see Delegation Use Cases doc)

**Regulatory touchpoints:** FCA Consumer Duty (fair treatment of joint holders), FSCS deposit protection (per-person, not per-account), PSD2 (third-party access to account data via Open Banking)

---

## Domain: Payments

**What it covers:** Faster Payments, BACS, CHAPS, Direct Debits, standing orders, international transfers (SWIFT), Open Banking payment initiation.

**Why it matters for entitlements:** Payments are the highest-risk action a user can perform. Every payment initiation is an authorization event. The entitlements platform must answer "can this person initiate/approve/cancel this payment from this account?" with high confidence and low latency.

**Key access patterns:**

- Initiate a domestic payment (Faster Payments, BACS)
- Initiate a high-value payment (CHAPS — typically requires elevated permissions)
- Set up, modify, or cancel a Direct Debit
- Create, modify, or cancel a standing order
- Approve payments (dual-control / maker-checker for business accounts)
- Initiate international transfers
- Consent to Open Banking payment initiation (PISP flow)

**Permission model considerations:**

- Payment limits are contextual — they depend on who the user is (owner vs delegate), the payment type, and potentially the destination. Caveats are the right tool here.
- Maker-checker patterns require intersection logic: "user must have initiator permission AND a different user must have approver permission"
- Direct Debit mandates are long-lived permissions — a merchant gets ongoing permission to pull from an account. This is a relationship, not a one-off check.
- Open Banking PISPs need scoped, time-limited, consent-based access — a good fit for caveated relationships

**Regulatory touchpoints:** PSD2 Strong Customer Authentication (SCA), Payment Services Regulations 2017, FCA rules on unauthorised payment recovery, confirmation of payee requirements

---

## Domain: Cards

**What it covers:** Debit cards, credit cards, prepaid cards, virtual cards, card controls, card limits, PIN management.

**Why it matters for entitlements:** Cards are a distinct resource with their own permission model. A card is linked to an account but has independent controls — a user might be able to view their account but have their card frozen. Delegated users may have cards issued in their own name against the primary holder's account.

**Key access patterns:**

- View card details (masked PAN, expiry, CVV reveal)
- Activate/deactivate a card
- Set card spending limits (per-transaction, daily, monthly)
- Block/unblock a card (temporary freeze)
- Report card lost/stolen
- Request a replacement card
- Manage card controls (online transactions, contactless, ATM, international usage)
- View card transactions
- Manage supplementary cards (additional cardholders on the account)

**Permission model considerations:**

- Supplementary cardholders have card-level permissions but not necessarily account-level permissions — the entitlements model needs to distinguish card ownership from account ownership
- Card controls (online/offline, domestic/international) could be modelled as permissions or as resource attributes. The recommendation is to keep card controls in the card domain and use entitlements only for "can this user manage these controls?"
- Virtual cards may have shorter lifespans and narrower scopes (single-merchant, single-use) — caveated access fits here

**Regulatory touchpoints:** PCI-DSS (card data access), PSD2 SCA (card-not-present transactions), Consumer Credit Act (credit card-specific obligations)

---

## Domain: Communications

**What it covers:** Secure messaging, push notifications, email preferences, SMS alerts, marketing consent, in-app notifications, document delivery (statements, letters).

**Why it matters for entitlements:** Communications involve personal data and consent. The entitlements question here is less "can this person send a message?" and more "can this person see communications on this account?" — particularly relevant for joint accounts and delegated access.

**Key access patterns:**

- View secure messages for an account
- Send secure messages to the bank
- Manage notification preferences (which channels, which events)
- View delivered documents (e-statements, tax certificates)
- Manage marketing consent
- View communications history

**Permission model considerations:**

- Joint account holders may both need access to account-level communications, but individual-level communications (identity verification, personal security alerts) should be restricted to the specific user
- Delegated users (PoA holders) may need access to account communications but not personal communications — the model needs a clear distinction between "account comms" and "personal comms"
- GDPR consent for marketing is a separate concern from entitlements but interacts with it — a user who has withdrawn marketing consent shouldn't receive marketing, regardless of their account permissions

**Regulatory touchpoints:** GDPR (consent management, data subject access), ePrivacy Regulation, FCA Consumer Duty (clear communication obligations)

---

## Domain: Customer Management & Servicing

**What it covers:** Customer profile management, KYC data, address changes, contact details, identity verification status, vulnerability flags, complaints, service requests.

**Why it matters for entitlements:** This domain sits at the intersection of identity and authorization. Changing a customer's address or contact details has security implications. Viewing KYC data requires elevated permissions. Vulnerability flags affect how the bank interacts with the customer.

**Key access patterns:**

- View and update personal details (name, address, phone, email)
- View KYC/identity verification status
- Initiate re-verification (refresh KYC)
- View and manage linked accounts
- Raise and track service requests
- View and respond to complaints
- View vulnerability status (staff-side only)
- Manage beneficiary/nominee details

**Permission model considerations:**

- Personal data changes (address, contact info) should require the account holder themselves or a legally delegated person — not just any delegate
- KYC data is sensitive; access should be auditable and limited to the individual and authorised bank staff
- Delegated users may need to manage some servicing tasks (raising complaints, requesting statements) but not others (changing contact details, updating KYC)
- The distinction between "this delegate can do operational tasks" and "this delegate can change identity data" is critical

**Regulatory touchpoints:** GDPR (data subject rights, right to rectification), KYC/AML regulations (ongoing due diligence), FCA Vulnerable Customer guidelines, Data Protection Act 2018

---

## Cross-Domain Patterns

Several authorization patterns recur across all domains:

**1. Account-anchored permissions:** Most permissions resolve to "can user X do action Y on account Z?" The account is the central resource in the permission graph.

**2. Layered delegation:** A delegate might have different permission scopes across domains — full access on payments, read-only on cards, no access on customer management. The entitlements platform needs to support per-domain permission scoping on delegation.

**3. Contextual constraints:** Many actions have conditions attached — payment limits, time windows, IP restrictions, channel restrictions (branch-only vs digital). Caveats handle these.

**4. Audit requirements:** Every domain has regulatory audit obligations. The entitlements platform must support "who had access to what, when?" queries efficiently (LookupSubjects, ReadRelationships, Watch API).

**5. State-dependent access:** Account states (active, frozen, dormant, deceased-holder) override individual permissions. A frozen account should deny all write operations regardless of the user's relationships.

**6. Channel-specific permissions:** Some actions may only be permitted in certain channels (branch, online banking, mobile app, telephone banking). This is a contextual constraint, not a static permission.

---

## Domain Interaction Map

```
                    ┌──────────────┐
                    │  ENTITLEMENTS │
                    │   PLATFORM    │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼──────┐
    │  ACCOUNTS  │   │  PAYMENTS  │   │   CARDS    │
    │            │   │            │   │            │
    │ Ownership  │   │ Initiation │   │ Controls   │
    │ Joint/Sole │   │ Approval   │   │ Limits     │
    │ Delegation │   │ Limits     │   │ Supp cards │
    └─────┬──────┘   └────────────┘   └────────────┘
          │
    ┌─────▼──────────────────────────────────┐
    │                                         │
    ┌─────▼──────┐                     ┌──────▼──────┐
    │   COMMS    │                     │  CUSTOMER   │
    │            │                     │  MANAGEMENT │
    │ Account vs │                     │             │
    │ Personal   │                     │ Profile     │
    │ Consent    │                     │ KYC         │
    └────────────┘                     │ Servicing   │
                                       └─────────────┘
```

---

## How to Use This Document

When designing entitlements schemas or writing specs, start by identifying which domain(s) the feature touches. Then check:

1. What are the access patterns for that domain?
2. What permission model considerations apply?
3. What regulatory constraints affect the authorization model?
4. Does this feature involve cross-domain interactions?

This document is the "business context lens" — pair it with the Zanzibar/SpiceDB technical reference and the Delegation Use Cases doc for a complete picture.

---

*Last updated: March 2026*
