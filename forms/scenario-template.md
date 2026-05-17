# Scenario Form — Template

> The shape every runnable scenario takes. Used by the Scenario Builder specialist on the way out, by the prototype's Scenario Studio on the way in. The artefact that closes the loop — what turns "we agreed an AC" into "we watched it pass."

---

## Why this form exists

Every AC must have at least one scenario that exercises it. The Scenario Builder takes the AC corpus and the schema (proposed or merged) and produces concrete, runnable scenarios that load into Scenario Studio.

This form serves two consumers:

1. **The prototype's Scenario Studio** — needs structured input it can load, walk through, and run against SpiceDB.
2. **The audit trail** — every scenario links back to the AC it exercises, the run that produced it, and the schema state it was tested against.

The form below is structured for both. The prose sections are for humans; the structured blocks are what Studio loads.

---

## Form shape

Frontmatter required for the file as a whole, then one block per scenario.

```yaml
---
run: runs/<YYYY-MM-name>
prd_id: PRD-<DOMAIN>-<NN>
domains: [<one or more affected>]
schema_state: <reference to consolidated.zed version, e.g. "v1 + SS-A-03 proposed">
status: <draft|reviewed|approved|loaded-in-studio>
ac_coverage_target: <number — count of AC IDs this scenario file is meant to cover>
ac_ids_covered: [AC-A-NNN, AC-A-NNN, ...]
last_updated: <YYYY-MM-DD>
---
```

## Scenario block shape

Each scenario is a self-contained block with the following fields. One scenario = one block.

### `### N. SCENARIO_ID — Title [Primary Domain]`

```yaml
id: SC-<DOMAIN>-<NNN>
ac_ids: [AC-A-NNN, AC-A-NNN]    # which AC this exercises
domains: [<primary>, <secondary if cross-domain>]
type: <positive|negative|edge|state-transition|revocation|caveat>
narrative: |
  <One paragraph plain-English description. What's happening, why it matters.>
```

**Setup** *(relationship writes / deletes / state changes that establish the scenario)*

```
WRITE  account:trust_001#owner@user:tina
WRITE  account:trust_001#holder@user:tina
WRITE  account:trust_001#trustee@user:tina with trust_scope(allowed_actions: ["view", "transact"])
```

**Operations** *(the permission checks being asserted, with expected outcomes)*

```
CHECK  user:tina  account:trust_001  can_view              → ALLOW
CHECK  user:tina  account:trust_001  can_transact (action: "transact")  → ALLOW
CHECK  user:tina  account:trust_001  can_close             → DENY
CHECK  user:bob   account:trust_001  can_view              → DENY  (no relation)
```

**Expected pattern** *(one line — the generalisation this scenario demonstrates)*

```
Pattern: Trustee within scope has read + transact; cannot close (holder-only); non-related users have no access.
```

**Cleanup** *(optional — relationships to remove if running scenarios in sequence requires it)*

```
DELETE account:trust_001#trustee@user:tina
```

---

## Scenario types and what each must include

| Type | Must include |
|---|---|
| `positive` | Subject in expected relation → permission → ALLOW. The happy path. |
| `negative` | Subject NOT in any relevant relation → permission → DENY. The "default-deny" assertion. |
| `edge` | A boundary condition (e.g. delegation expiry exactly at `valid_until`, scope edge, joint-vs-sole). |
| `state-transition` | Resource state change mid-scenario (e.g. account flipped to bereavement, then permission re-checked). |
| `revocation` | Relationship removed mid-scenario, then permission re-checked with consistency posture noted. |
| `caveat` | Caveat context passed in two variants (in-scope and out-of-scope), demonstrating the caveat's effect. |

The Scenario Builder's contract names a coverage target across these types per AC.

---

## File-level structure

The scenario file (`04-scenarios.md` in a run folder) follows this top-level shape:

```markdown
---
<frontmatter>
---

# Scenarios — <Use Case Title>

## Setup state

<People, accounts, cards etc. — declared once at the top of the file,
referenced by ID throughout the scenarios. Mirrors the prototype's
existing setup block in entitlements-scenarios-curated.md.>

## Scenarios

### 1. SCENARIO_ID — Title [Primary Domain]
<scenario block>

### 2. SCENARIO_ID — Title [Primary Domain]
<scenario block>

...
```

## Compatibility with the prototype's Scenario Studio

The Scenario Studio in the prototype consumes a slightly looser format (no frontmatter, no per-scenario YAML). The Scenario Builder's contract requires producing the structured form *here*, and a `studio-import.json` companion file in the same run folder for direct Studio loading. The structured `.md` is the canonical artefact; the JSON is a derivative.

If Studio's import format changes, only the JSON output of the Scenario Builder changes — the canonical scenarios stay stable.

## Style and voice

Narrative sections (the `narrative:` field per scenario, the file's introductory paragraph) follow the voice profile. Setup and Operations blocks are code-shaped — clarity over voice. No marketing copy in scenario titles ("BASELINE — Sole owner full access" beats "Empowering Sole Owners with Comprehensive Access").

## Coverage rules

A scenario file is not complete until:

- Every AC ID listed in `ac_ids_covered` appears in at least one scenario's `ac_ids` field.
- Every AC has at least one positive scenario AND, where the AC implies a negative, at least one negative scenario.
- Caveat-bearing AC have at least one in-scope and one out-of-scope scenario.
- Revocation-relevant AC have a revocation scenario with consistency posture asserted.

The Scenario Builder's contract is responsible for hitting these targets. The PM signs off on coverage adequacy.
