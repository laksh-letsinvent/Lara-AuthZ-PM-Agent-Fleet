# Knowledge Base

Reference material the agent fleet reads from. Stable. Not modified as part of normal work.

Specialists load from here when they need to know how Zanzibar works, what schema patterns exist, what the SpiceDB API surface is, or what banking and regulatory conventions apply at the domain level. Each specialist's contract names which files it reads.

## What's in here

| File | What it is | When a specialist reads it |
|---|---|---|
| `zanzibar-spicedb-reference.md` | Comprehensive reference on Zanzibar concepts and SpiceDB syntax | Schema Sketcher (always), Rule Lister (when AC involves consistency or caveats) |
| `schema-design-patterns.md` | 12 ready-to-use schema patterns (delegation, hierarchy, RBAC, caveats, exclusion) | Schema Sketcher (always) |
| `spicedb-api-reference.md` | All 7 SpiceDB APIs with banking examples and consistency strategy | Scenario Builder (always) |
| `banking-domain-context.md` | Business context across Accounts, Payments, Cards, Comms, Customer Mgmt | Spec Writer (always), Rule Lister (when use case spans domains) |
| `delegation-use-cases.md` | Detailed use case reference with regulatory context | Spec Writer (when use case involves delegation), Rule Lister (always) |

## Updating these

Don't edit casually. These are reference artefacts. Update only when:

- SpiceDB or Zanzibar releases something material (new API, new caveat behaviour)
- Banking regulation shifts in a way that changes a domain conventions
- A pattern in `schema-design-patterns.md` is proven wrong by something the platform actually does

When you update, note the change at the top of the file with a date. Don't re-version the whole file.

## Why duplicates and not symlinks

The originals in `/knowledge` are archived. These copies are the live versions for the framework, so the framework folder is portable as one unit. When this ports to work, you move `Lara-AuthZ-Agent-Fleet/` and everything it depends on comes with it. Symlinks would break that.
