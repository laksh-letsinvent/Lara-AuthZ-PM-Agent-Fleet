# AuthZ Agent Fleet

> A portable AI-native delivery framework for authorization (AuthZ) platform work.
> Built by a PM, for PMs. No eng required to produce regulator-defensible artefacts.
> Status: v1 — built and validated on a live entitlements platform build.

---

## What this is

A small, self-contained framework for designing, specifying, and validating new entitlement use cases using a fleet of specialist agents over a structured knowledge substrate.

One PM, a small set of well-defined agents, and a structured run folder takes a new use case from raw input to a TL-ready schema handoff brief — with the same rigour and traceability a regulator would expect from a real platform team.

Built on Google Zanzibar (SpiceDB) as the authorization model. The pipeline logic is platform-agnostic; the knowledge base is Zanzibar-specific and can be swapped for other frameworks.

---

## Six moving parts

- **Inbox** — where raw stakeholder inputs land before triage (lives in `inbox/`). Drop the email or doc here; triage reads from here.
- **Skills** — how to invoke each pipeline step (lives in `skills/`). Start here if you're running the pipeline.
- **Specialists** — what each agent does, its quality bar, its trust posture (lives in `specialists/`). Read these to understand or modify an agent's behaviour.
- **Forms** — the output shapes each specialist fills (lives in `forms/`). The contract between agents.
- **Domains** — what's known about each consuming domain: approved AC, schema fragments, regulatory anchors (lives in `domains/`). This is the platform state; it evolves as runs complete.
- **Knowledge Base** — stable reference material the agents read (lives in `knowledge-base/`). Zanzibar/SpiceDB reference, banking domain context, delegation use cases, schema design patterns.

---

## The pipeline

```
inbox/<input-file>.md  (PM drops raw input here)
        │
        ▼
[Skill 00 — Triage]           → verdict + creates run card  (runs/YYYY-MM-<name>/00-run-card.md)
        │   human gate
        ▼
[Skill 01 — Spec Writer]      → PRD                         (01-prd.md)
        │   human gate
        ▼
[Skill 02 — Rule Lister]      → Acceptance criteria         (02-ac.md)
        │   human gate
        ▼
[Skill 03 — Scenario Builder] → Scenarios + SCHEMA-NEEDED   (03-scenarios.md)
        │   human gate
        ▼
[Skill 05 — Schema Sketch]    → Draft .zed proposals        (05-schema-sketch.md)  ← OPTIONAL
        │   human gate (if used)
        ▼
[Skill 04 — Schema Handoff]   → TL brief                    (04-schema-handoff.md)
        │
        ▼
Tech Lead designs schema → schema-fragment.zed updated → run merged
```

The PM drops input in inbox, then gates every step. Agents draft; PM signs off; next step runs. No auto-act. Skill 05 (Schema Sketch) is optional — use it when you want to give the TL a starting point rather than a blank page.

**See `pipeline.md` for the full chain: how to start a run, what each gate checks, and the merge protocol.**

---

## Quick start

1. Requirement lands → save it to `inbox/YYYY-MM-DD-<topic>.md`
2. Invoke Skill 00 (Triage) → it produces a verdict and creates the run card automatically
3. Review the run card, resolve any open issues, confirm proceed
4. Invoke Skills 01 → 02 → 03 → 04 in order, one human gate each
5. Optionally invoke Skill 05 (Schema Sketch) between steps 03 and 04 if new schema elements are needed
6. Step 04 output goes to your Tech Lead — their schema work is tracked outside this folder
7. When schema is done: merge approved AC into the domain corpus, flip run status to `merged`

---

## Folder structure

```
authz-agent-fleet/
├── pipeline.md              ← the chain; read this to understand the e2e flow
├── inbox/                   ← raw stakeholder inputs; triage reads from here
├── skills/                  ← invocation recipes; start here to run a step
├── specialists/             ← agent contracts; read to understand or tune an agent
├── forms/                   ← output templates; one per pipeline stage
├── domains/                 ← platform state per consuming domain
│   ├── accounts/            ← reference domain (ac-corpus starts empty; runs populate it)
│   ├── payments/            ← stub
│   ├── cards/               ← stub
│   ├── communications/      ← stub
│   └── customer-mgmt/       ← stub
├── knowledge-base/          ← stable reference (Zanzibar, SpiceDB, banking context)
├── style/                   ← voice profile and writing standards
├── runs/                    ← one folder per use case; created by triage, never deleted
│   ├── _template/           ← triage uses this shape; PM does not copy it manually
│   └── <past runs>          ← historical record; stays after merge
└── log/                     ← build log; what worked, what didn't
```

---

## Porting to a new organisation or domain

Everything domain-specific is in `domains/` and `knowledge-base/`. To port:

1. Replace `knowledge-base/` with your platform's reference docs (or keep Zanzibar if applicable)
2. Replace `domains/` structure with your bounded contexts — one folder per domain, same shape
3. Replace `style/` with your org's voice profile and writing standards
4. Keep everything else unchanged — `pipeline.md`, `skills/`, `specialists/`, `forms/`, `runs/` are all domain-agnostic

The pipeline logic is stable across organisations. The knowledge substrate is the only variable.

---

## What v1 deliberately leaves out

- **Other domains beyond Accounts fully populated.** The other four are stubs — populate them with your real SMEs at port-to-work.
- **An orchestrator agent.** The PM is the orchestrator. Manual handoff between skills is intentional — every output is reviewed before passing forward.
- **Schema validation (zed CLI).** Schema design is the TL's job. The Scenario Builder flags SCHEMA-NEEDED gaps; the TL resolves them.
- **Automated merge.** Merging approved AC into the corpus is a manual step — one minute of work and worth the intentionality.

---

## Build notes

Built and validated on one end-to-end use case (third-party access / mandate) before publication. The eval run lives in `runs/`. The framework walked from a stakeholder email to 22 structured AC, a no-change schema verdict, and 20 runnable scenarios. Substrate and writing gaps surfaced; all documented in `log/`.

Build log: `log/build-log.md`.
