> ⚠️ SUPERSEDED — replaced by `schema-handoff-template.md` (v2, 2026-05-10). Schema design is TL territory; this template proposed schema code which blurred that boundary. Do not use for new runs.

# Schema Sketch Form — Template

> The shape every schema proposal takes. Used by the Schema Sketcher specialist on the way out, by the Scenario Builder on the way in. Implementation-ready but not auto-merged.

---

## Why this form exists

The Schema Sketcher proposes additions to one or more `domains/*/schema-fragment.zed` files. The output must be specific enough that the Tech Lead can review for implementation correctness without re-deriving intent from the AC, and structured enough that the Scenario Builder can generate scenarios against the proposed schema before the additions are merged.

This is also the artefact that triggers the dual-gate review: PM signs off on semantics (does this correctly model the use case?), TL signs off on implementation (is this idiomatic SpiceDB, performant, consistent?). The form makes both gates clear.

---

## Form shape

Every schema sketch has the following sections. Frontmatter required.

```yaml
---
id: SS-<DOMAIN>-<NN>             # e.g. SS-A-03 for the third Accounts schema sketch
prd_id: PRD-<DOMAIN>-<NN>        # the PRD this sketch addresses
ac_ids: [AC-A-NNN, AC-A-NNN, ...]  # AC IDs this sketch enables
domains: [<one or more affected domains>]
status: <proposed|signed-off-pm|signed-off-tl|approved|rejected>
source_run: runs/<YYYY-MM-name>
last_updated: <YYYY-MM-DD>
---
```

### 1. Summary

One paragraph. What's being added, to which fragment(s), and why. State the use case in two sentences and the schema response in two sentences.

### 2. Pattern citation

Which pattern(s) from `knowledge-base/schema-design-patterns.md` does this sketch apply? If none — flag it. Inventing a new pattern is allowed but requires explicit justification.

```
- Delegation pattern (with caveat for scope) — applied to trustee
- State override pattern — reused (no change)
```

### 3. Proposed additions per fragment

One subsection per affected fragment. Each subsection contains the literal `.zed` to be added, in order: relations, then permissions, then any new caveats. No deletions or modifications without a separate subsection naming them as such.

#### `domains/accounts/schema-fragment.zed`

**New relations**
```zed
// Trustee with scope-bounded authority over a trust-held account.
relation trustee: user with trust_scope | user with trust_scope with delegation_window
```

**New permissions** *(or modifications to existing permissions, called out)*
```zed
// Trustees join viewer at read floor.
permission viewer = holder
                  + delegate_view_talk
                  + delegate_view_pay
                  + attorney
                  + ops_agent
                  + trustee   // ← added
```

**New caveats** *(if any)*
```zed
// Trust scope — analogous to poa_scope, but trust-deed-driven.
caveat trust_scope(action: string, allowed_actions: list<string>) {
    action in allowed_actions
}
```

#### `domains/<other-affected-domain>/schema-fragment.zed`

*(repeat for each affected fragment)*

### 4. Cross-domain dependencies

Any new references *between* fragments. Read by the affected domain's SME because their fragment now has a new external dependency.

```
- payment.can_initiate_on_me — unchanged. Trustees are not holders, so they
  inherit no ON_ME funding capability. (Verified: no change needed in payments
  fragment.)
- card.can_change_controls — extended? Open question: does a trustee on a
  trust-held card account get the same controls as a PoA attorney? Defer.
```

### 5. Backward-compat assessment

Does this break any existing AC, scenario, or stored relationship? Required, even when the answer is no.

- Existing AC reviewed: AC-A-001 through AC-A-016. None affected (trustee is additive).
- Existing scenarios reviewed: 1–20 in `entitlements-scenarios-curated.md`. None affected.
- Stored relationships: no migration required (no existing trustee relations to backfill).

### 6. Trade-offs and alternatives

Three short paragraphs at most. What did you consider? Why is this the recommended shape?

```
Considered: encoding trustee as a special case of attorney (reuse poa_scope).
Rejected because (a) the regulatory anchor is different (Trustee Act 2000 vs
Mental Capacity Act 2005), (b) the audit trail benefits from distinct
relations, and (c) future trustee-specific scope rules (e.g. unanimous-action
requirements) are easier to model on a separate relation.
```

### 7. Performance and consistency notes

Anything that affects how the calling service must use this. Caveat-heavy permissions, cache implications, ZedToken posture for security-critical checks.

```
- Trustee permissions use trust_scope caveat — every check passes context.
  Caveat overhead is comparable to poa_scope (already in production-equivalent).
- No new high-fanout relations. LookupResources for trustee should be efficient.
- Security-critical checks (transact, manage_payees) require at_least_as_fresh
  consistency — same posture as existing attorney checks.
```

### 8. Test surface

Which AC IDs from the originating PRD will exercise this sketch in scenarios? Reverse pointer for the Scenario Builder.

```
- AC-A-017 (positive: trustee within scope can transact)
- AC-A-018 (negative: trustee outside scope is denied)
- AC-A-019 (revocation: trustee removal takes effect on consistency-fresh check)
```

### 9. Open questions

Required.

```
- Multiple trustees acting jointly — schema enables holder-style check, but
  the joint-action threshold belongs in app-layer workflow. Confirm with TL
  whether we want a richer check (e.g. quorum count) in v2.
- Corporate trustees — current schema treats trustee as `user`. If corporate
  trustees are common, may want a corporate-actor relation. Defer.
```

---

## Style and voice

- Comments in `.zed` are part of the deliverable. They should explain *why*, not just restate *what*.
- Match the voice profile for prose sections (sections 1, 4, 6, 7, 9). Schema blocks are code, not prose — clarity over voice there.
- No marketing language. The TL is reading this; they want precise.

## Sign-off discipline

Two gates, both required:

1. **PM (semantics):** does the relation model the use case correctly? Does the permission set match the AC? Are caveats used appropriately? Status flips to `signed-off-pm`.
2. **TL (implementation):** is this idiomatic SpiceDB? Does it pass the schema lint? Are performance and consistency assumptions sound? Status flips to `signed-off-tl`.

Status only flips to `approved` after both. `approved` is the trigger for fragment merge.
