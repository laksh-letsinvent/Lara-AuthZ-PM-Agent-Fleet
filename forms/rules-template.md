# Rules Form — Template

> The shape every acceptance criterion takes. Used by the Rule Lister specialist on the way out, by the Schema Sketcher and Scenario Builder on the way in. The single most-depended-on form in the framework.

---

## Why this form exists

The whole framework rests on the AC corpus being structured, not prose. If AC are paragraphs of "the system should...", we cannot:

- Generate scenarios mechanically from them
- Audit coverage across use cases and jurisdictions
- Cite a specific assertion in a regulator response
- Detect when a schema change breaks an existing AC

The form below makes each AC a small, queryable object. The cost is a slightly more rigid writing style. The benefit is everything else in the framework working.

---

## Form shape

Every AC has the following fields. Required unless marked optional.

```yaml
id: AC-<DOMAIN>-<NNN>           # e.g. AC-A-001 for Accounts; AC-P-001 for Payments
use_case: UC-<DOMAIN>-<NN>       # the use case this AC belongs to
domain: <accounts|payments|cards|communications|customer-mgmt>
status: <proposed|approved|deprecated>
statement: |
  <Plain-English assertion. One sentence preferred, two max. Subject + action + resource + condition.>
subject:
  relation: <relation name on the resource, or "any" / "none">
  notes: <optional — caveats on subject, e.g. "with poa_scope containing transact">
action:
  permission: <permission name as it appears in the schema>
  context: <optional — caveat context the calling service must pass>
resource:
  type: <account | payment | card | communication | customer_profile>
  state: <optional — required state of the resource, e.g. "blocked@flag:bereavement">
expected: <allow | deny | conditional>
negative_case: <optional — the inverse assertion that must also hold>
anchors:
  - <named regulatory or business anchor from regulatory-anchors.md>
notes: <optional — context, edge cases, links to decision log>
source_run: <runs/YYYY-MM-name — the run that produced this AC>
```

---

## A worked example

```yaml
id: AC-A-008
use_case: UC-A-06
domain: accounts
status: approved
statement: |
  An attorney with poa_scope containing "transact" and "manage_payees"
  can initiate payments and add payees on the donor's account.
subject:
  relation: account#attorney
  notes: poa_scope containing the relevant action
action:
  permission: can_transact, can_manage_payees
  context: action passed in caveat context must match
resource:
  type: account
  state: not blocked
expected: allow
negative_case:
  An attorney whose poa_scope does NOT contain "transact" gets deny on can_transact.
anchors:
  - Mental Capacity Act 2005
  - FCA Consumer Duty
notes: |
  This is the canonical PoA-within-scope assertion. The negative case
  (out-of-scope action) is covered by AC-A-010.
source_run: pre-framework
```

The corresponding entry in `ac-corpus.md` is the human-readable version of the same object. The YAML form lives in run output (`02-rules.md`); the merged corpus uses the prose form for readability while preserving the same fields.

---

## Writing rules (style)

- **One assertion per AC.** "X can do Y *and* W" is two ACs, not one.
- **Statement first, fields second.** The statement should be readable on its own. Fields are how machines parse it.
- **Negative case where it changes the meaning.** "Holders can close" is meaningful only with "delegates cannot close." Pair them.
- **Anchor every AC.** If you can't name a regulatory or business anchor, the AC may not belong in the corpus — or the anchor needs adding to `regulatory-anchors.md`.
- **No hedge words.** "Should" or "may" are forbidden. The schema either allows or denies; AC reflects that bivalent reality. Caveated permissions get `expected: conditional`.
- **Voice.** Match the voice profile and anti-AI style. No "robust", no "leverage", no "delve into". State the thing.

---

## Conventions

- **ID namespacing by domain initial:** A=Accounts, P=Payments, C=Cards, M=Communications (M for "Messaging" to avoid collision with Cards), U=Customer-mgmt (U for "User profile" to avoid collision with Communications). Document the mapping in the framework README if it ever changes.
- **AC IDs are stable forever.** Once an AC is approved, its ID does not get reused. If an AC is deprecated, status flips to `deprecated`; the ID stays.
- **Cross-domain ACs.** When an AC genuinely spans two domains (rare), its primary domain is whichever owns the resource being checked. The other domain's `ac-corpus.md` may carry a back-reference but not the canonical entry.

---

## Coverage targets

A use case is not "approved" until its AC corpus covers, at minimum:

- The positive happy path (subject can do action under normal conditions).
- The negative non-relation path (a user with no relation has no access).
- The state-blocking path (where the resource has a blocking state, the right permissions deny).
- The caveat-out-of-scope path (where the AC involves a caveat, the out-of-scope case is asserted).
- The revocation path (where the AC involves a relation that can be revoked, the post-revocation behaviour is asserted, including consistency posture).

The Rule Lister's contract names these as required generation targets.
