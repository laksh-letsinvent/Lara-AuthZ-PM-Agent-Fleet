> _Maintained copy for the agent fleet. Do not sync from `/knowledge` — that copy is archived._

# Delegation Use Cases — Entitlements Platform

> Reference for the complex delegation and multi-party access scenarios the Entitlements platform must support. These are the hard problems — joint accounts are the easy part. Power of Attorney, bereavement, guardianship, and legal heir access are where the real complexity lives.

---

## Why Delegation Is the Hard Problem

Standard account access (sole owner, full control) is trivially modelled: `account:123#owner@user:alice`. The complexity comes when multiple people need different levels of access to the same account, often with legal, temporal, and jurisdictional constraints. These aren't edge cases — they affect millions of banking customers and carry regulatory, legal, and reputational risk when handled poorly.

The Entitlements platform must support a spectrum from "simple shared access" to "legally complex delegated authority with jurisdictional variance."

---

## 1. Joint Accounts

### What It Is

Two or more individuals share ownership of a single account. This is the most common multi-party access pattern in retail banking.

### Types

**Joint Tenancy (default in UK banking)**
- All holders have equal, undivided ownership of the full balance
- Right of survivorship: on death of one holder, the surviving holder(s) automatically inherit full ownership
- No probate required for the account to continue
- Either holder can sever the joint tenancy unilaterally (converts to tenants in common)

**Tenants in Common**
- Each holder owns a defined share (e.g. 50/50, 60/40)
- No automatic survivorship: deceased holder's share goes through their estate
- Probate required before the deceased's share can be transferred
- More common in business/investment contexts

### Signature Authority Models

**Either to Sign (OR logic)**
- Any single holder can independently perform operations
- Most common for personal current accounts
- In Zanzibar terms: `permission transfer = holder_a + holder_b` (union)

**Both to Sign (AND logic)**
- All holders must approve an operation
- Common for business accounts, high-value savings
- In Zanzibar terms: `permission transfer = holder_a & holder_b` (intersection)
- Implementation challenge: requires a multi-step approval workflow, not just a single permission check

### Entitlements Model

```
definition user {}

definition account {
  relation holder: user                    // Joint holder
  relation primary_contact: user           // For comms routing

  // Either-to-sign: any holder can act
  permission transfer_either = holder
  permission view = holder

  // Both-to-sign: all holders must approve
  // NOTE: Intersection requires workflow support — you check each holder separately
  // and only proceed when all have approved
}
```

The "both to sign" pattern is not a simple CheckPermission call. It requires the application layer to:
1. Check that the initiator has `holder` relationship
2. Create a pending approval
3. Check that the approver also has `holder` relationship
4. Only execute when all required approvals are collected

### Key Considerations

- Joint accounts may have different signature rules for different operations (e.g. either-to-sign for payments under £500, both-to-sign above)
- Adding or removing a joint holder is itself a high-privilege operation that may require all existing holders to consent
- FSCS deposit protection is per-person: a joint account with two holders gets 2× the protection limit
- Joint accounts in bereavement follow different rules depending on joint tenancy vs tenants in common (see Section 3)

---

## 2. Power of Attorney (PoA)

### What It Is

A legal instrument that grants one person (the attorney) authority to act on behalf of another (the donor) in financial and/or personal welfare matters. The most complex delegation pattern in banking.

### UK Framework

**Lasting Power of Attorney (LPA)**
- Created while the donor has mental capacity
- Must be registered with the Office of the Public Guardian (OPG) before use
- Two types: Property & Financial Affairs (relevant for banking) and Health & Welfare
- Can be used while the donor still has capacity (if the donor consents) or after capacity is lost
- Registration takes 8-12 weeks and costs £82 per LPA

**Enduring Power of Attorney (EPA)**
- Pre-2007 instrument (no longer possible to create new ones)
- Only covers property and financial affairs
- Must be registered with OPG once the donor loses or is losing mental capacity
- Banks must still honour valid, registered EPAs

### What a PoA Holder Can Typically Do

- View account balances and transactions
- Initiate payments and transfers (subject to limits)
- Manage Direct Debits and standing orders
- Request statements
- Communicate with the bank on behalf of the donor

### What a PoA Holder Typically Cannot Do

- Open new accounts in the donor's name (varies by bank)
- Make gifts from the donor's funds (restricted by law — only customary gifts)
- Change the donor's will or beneficiaries
- Delegate their authority to someone else (unless the LPA specifically allows this)
- Act outside the scope specified in the LPA (e.g. a property-only LPA doesn't cover welfare decisions)

### Cross-Jurisdiction Considerations

| Jurisdiction | Instrument | Registration | Key Differences |
|---|---|---|---|
| **UK (England & Wales)** | Lasting Power of Attorney (LPA) | OPG registration mandatory | Two types (financial, welfare); usable before incapacity if donor consents |
| **UK (Scotland)** | Continuing Power of Attorney | Office of the Public Guardian (Scotland) | Similar to LPA but different legislation (Adults with Incapacity Act 2000) |
| **UK (Northern Ireland)** | Enduring Power of Attorney | High Court registration | No LPA equivalent yet; EPA only |
| **EU (General)** | Varies by member state | Typically notarised | No unified standard; cross-border recognition is patchy |
| **Netherlands** | Levenslooptestament / Volmacht | Notarial deed | Can be general or specific; notarisation common |
| **Spain** | Poder Notarial | Notarised | Must be specific for banking; general powers often rejected |
| **France** | Mandat de Protection Future | Court registration | Activates only on incapacity; requires medical certificate |
| **Germany** | Vorsorgevollmacht | Optional registration | Can be informal; banks often require notarised version |

### Entitlements Model

```
definition user {}

caveat poa_active(
  request_time: timestamp,
  registered_date: timestamp,
  revoked: bool
) {
  request_time >= registered_date && !revoked
}

caveat poa_scope(
  action_type: string,
  allowed_actions: list<string>
) {
  action_type in allowed_actions
}

definition account {
  relation owner: user
  relation attorney: user with poa_active      // PoA holder, conditional on registration

  permission view = owner + attorney
  permission transact = owner + (attorney with poa_scope)
  permission manage_account = owner             // Attorney cannot change account structure
}
```

### Key Considerations

- Banks frequently reject valid LPAs due to internal compliance concerns — the entitlements model should support a "verified" status on attorney relationships
- LPA verification is a human process (checking OPG registration, validating the physical document) — the entitlement is only created after this verification completes
- Multiple attorneys can be appointed: jointly (all must agree), jointly and severally (any can act independently), or jointly for some decisions and severally for others
- Successor attorneys may be named — they activate if the primary attorney can no longer act
- The donor can revoke the LPA at any time while they have capacity — this must trigger immediate entitlement removal
- Banks must balance "protect the donor" with "don't create unnecessary barriers for legitimate attorneys" — FCA Consumer Duty applies here

---

## 3. Bereavement

### What It Is

When an account holder dies, the account enters a specific state with its own access rules. The entitlements model must handle the transition from normal access to bereavement handling, then to estate settlement.

### Joint Account — Joint Tenancy (Survivorship)

**What happens:**
- The surviving holder automatically inherits full ownership
- The deceased's relationship is removed
- No probate required
- The account continues to function under the surviving holder's sole control

**Entitlements transition:**
1. Bank is notified of death (death certificate provided)
2. Deceased holder's relationships are removed: `DELETE account:123#holder@user:deceased`
3. Surviving holder retains all existing relationships
4. Account continues as a sole account

### Joint Account — Tenants in Common

**What happens:**
- The deceased's share becomes part of their estate
- Probate is required before the share can be distributed
- The surviving holder retains access to their share but may face restrictions on the full balance pending probate
- An executor/administrator gains access to the deceased's share

**Entitlements transition:**
1. Bank is notified of death
2. Account may be partially frozen (deceased's share)
3. Executor is granted limited access: `WRITE account:123#executor@user:executor_id`
4. After probate: executor can instruct transfer of deceased's share

### Sole Account

**What happens:**
- The account is frozen immediately on notification of death
- No one has access until an executor or administrator is appointed
- Grant of Probate (if there's a will) or Letters of Administration (if no will) must be obtained
- The executor/administrator then gains access to manage the estate

**Entitlements transition:**
1. Bank notified of death → all existing relationships frozen
2. `WRITE account:123#frozen@flag:bereavement` (state-level override)
3. Executor presents Grant of Probate → verified by bank
4. `WRITE account:123#executor@user:executor_id`
5. Executor can view, pay debts, distribute estate
6. Account eventually closed

### Small Estates Exception

For accounts with balances below £5,000–£15,000 (varies by bank), banks may release funds without full probate documentation. This is a bank-specific policy, not a legal requirement. The entitlements model should support configurable thresholds.

### Entitlements Model

```
definition user {}

caveat executor_verified(
  grant_type: string,         // "probate" or "letters_of_administration"
  verified_date: timestamp,
  request_time: timestamp
) {
  verified_date > 0 && request_time >= verified_date
}

definition account {
  relation owner: user
  relation holder: user
  relation executor: user with executor_verified
  relation frozen_reason: string              // "bereavement", "fraud", etc.

  // Normal access blocked when frozen
  permission is_frozen = frozen_reason
  permission normal_access = (owner + holder) - is_frozen

  // Executor access only when verified and account is in bereavement
  permission executor_access = executor
  permission view = normal_access + executor_access
  permission distribute_estate = executor_access
}
```

### Key Considerations

- Bereavement is a state, not a relationship — the account's state changes, which overrides individual permissions
- The transition from "frozen" to "executor has access" is gated by a human verification process (checking probate documents)
- Funeral expenses may be released from frozen accounts before probate — this is a special exception that needs modelling
- Direct Debits and standing orders may continue or be cancelled depending on the account type and bank policy
- The emotional context matters for product design: bereaved families are vulnerable customers, and the entitlements system should not create unnecessary friction

---

## 4. Guardianship & Deputyship

### What It Is

Court-appointed authority to manage the financial affairs of someone who lacks mental capacity and did not create a Power of Attorney while they had capacity.

### UK: Deputyship (Court of Protection)

- Applied for through the Court of Protection when someone lacks mental capacity
- Court appoints a deputy to manage property and financial affairs
- Deputy must act in the person's best interests
- Court may impose specific restrictions (spending limits, reporting requirements)
- Annual reporting to the OPG is mandatory
- Application process takes 4-6 months and costs £371 + potential hearing fees

**What a deputy can do:**
- Manage bank accounts
- Pay bills and manage finances
- Make investment decisions (within court-specified limits)
- Sell property (with court approval)

**What a deputy cannot do:**
- Make decisions the person can make themselves
- Act outside the scope of the court order
- Make gifts (except in limited circumstances with court approval)
- Delegate their authority

### UK: Scottish Guardianship

- Under the Adults with Incapacity (Scotland) Act 2000
- Similar to deputyship but with different legislation
- Financial guardian appointed by the Sheriff Court
- Powers specified in the guardianship order

### Minor Accounts — Parental/Guardian Access

- Accounts opened for children (under 18) are managed by a parent or legal guardian
- The parent/guardian has full control until the child reaches a specified age (typically 16 for some operations, 18 for full control)
- Age-based permission transitions: at 11, child may get limited self-service; at 16, joint control; at 18, full handover

**Entitlements model for age transitions:**

```
caveat minor_guardian_access(
  child_age: int,
  guardian_full_control_until: int
) {
  child_age < guardian_full_control_until
}

caveat minor_self_service(
  child_age: int,
  self_service_from: int
) {
  child_age >= self_service_from
}

definition account {
  relation minor_holder: user
  relation guardian: user with minor_guardian_access

  permission guardian_full_control = guardian
  permission minor_view = minor_holder with minor_self_service
  permission minor_transact = minor_holder with minor_self_service
}
```

### Key Considerations

- Deputyship orders specify the exact scope of the deputy's authority — the entitlements model must support order-specific permission scoping
- Court orders can be time-limited or indefinite
- Deputies must file annual reports — the system should support audit queries for regulatory reporting
- The transition from "parent manages child's account" to "young adult manages own account" should be automated based on age thresholds
- Multiple guardians/deputies may be appointed with different scopes

---

## 5. Third-Party Mandates

### What It Is

A formal instruction from an account holder authorising a named third party to operate the account on their behalf, without the legal framework of a Power of Attorney.

### Types

**General Mandate**
- Broad authority to operate the account
- Typically time-limited (annual renewal)
- Common for business accounts where a bookkeeper or assistant manages finances

**Specific Mandate**
- Authority for specific operations only (e.g. "can view statements and set up standing orders, but cannot make payments over £1,000")
- Scoped by action type and/or amount

**Temporary Mandate**
- Short-term access for a specific purpose (e.g. "manage my finances while I'm travelling for 3 months")
- Auto-expires on a specified date

### Entitlements Model

```
caveat mandate_valid(
  request_time: timestamp,
  valid_from: timestamp,
  valid_until: timestamp
) {
  request_time >= valid_from && request_time <= valid_until
}

caveat mandate_scope(
  action: string,
  permitted_actions: list<string>,
  amount: int,
  max_amount: int
) {
  action in permitted_actions && amount <= max_amount
}

definition account {
  relation owner: user
  relation mandated_party: user with mandate_valid

  permission view = owner + mandated_party
  permission transact = owner + (mandated_party with mandate_scope)
}
```

### Key Considerations

- Mandates are simpler than PoA — they don't survive loss of mental capacity
- The account holder can revoke a mandate at any time
- Banks typically require mandates to be set up in-branch with identity verification of the mandated party
- Mandates don't transfer fiduciary duty — the mandated party acts on instruction, not in the person's best interests

---

## 6. Appointeeship (DWP Benefits)

### What It Is

The Department for Work and Pensions (DWP) can appoint someone to manage benefits payments on behalf of a person who cannot manage their own affairs.

### Scope

- Limited to DWP benefits only (not other income or assets)
- Appointee manages benefits payments into the person's account
- Appointee can use the benefits to pay bills and meet the person's needs

### Entitlements Implications

- Appointeeship is narrower than deputyship — it only covers benefits income
- The entitlements model needs to distinguish between "benefits-related transactions" and "other transactions"
- This is a niche but important pattern for vulnerable customers

---

## 7. Trustee Arrangements

### What It Is

A trust holds assets (including bank accounts) on behalf of beneficiaries, managed by trustees. The trustees have legal authority to manage the trust's financial affairs.

### Types Relevant to Banking

- **Bare trusts:** Beneficiary has absolute right to assets; trustee holds in name only
- **Discretionary trusts:** Trustees decide how to distribute; beneficiaries have no fixed entitlement
- **Life interest trusts:** One beneficiary receives income during their lifetime; capital goes to others

### Entitlements Model

```
definition trust {
  relation trustee: user
  relation beneficiary: user
}

definition account {
  relation trust: trust

  permission manage = trust#trustee
  permission view_income = trust#beneficiary
  permission view_capital = trust#trustee   // Beneficiaries may not see capital
}
```

### Key Considerations

- Multiple trustees may need to act jointly
- Trust deeds specify the scope of trustee authority — each trust is different
- Beneficiaries may have visibility but not control
- Trust accounts have specific tax and reporting obligations

---

## Delegation Complexity Matrix

| Delegation Type | Formality | Cost | Duration | Scope | Revocability | Survives Incapacity |
|---|---|---|---|---|---|---|
| **Joint Account** | Account opening | Free | Indefinite | Full (either) or controlled (both) | Requires all holders | N/A |
| **Power of Attorney (LPA)** | Legal document + OPG registration | £82 | Until revoked or death | As specified in LPA | By donor (with capacity) | Yes (primary purpose) |
| **Deputyship** | Court application | £371+ | As court specifies | As court specifies | By court | N/A (created because of incapacity) |
| **Third-Party Mandate** | Bank form | Free | Typically annual | As specified | By account holder | No |
| **Appointeeship** | DWP application | Free | Ongoing | Benefits only | By DWP | N/A |
| **Guardianship (minor)** | Automatic (parent) or court | Varies | Until child reaches age threshold | Full (parental) or as court specifies | Age-based transition | N/A |
| **Executorship** | Grant of Probate | £273+ | Until estate settled | Estate administration | N/A (deceased) | N/A |
| **Trusteeship** | Trust deed | Varies | As trust specifies | As trust deed specifies | Per trust terms | Per trust terms |

---

## Regulatory Framework Summary

### FCA (Financial Conduct Authority)

- **Consumer Duty:** Banks must act in customers' best interests — applies to how delegation access is managed, especially for vulnerable customers
- **Third-party access:** Banks must have clear processes for granting and revoking delegated access
- **Joint accounts:** Fair treatment of both holders, including during disputes and separation

### PSD2 / Payment Services Regulations

- **Strong Customer Authentication (SCA):** Applies to the person performing the action, including delegates
- **Third-Party Providers (TPPs):** Open Banking access operates in parallel to delegation — a PoA holder could also consent to TPP access
- **Regulatory gap:** Traditional PoA arrangements sit between PSD2's explicit TPP framework and common law agency

### GDPR / Data Protection Act 2018

- **Delegated access to personal data:** A PoA holder accessing account data is processing the donor's personal data — requires a legal basis
- **Data subject rights:** The donor retains rights over their data, even when they lack capacity
- **Right to be informed:** The donor (or their representative) must be informed about how data is processed
- **Cross-border data transfers:** Relevant when PoA holders are in different jurisdictions

### AML / KYC Regulations

- **Due diligence on delegates:** Banks must verify the identity of anyone granted account access
- **Beneficial ownership:** The underlying account holder remains the beneficial owner, even when a delegate operates the account
- **Sanctions screening:** Delegates must be screened against sanctions lists
- **Suspicious activity reporting:** Unusual delegation patterns may trigger SAR obligations

---

## Implementation Priorities

Based on volume, complexity, and regulatory risk:

1. **Joint accounts** — Highest volume, well-understood patterns, start here
2. **Power of Attorney** — High complexity, strong regulatory requirements, significant vulnerable customer impact
3. **Bereavement** — Emotionally sensitive, regulatory focus on vulnerable customers, operational pain point for most banks
4. **Third-party mandates** — Simpler than PoA, common for business banking
5. **Guardianship/Deputyship** — Lower volume but high complexity per case
6. **Minor accounts** — Clear age-based rules, good candidate for automated transitions
7. **Appointeeship** — Niche but important for vulnerable customer compliance
8. **Trusteeship** — Complex but lower volume in retail banking

---

*Last updated: March 2026*
