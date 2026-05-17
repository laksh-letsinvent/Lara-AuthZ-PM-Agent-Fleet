# Schema Handoff Form — Template

> The PM's brief to the Tech Lead. Produced after scenarios are approved. Not a schema design — that's the TL's job. This document tells the TL what must be achievable and hands over the AC and scenarios as the requirements surface.

---

## Why this form exists

Schema design belongs in technical leadership territory. The PM's job is to specify what must be true (scenarios and AC); the TL's job is to figure out how to model it in SpiceDB. This form is the boundary artefact — everything the TL needs to start schema work, nothing they don't.

Handing over half-formed schema sketches creates confusion about who owns the design decision. This form doesn't attempt to prescribe `.zed` code. It states requirements clearly and asks specific questions.

---

## Form shape

```yaml
---
id: SH-<DOMAIN>-<NN>             # e.g. SH-A-04 for the fourth Accounts handoff
prd_id: PRD-<DOMAIN>-<NN>
ac_ids: [AC-X-NNN, ...]          # all AC IDs covered by this handoff
domains: [<one or more>]
status: <draft|ready-for-tl|tl-acknowledged|schema-complete>
source_run: runs/<YYYY-MM-name>
last_updated: <YYYY-MM-DD>
---
```

### 1. What this is about

One paragraph. The use case in plain English. What the customer can do that they couldn't before, or what changes about how an existing permission works.

### 2. What must be achievable (scenarios)

Link to the approved scenarios file and list the key capability assertions in plain English. The TL should be able to read this section without opening the scenarios file.

```
From: runs/<YYYY-MM-name>/03-scenarios.md (approved)

Key capabilities that must work:
- [Subject X] can [action Y] on [resource Z] when [condition].
- [Subject X] cannot [action Y] when [condition is absent].
- Revoking [relation] must take effect on the next consistency-fresh check.
- ...
```

### 3. Acceptance criteria (structured)

Direct reference to the approved AC file. The AC are the contract — the schema design must satisfy all of them.

```
From: runs/<YYYY-MM-name>/02-ac.md (approved)
AC count: <N>
AC IDs: [AC-X-NNN, ...]
```

List any AC that the TL should pay special attention to — caveated permissions, cross-domain dependencies, revocation requirements.

### 4. Known constraints

What the PM knows that constrains the design. Keep it factual — don't speculate about schema implications.

- **Regulatory anchor:** [e.g. Mental Capacity Act 2005 requires distinct audit trail for this relation — affects naming conventions]
- **Cross-domain dependency:** [e.g. This subject must be able to initiate payments — Payments domain involved]
- **Backward-compatibility requirement:** [e.g. Existing UC-A-06 (PoA) AC must not be broken]
- **Caveat context:** [e.g. Scope is bounded by trust deed — some form of scope-check caveat needed]

### 5. Out of scope (PM's scope boundary)

What the PM has explicitly excluded from this use case. Helps the TL avoid designing for things that don't need to be in scope yet.

- [e.g. Corporate trustees — defer to v2]
- [e.g. Multi-trustee quorum logic — application-layer workflow, not schema]
- [e.g. Automatic trust deed parsing — manual flag for now]

### 6. Open questions for TL

The PM's questions for the TL — the things that require schema expertise to answer. This is not a request for a schema draft; it's a targeted set of questions to resolve before or during design.

- [e.g. Can this relation reuse an existing caveat (`poa_scope`), or does the distinct regulatory basis require a new one?]
- [e.g. Does this subject need to be modelled at the account level, or does it inherit from a parent resource?]
- [e.g. What consistency posture does the TL recommend for the revocation check?]

### 7. Sign-off

| Gate | Owner | Status |
|---|---|---|
| PM (scenarios + AC complete) | <name> | <pending / signed-off> |
| TL acknowledged | <name> | <pending / acknowledged> |
| Schema design complete | <name> | <pending / complete — link to PR or schema fragment> |

---

## Style notes

- Prose sections should be PM-quality writing — clear, specific, no filler.
- Don't write `.zed` code. If you find yourself sketching schema syntax, stop — that's the TL's job.
- Open questions should be genuine questions, not rhetorical ones. If you already know the answer, state it as a constraint (section 4).

## Length target

One to two pages. If it's longer, the use case scope may need splitting.
