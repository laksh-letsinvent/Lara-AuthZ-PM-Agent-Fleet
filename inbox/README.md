# Inbox

> Raw stakeholder inputs land here before triage. One file per requirement. Triage reads from here and creates the run card.

---

## How to use this folder

1. Receive a requirement (email, doc, Confluence export, Slack thread, BA brief)
2. Save it here as `YYYY-MM-DD-<short-topic>.md`
3. Add frontmatter at the top:

```yaml
---
received: YYYY-MM-DD
from: <sender name and role>
format: <email|doc|brief|slack>
status: pending-triage
---
```

4. Invoke Skill 00 (Triage) pointing at this file — it reads the input and creates the run card

## After triage

- Flip `status` from `pending-triage` to `triaged`
- Triage will have created `runs/YYYY-MM-<name>/` with a populated run card
- The inbox file stays here as the original source record

## Archived inputs

Move triaged files to `inbox/archived/` once the run is closed (merged or parked). Keeps the inbox clean for active requirements.

## What goes here

Any format of raw requirement is fine — paste email text, copy a Confluence doc, transcribe a Slack thread. The PM's job is to capture the input faithfully, not to pre-structure it. Triage handles the structure.
