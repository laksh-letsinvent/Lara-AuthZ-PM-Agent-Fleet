# Build Log

Week-by-week notes from the v1 solo build. What worked, what didn't, what took longest. The artefact that turns "I built a framework" into "I learned what the framework needs to be."

Format per entry: date, what was built, what worked, what didn't, what to change next.

---

## 2026-04-29 — Day zero: framework structure

**Built:**
- Top-level README with mental model committed
- `knowledge-base/` populated with five reference files (drift-headed copies from `/knowledge`)
- `style/` populated with voice profile and anti-AI writing style (drift-headed copies)
- `domains/accounts/` populated end-to-end: README, use-cases, schema-fragment, regulatory-anchors, ac-corpus (10 use cases, 16 ACs from existing material)
- Other four domain folders stubbed with READMEs
- `forms/rules-template.md` drafted — the most-depended-on form
- `forms/README.md` and `specialists/README.md` placeholder docs
- `schema/` folder created (empty; consolidation deferred until other domains populated)

**What worked:**
- Reusing the existing prototype schema as the source of truth for the Accounts fragment — no need to redesign anything.
- Tight separation: KB stable, Brain evolves, Style filters output. Mental model survived contact with the actual files.

**What didn't:**
- Initial instinct was to populate all five domains. Pulled back to stubs only — the right call. Multi-domain population needs SMEs.

**Next:**
- Week 1 proper: refine Rules template based on a fresh use case attempt; draft PRD template; pick the Spec Writer's tooling home (Claude.ai Project vs Cowork skill).

---

## 2026-04-29 — Day zero, batch 2: forms pipeline complete

**Built:**
- `forms/prd-template.md` — Spec Writer's output shape. Frontmatter + 11 named sections, AC-feedable, voice-disciplined.
- `forms/schema-sketch-template.md` — Schema Sketcher's output shape. Frontmatter + 9 sections including dual-gate sign-off discipline (PM semantics, TL implementation), pattern citation, cross-domain dependencies, backward-compat assessment.
- `forms/scenario-template.md` — Scenario Builder's output shape. Frontmatter + per-scenario YAML blocks + setup/operations/cleanup format compatible with the prototype's Scenario Studio. Coverage rules named.
- `runs/_template/00-run-card.md` and `runs/_template/README.md` — run scaffolding. Copy-the-folder pattern for starting any new run.

**What worked:**
- Drafting all four forms before any specialist contract. Catches contract mismatches between forms early — would have been brutal to discover during specialist design.
- Anchoring each template on existing artefacts (third_party_access.md for PRD shape, entitlements-scenarios-curated.md for scenario shape). The framework respects what's already proven.
- Voice + anti-AI requirements named explicitly in each template, not assumed. Removes ambiguity for the specialist contracts.

**What didn't:**
- Some risk that the templates are too prescriptive. Worth testing on a real use case before locking. The trusteeship use case (UC-A-11) is the v1 demo target — if templates feel rigid there, refine.

**Next:**
- Specialist contracts in pipeline order: spec-writer → rule-lister → schema-sketcher → scenario-builder. Spec Writer first, in Cowork. Schema Sketcher when we get there will live in Claude Code (code-shaped output, validates against zed CLI).

---

## 2026-04-29 — Day zero, batch 3: specialist contracts complete

**Built:**
- `specialists/spec-writer.md` — first specialist contract. Cowork-tooled. Inputs, output, trust posture (auto-suggest), quality bar with pass/fail examples, eval rubric against three known reference use cases (third-party access, joint accounts, PoA UK LPA).
- `specialists/rule-lister.md` — second contract. Cowork-tooled. Coverage discipline made explicit; anchor-existence check is a hard gate.
- `specialists/schema-sketcher.md` — third contract. Claude Code-tooled (code-shaped output, zed CLI validation in loop). Dual-gate review (PM semantics, TL implementation) called out as non-negotiable.
- `specialists/scenario-builder.md` — fourth contract. Claude Code-tooled (verification means running against the prototype). Studio loadability is a hard gate; unverified scenario files are not `loaded-in-studio`.

**What worked:**
- Each contract slots cleanly against its form. The forms-first discipline paid back here — specialist contracts referenced concrete output shapes rather than waving at "structured output."
- Eval rubrics are testable. Each specialist has 3 reference cases the framework can use to tune the prompt, with pass criteria stated.
- Tooling split (Cowork for prose, Claude Code for code) is named per specialist, not implicit. Avoids the "but where does this run?" confusion at port-to-work.

**What didn't:**
- Some risk that specialist contracts feel like over-engineering for v1 solo. They're not — they're the artefact that ports to work. The discipline is the deliverable.
- The Schema Sketcher and Scenario Builder contracts assume a working prototype. If the prototype regresses, those specialists' verification gates can't be exercised. Worth a sanity-check of the prototype before week 5–6.

**Framework status:**
- All four forms drafted.
- All four specialist contracts drafted.
- Accounts domain populated end-to-end; other four domains stubbed.
- Knowledge base and style copied with drift headers.
- Run template scaffolded.
- The framework is *complete on paper*. Next: invoke the first specialist on a real use case.

**Next:**
- Pick the v1 demo use case. Strong candidate: trusteeship for a trust-held current account (UC-A-11, already proposed in `domains/accounts/use-cases.md`). Open the run folder, fill the run card, invoke Spec Writer.

---

## 2026-05-04 — First end-to-end walk: gap surfaced and patched

**What we did:**
- Started Option A — exercising the framework on the third-party-access use case as the eval reference.
- Opened `runs/2026-05-third-party-access-eval/`, drafted run card and 01-prd.md.

**Gap surfaced (caught by Laksh on review):**
- The run card did not contain the stakeholder brief. The Spec Writer read Adrian's email from chat, not from a file in the run folder. That makes the run non-reproducible — re-opening it later yields a PRD with no captured input.

**Fix applied (same session):**
- Added "Stakeholder brief (input)" section to `runs/_template/00-run-card.md` so every future run captures the verbatim input.
- Updated `runs/2026-05-third-party-access-eval/00-run-card.md` retroactively with Adrian's email.
- Updated `specialists/spec-writer.md` input list — the brief is now a *file* read (run card), not a chat-passed argument. Includes the why-it-matters note for future readers.
- Convention added: briefs over a page move to `runs/<run>/_input/` with a link from the run card.

**Lesson:**
- Walking the framework on a real use case surfaces gaps the contracts wouldn't have caught on paper. This is exactly why we ran Option A before Option B. Expect more of these in Steps 2–4.

**Next:**
- Continue the third-party-access run from Step 2 (Rule Lister). The Step 1 PRD remains valid; the brief is now properly captured.

---

## 2026-05-04 — Walking Steps 2 and 3: substrate gap, refactor item, tooling expedient

**What we did:**
- Step 2 (Rule Lister) — produced `02-rules.md` with 22 AC. Coverage targets met. 11 AC carry `proposed-pending-domain-substrate` because four domains are stubs.
- Step 3 (Schema Sketcher) — produced `03-schema-sketch.md` with `recommendation: no-schema-changes-proposed`. Existing schema supports all 22 AC.

**What surfaced:**

1. **Substrate gap is recurrent** — the same four-domains-are-stubs gap surfaces at every multi-domain step. Every specialist hits it. Captured as a fact: until domain-population work happens, multi-domain runs always produce a mix of merge-ready and pending-substrate output. Not a bug; the framework is being honest about its current state.

2. **Refactor item RB-001** — Laksh raised the "use-cases.md vs PRD vs AC" three-layer concern. Captured in `log/refactor-backlog.md`. Deferred to consolidation pass before finalisation.

3. **Tooling expedient on Step 3** — the Schema Sketcher's contract specifies Claude Code (because of `zed` CLI validation in the iteration loop). I produced the sketch in Cowork. It "worked" because the sketch was no-change — there was nothing to validate. For a future run with an additive schema sketch (trusteeship, etc.), Step 3 must genuinely move to Claude Code. The contract was right; the eval-in-Cowork-only path is the expedient.

4. **Schema Sketcher surfaced domain-population as the real next-action** — even with no design work to do, the framework correctly identified that the four stub fragments need to be lifted from the prototype reference into `domains/*/schema-fragment.zed`. Mechanical task, but identified as actionable.

**Next:**
- Step 4 (Scenario Builder) — the showpiece step. Same Cowork-vs-Claude-Code consideration applies: the contract says Claude Code because verification means running scenarios against the prototype. For the eval, we'll simulate output in Cowork and acknowledge the limitation (no actual Studio loadability test).

---

## 2026-05-04 — Run closed: end-to-end walk complete + eval comparison

**Run state:** `runs/2026-05-third-party-access-eval/` closed. All four pipeline outputs produced (PRD, Rules, Schema Sketch, Scenarios), reviewed, status-flipped per the contracts. Eval comparison written to `05-eval-comparison.md`. Run not merged (eval; canonical AC already exist in `domains/accounts/ac-corpus.md`).

**End-to-end achievement:**
- Adrian's stakeholder email (~5 paragraphs) → 1 PRD (~250 lines) → 22 AC (structured YAML) → no-change schema verdict (with verification tables) → 20 runnable scenarios (with coverage matrix).
- Four specialists handed off through structured artefacts in the run folder.
- PM sign-off discipline applied at every hop.

**Eval verdict (full detail in `05-eval-comparison.md`):**
- Substantive coverage vs reference: ~80%.
- Structural rigour: stronger than reference (anchors, frontmatter, coverage matrices, scenario typing).
- Three real coverage gaps: notifications, First Party state-impact matrix, consent/evidence requirements. Spec Writer biased toward what it can structure (relations, permissions, anchors) and away from process flows.
- One real over-reach: fabricated magnitude numbers. Spec Writer prompt v2 must forbid invented quantitative claims.
- Two voice quibbles: minor copula-avoidance constructions ("represents", "stands as"). Reinforce in Spec Writer prompt.
- Cross-domain revocation cascade and joint-card isolation scenarios — gaps in Scenario Builder output. Both tractable in re-runs.

**Framework status:** Walks end-to-end. Ready to take on a fresh use case (trusteeship, UC-A-11) with the gaps above flagged for the Spec Writer prompt.

**Outstanding items before fresh-use-case run:**
1. Domain-population work: lift the four pending-substrate fragments from `LS-AuthZPM/schemas/entitlements-full-schema.zed` into the framework's `domains/<domain>/schema-fragment.zed`.
2. Spec Writer prompt v2: coverage probing, no-invented-numbers, copula-avoidance reinforcement.
3. Schema Sketcher and Scenario Builder must run in Claude Code (not Cowork) for the next run, because schema additions and Studio verification are both expected.
4. Refactor backlog (RB-001): collapse `use-cases.md` into `ac-corpus.md`. Defer to consolidation pass.

**What this proves to leadership:**
The proving-ground story now has a concrete artefact. A use case enters as an email; valid, regulator-defensible artefacts come out the other end inside an hour of compressed agent work. With domain population and the Spec Writer prompt updates, a fresh use case demo is realistic for week 6 of the original AI-native delivery plan.

---

<!-- Append weekly entries below in the same shape. -->
