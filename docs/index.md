---
hide:
  - navigation
  - toc
---

<div class="hero">
  <div class="hero-inner">
    <div class="hero-badge">Entitlements Platform · Lara Banks</div>
    <h1 class="hero-title">AuthZ Pipeline</h1>
    <p class="hero-sub">Fine-grained authorization for retail banking — powered by Google Zanzibar via SpiceDB. One framework, every delegation pattern, full regulatory traceability.</p>
    <div class="hero-actions">
      <a href="pipeline/" class="hero-btn-primary">View Pipeline →</a>
      <a href="runs/" class="hero-btn-secondary">Active Runs</a>
    </div>
  </div>
</div>

## What's here

<div class="grid-cards">

<div class="grid-card">
  <div class="card-icon">⚡</div>
  <div class="card-content">
    <h3><a href="pipeline/">Pipeline</a></h3>
    <p>The end-to-end delivery chain. Triage → Spec Writer → Rule Lister → Scenario Builder → Schema Handoff. How a BA email becomes approved AC and a TL brief.</p>
  </div>
</div>

<div class="grid-card">
  <div class="card-icon">📁</div>
  <div class="card-content">
    <h3><a href="runs/">Runs</a></h3>
    <p>Active and completed use case runs. Each run traces from stakeholder brief to signed-off AC and schema handoff. Joint account baseline is the first completed run.</p>
  </div>
</div>

<div class="grid-card">
  <div class="card-icon">🏦</div>
  <div class="card-content">
    <h3><a href="domains/accounts/">Domains</a></h3>
    <p>AC corpus and regulatory anchors per consuming domain — Accounts, Payments, Cards, Communications, Customer Management. Accounts is live; others in progress.</p>
  </div>
</div>

<div class="grid-card">
  <div class="card-icon">📚</div>
  <div class="card-content">
    <h3><a href="knowledge-base/delegation-use-cases/">Knowledge Base</a></h3>
    <p>Zanzibar & SpiceDB reference, schema design patterns, SpiceDB API, banking domain context, delegation use cases. The technical foundation the pipeline runs on.</p>
  </div>
</div>

<div class="grid-card">
  <div class="card-icon">⚖️</div>
  <div class="card-content">
    <h3><a href="schema/permission-matrix/">Permission Matrix</a></h3>
    <p>Cross-domain permission reference. What each subject can do on each resource type. Derived from merged AC across all completed runs.</p>
  </div>
</div>

<div class="grid-card">
  <div class="card-icon">🛠️</div>
  <div class="card-content">
    <h3><a href="skills/">Framework</a></h3>
    <p>Skills, specialist contracts, output forms, and style guide. The portable layer — unchanged when you port this framework to a new org.</p>
  </div>
</div>

</div>

---

## Pipeline at a glance

| Step | Specialist | Input | Output | Gate |
|------|-----------|-------|--------|------|
| 00 | Triage | Inbox file | Run card + verdict | PM confirms scope |
| 01 | Spec Writer | Run card | PRD | PM signs off |
| 02 | Rule Lister | PRD | AC corpus | PM signs off |
| 03 | Scenario Builder | AC | Runnable scenarios | PM signs off |
| 04 | Schema Handoff | Scenarios + AC | TL brief | TL receives |
| 05 _(optional)_ | Schema Sketch | Scenarios | Draft `.zed` proposals | TL reviews |

## Current coverage

| Domain | Use case | Status |
|--------|----------|--------|
| Accounts | Joint current account — access and delegation baseline | ✅ Merged |
| Payments | — | Not started |
| Cards | — | Not started |
| Communications | — | Not started |
| Customer Management | — | Not started |
