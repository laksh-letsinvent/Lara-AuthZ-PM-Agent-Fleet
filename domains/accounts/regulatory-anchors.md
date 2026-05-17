---
domain: accounts
last_updated: 2026-04-29
---

# Accounts — Regulatory Anchors

Regulations that bear directly on retail account access, delegation, and state transitions. Each entry names the source, what it requires, and where it lands in the schema.

This is the document the Rule Lister consults when generating AC for Accounts use cases — it links every assertion back to a named regulatory source.

---

## FCA Consumer Duty (PRIN 2A)

**What it requires.** Firms must act to deliver good outcomes for retail customers, with specific attention to vulnerable customers. Bereaved customers, those lacking capacity, and the elderly are explicitly named in FCA guidance.

**Where it lands in the schema.**
- `account#blocked@flag:bereavement` — bereavement state must be a first-class transition with documented effects, not an ad-hoc flag.
- `attorney` relation with `poa_scope` caveat — PoA flows must allow donors to retain capacity-appropriate control.
- `ops_agent` with `ops_consent` caveat — vulnerability detection by ops staff must be consent-gated.

**Open questions.** Vulnerability flag visibility (currently `customer_profile#can_view_vulnerability` is ops-only) — is the customer entitled to know they've been flagged? Probably yes under Consumer Duty; revisit when CustMgmt domain is populated.

---

## Mental Capacity Act 2005 (England and Wales) and the Adults with Incapacity (Scotland) Act 2000

**What they require.** Authority to act on behalf of someone who lacks capacity must come from a recognised legal instrument: LPA (England/Wales), Continuing PoA (Scotland), Welfare PoA, Court of Protection deputyship. The instrument defines the scope.

**Where it lands in the schema.**
- `attorney` relation requires `poa_scope` caveat — the schema cannot grant attorney rights without a documented scope.
- Currently the schema models LPA Property and Financial Affairs (UC-A-06). Scottish Continuing PoA, Welfare PoA, and Deputyship are out of scope for v1 — each will need its own relation or caveat extension.

**Open questions.** Should `attorney` be split into per-instrument relations (`lpa_attorney`, `cpa_attorney`, `deputy`) or remain a single relation with a richer caveat? Currently the latter; revisit when v2 use cases land.

---

## PSD2 / Payment Services Regulations 2017

**What it requires.** Strong Customer Authentication (SCA) for payment initiation and account access, with defined exemptions. Open Banking PISP/AISP access requires explicit consent and is scope-bound.

**Where it lands in the schema (Accounts portion).**
- `can_transact` — the gate that any payment initiation must pass. Delegates with `delegate_view_pay` and attorneys within scope qualify; pure viewers do not.
- The wider PISP/AISP consent model lives in `domains/payments/` (when populated). Accounts only exposes the relations Payments depends on.

**Open questions.** SCA step-up for delegate-initiated payments — does a View & Pay delegate need their own SCA, or can they ride the holder's? Worth a regulatory read with legal before drafting AC.

---

## GDPR / Data Protection Act 2018

**What it requires.** Lawful basis for processing personal data; data subject rights (access, rectification, erasure) regardless of capacity; data minimisation.

**Where it lands in the schema (Accounts portion).**
- `viewer` defines who can see account data. Every relation that grants viewer access creates a data-processing relationship that must have a lawful basis.
- `can_view` is intentionally permissive (covers V&T, V&P, attorney, ops). The lawful-basis check happens at the calling service layer, not in the permission check — but the AC corpus must document the basis per relation.
- Bereavement: data subject rights expire with the data subject. Executor access (`attorney` with view-only `poa_scope`) is the inheritance pattern.

**Open questions.** Right of erasure on a joint account where one holder withdraws — schema doesn't currently model this. Likely needs an "erasure pending" account state plus per-holder data scoping.

---

## FCA Banking: Conduct of Business Sourcebook (BCOBS) and Lending Conduct of Business Sourcebook (CONC)

**What they require.** Clear processes for granting and revoking third-party access. Customer must be informed about the scope of access granted to delegates.

**Where it lands in the schema.**
- `delegate_view_talk` and `delegate_view_pay` — the schema enforces tier separation; the calling service must surface the tier in user-facing flows.
- `can_delegate = holder` — only holders can grant delegation. The schema prevents delegated grant-of-grant.
- Revocation: instant effect once `DeleteRelationships` runs and ZedToken is fresh. The AC for revocation must call out consistency posture.

---

## FSCS (Financial Services Compensation Scheme)

**What it requires.** Per-person deposit protection up to the relevant limit. Joint accounts protect both holders separately.

**Where it lands in the schema.**
- Indirectly. The schema doesn't model FSCS — but `holder` count on a joint account is the data point FSCS calculations need. Worth flagging when a use case adds non-holder relations that might be misread as ownership (e.g., trustee).

---

## How to add a new anchor

When a run surfaces a new regulatory ground (e.g., Trustee Act 2000 for trusteeship use cases), append an entry here in the same shape:

- Source (named, with section if relevant)
- What it requires (one paragraph)
- Where it lands in the schema (specific relations / permissions / caveats)
- Open questions (don't pretend it's all resolved)

Each AC in `ac-corpus.md` cites at least one anchor from this file.
