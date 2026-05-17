# Skills

> Invocation recipes for the pipeline. One file per step. Each skill tells you exactly what to say to the agent, what files to attach, and what to do with the output.

Skills are the how; specialists are the what. Read a specialist contract to understand what an agent does and its quality bar. Read the skill to run it.

---

## Skills in this folder

| File | When to use | Required? |
|---|---|---|
| `00-triage.md` | A new requirement just landed. Always first. | Always |
| `01-spec-writer.md` | Run card open and brief captured. Produces PRD. | Always |
| `02-rule-lister.md` | PRD signed off. Produces AC. | Always |
| `03-scenario-builder.md` | AC signed off. Produces scenarios + SCHEMA-NEEDED flags. | Always |
| `05-schema-sketch.md` | Scenarios signed off AND new schema elements needed. Produces draft .zed proposals for TL. | Optional |
| `04-schema-handoff.md` | Scenarios signed off (and sketch done, if used). Produces TL brief. | Always |

**Default invocation order:** 00 → 01 → 02 → 03 → 04  
**With schema sketch:** 00 → 01 → 02 → 03 → 05 → 04

## How to use a skill

Each skill file has a **Prompt** block — copy it, fill in the `<placeholders>`, and send it to Claude (Cowork, Claude.ai Project, or Claude Code — your choice). Attach the files listed under **Attach**.

Skills are designed to be self-contained. You shouldn't need to remember anything about the framework's internals to invoke one — the skill tells you everything needed for that step.

## Running the full pipeline

See `pipeline.md` at the root for the end-to-end chain: when each skill fires, what the human gate is, and when to move to the next step.
