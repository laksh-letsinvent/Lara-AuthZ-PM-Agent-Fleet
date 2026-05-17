> _Maintained copy for the agent fleet. Do not sync from `/knowledge` — that copy is archived._

# Google Zanzibar & SpiceDB: A Comprehensive Reference for Entitlements Systems

> A research-backed reference document for PMs implementing fine-grained authorization (FGA) systems in retail banking. Structured for quick lookup and practical application design.

---

## Part 1: Google Zanzibar Fundamentals

### 1.1 What is Zanzibar?

Google Zanzibar is a **global, consistent authorization system** that powers authorization across Google services including Cloud, Drive, and YouTube. It manages over **2 trillion relation tuples** across ~100 terabytes of data.

**Core innovation:** Moving from role-based access control (RBAC) to **relationship-based access control (ReBAC)** — authorization decisions depend on relationships between entities rather than predefined role assignments.

**Why it matters for banking:** ReBAC elegantly handles complex hierarchies (org → account → product) and dynamic delegation patterns, which are native to consumer banking permission models.

---

### 1.2 Core Concept: Relation Tuples

A **relation tuple** is the atomic unit of authorization in Zanzibar. It represents a single relationship in the permission graph.

#### Format

```
<object>#<relation>@<subject>
```

#### Anatomy

| Component | Definition | Banking Example |
|-----------|-----------|-----------------|
| **object** | A resource being controlled | `account:12345` |
| **relation** | The type of relationship | `owner`, `viewer`, `editor` |
| **subject** | A user or group with that relationship | `user:alice` or `team:finance` |

#### Examples

- `document:expense_report_2026#owner@user:alice` — Alice owns the expense report
- `account:checking_acct_789#editor@user:bob` — Bob can edit the checking account
- `organization:bank_branch_01#admin@team:branch_managers` — Branch managers team has admin access

#### Key Rules

- Tuples are **declarative** (state what is true, not what isn't)
- Tuples are **stored and queryable** (unlike computed roles)
- Tuples can reference other tuples (enabling hierarchical permissions)
- Tuples can be timestamped for audit trails

---

### 1.3 Namespace Configuration

Before storing tuples, services must configure **namespaces** — essentially schemas that define:

1. **Object types** (e.g., document, account, organization)
2. **Relations** available on each type (e.g., owner, viewer, editor)
3. **Rewrite rules** that compute permissions from relations
4. **Storage parameters** (sharding, encoding)

#### Namespace Structure

A namespace config specifies:

```
namespace_name:
  - relation: viewer
    comment: "User can view the object"
  - relation: editor
    comment: "User can edit the object"
  - relation: owner
    comment: "User is the owner"
  
  permission: view = viewer + editor + owner
  permission: edit = editor + owner
  permission: admin = owner
```

#### Banking Application

For retail banking, you might define:

```
namespace account:
  - relation: owner
  - relation: beneficiary
  - relation: delegate
  
  permission: access = owner + delegate
  permission: transfer = owner + delegate
  permission: view_statements = owner + beneficiary
```

---

### 1.4 Zanzibar's Five Core APIs

Zanzibar provides five APIs for authorization operations:

#### 1. **Check API** — Permission Verification

Determines if a subject has a specific permission on an object.

**Parameters:**
- `object` — The resource being checked
- `relation` — The permission/relation type
- `subject` — The user/entity being checked
- `zookie` — Timestamp specifying consistency level (see Section 2.2)

**Returns:**
- Boolean (permitted/denied)

**Use case in banking:** "Can user:bob transfer funds from account:checking_789?"

---

#### 2. **Expand API** — Permission Graph Exploration

Computes all subjects that have a particular permission on a resource. Follows indirect references through rewrite rules.

**Returns:** A userset tree showing:
- Leaf nodes: specific users
- Intermediate nodes: union (+), intersection (&), exclusion (-) operators

**Use case in banking:** "Who has access to account:savings_456?" (surfaces all owners, delegates, and indirect access paths)

---

#### 3. **Read API** — Tuple Retrieval

Retrieves stored tuples matching a filter. Simple CRUD operation for reading relationships.

**Parameters:**
- Object filter (optional)
- Relation filter (optional)
- Subject filter (optional)

**Use case in banking:** Audit trail — "Show all tuples for account:checking_789"

---

#### 4. **Write API** — Tuple Mutation

Creates or updates tuples. Uses optimistic concurrency control.

**Process:**
1. Client reads all tuples for an object (includes per-object lock tuple)
2. Client modifies desired tuples
3. Client writes back; Zanzibar checks if lock tuple unchanged
4. If lock unchanged, write succeeds; otherwise, retry

**Use case in banking:** "Grant user:charlie delegate access to account:business_acct_001"

---

#### 5. **Watch API** — Change Subscription

Subscribes to real-time tuple modification events (create, update, delete).

**Returns:** Ordered stream of modification events with timestamps

**Use case in banking:** Real-time audit logging, permission sync to downstream systems, triggering compliance checks

---

### 1.5 Consistency Model: Zookies & Snapshots

Zanzibar's consistency model solves the **"new enemy" problem** — ensuring that ACL changes and content updates respect causal ordering.

#### The New Enemy Problem

**Scenario:**
1. Alice removes Bob from a folder's permissions
2. Alice adds new documents to the folder
3. Bob shouldn't see the new documents

**Problem:** If the system uses stale ACLs, Bob might see documents he shouldn't access due to race conditions between ACL and content updates.

#### Solution: Zookies

A **zookie** is an opaque byte sequence encoding a globally meaningful timestamp. It captures:
- ACL write timestamp
- Client content version
- Read snapshot point-in-time

**How it works:**
- When performing ACL reads or checks, include a zookie in the request
- Zookie specifies the staleness bound for the snapshot read
- Zanzibar guarantees consistency at least as fresh as the zookie timestamp

#### Consistency Guarantees

Zanzibar provides **external consistency** with **snapshot reads of bounded staleness** through the zookie protocol:

- **Respects causal ordering** between ACL and content updates
- **Bounds staleness** while allowing Zanzibar freedom to choose timestamps for latency/availability optimization
- Uses **"at-least-as-fresh" semantics** — can use any timestamp fresher than the zookie-encoded timestamp

**Implication for banking:** When checking permission before a money transfer, you can ensure the permission check reflects ACL changes from the past N seconds, preventing race condition exploits.

---

### 1.6 Terminology Mapping: Zanzibar → SpiceDB

| Zanzibar Term | SpiceDB Equivalent | Definition |
|---|---|---|
| **Namespace** | **Definition** | Schema defining object types and relations |
| **Relation tuple** | **Relationship** | Atomic permission unit (subject-relation-object) |
| **Userset rewrite** | **Permission** | Computed set from relations using set operations |
| **Zookie** | **ZedToken** | Timestamp/version for consistency control |
| **Check API** | **CheckPermission** | Verify if subject has permission |
| **Expand API** | **LookupResources** / **LookupSubjects** | Find accessible resources or subjects |
| **Read API** | **ReadRelationships** | Retrieve stored relationships |
| **Write API** | **WriteRelationships** | Create/update relationships |
| **Watch API** | **Watch** | Subscribe to relationship changes |

---

## Part 2: SpiceDB Deep Dive

### 2.1 What is SpiceDB?

SpiceDB is an **open-source, Google Zanzibar-inspired authorization database** maintained by AuthZed. It's built on the same principles as Zanzibar but designed for ease of deployment and integration into custom applications.

**Key characteristics:**
- Implements Zanzibar's ReBAC model in open source
- Purpose-built for fine-grained authorization (FGA)
- Used in production by enterprises like OpenAI, handling billions of fine-grained permissions
- Provides a developer-friendly schema language inspired by Zanzibar's configuration

---

### 2.2 Schema Language Fundamentals

SpiceDB schemas define **definitions** (analogous to Zanzibar namespaces) that specify object types, relations, and computed permissions.

#### Basic Structure

```
definition object_type {
  relation relation_name: allowed_subject_type
  permission permission_name = relation_name
}
```

#### Components

| Component | Role | Constraints |
|-----------|------|-------------|
| **definition** | Object type (e.g., user, account, document) | Lowercase, snake_case |
| **relation** | Relationship type (named as nouns) | Defines how objects relate |
| **allowed_subject_type** | Who/what can hold this relation | Can be multiple types using `\|` |
| **permission** | Computed set (named as adjectives) | Derived from relations using set operations |

#### Example: Banking Account Schema

```
definition user {}

definition account {
  relation owner: user
  relation delegate: user
  relation beneficiary: user
  
  permission access = owner | delegate
  permission transfer = owner | delegate
  permission view_statements = owner | beneficiary | delegate
}
```

---

### 2.3 Relations: The Building Blocks

**Relations** define how two objects (or object and subject) can relate. They're named as **nouns** and must reference a `definition` of allowed subjects.

#### Basic Syntax

```
relation relation_name: allowed_type
```

#### Multiple Allowed Types

```
definition document {
  relation editor: user | admin_group
  relation viewer: user | public_group | team#member
}
```

The `|` (pipe) operator allows multiple subject types. In the example:
- `user` — a direct user reference
- `admin_group` — another definition (group)
- `team#member` — a user with a specific relation on another object (indirect subject)

#### Practical Banking Example

```
definition organization {
  relation admin: user | admin_team
  relation member: user
}

definition account {
  relation owner: user
  relation organization: organization  // Account belongs to an org
  relation delegate: user
  
  // Org admins have implicit access to org's accounts
  permission org_admin_access = organization#admin
  permission owner_access = owner | delegate
  permission full_access = owner_access | org_admin_access
}
```

---

### 2.4 Permissions: Computed Authorization

**Permissions** are derived from relations using **set operations**. They're named as **adjectives** and represent computed entitlements.

#### Set Operations

| Operation | Symbol | Meaning | SQL Analogy |
|-----------|--------|---------|------------|
| **Union** | `+` | OR (any condition) | `SELECT * FROM a UNION SELECT * FROM b` |
| **Intersection** | `&` | AND (all conditions) | `SELECT * FROM a INTERSECT SELECT * FROM b` |
| **Exclusion** | `-` | NOT (subtract) | `SELECT * FROM a EXCEPT SELECT * FROM b` |

#### Examples

```
definition document {
  relation writer: user
  relation reader: user
  relation banned: user
  
  // Simple union: can view if reader OR writer
  permission view = reader + writer
  
  // Intersection: can edit only if writer AND not banned
  permission edit = writer - banned
  
  // Complex: can manage if writer AND not banned AND org_admin
  permission manage = (writer + org_admin) - banned
}
```

#### Permission Computation Flow

When checking a permission:

1. **Evaluate all relations** in the expression
2. **Apply set operations** (union, intersection, exclusion)
3. **Return the computed set** of subjects with that permission
4. **Check if subject is in set** to determine permission

**Critical rule:** You can **write to relations only**, not permissions. Permissions are computed, read-only views. This ensures you can safely refactor permission logic without updating stored data.

---

### 2.5 Advanced: Caveats (Conditional Permissions)

**Caveats** are conditional expressions attached to relationships that enable **attribute-based access control (ABAC)**. A relationship with a caveat only applies if the caveat expression evaluates to true.

#### Definition Syntax

```
caveat caveat_name(context_param: type_name) {
  expression_returning_boolean
}
```

#### Usage in Relations

```
definition document {
  // A simple relation
  relation editor: user
  
  // A caveated relation: editor only if within business hours
  relation temp_editor: user with business_hours_caveat
}

caveat business_hours_caveat(request_time: timestamp) {
  // Returns true if current time is within business hours (9-5 UTC)
  request_time.getHours('UTC') >= 9 && request_time.getHours('UTC') < 17
}
```

#### Practical Banking Examples

```
caveat transaction_limit(amount: int, user_limit: int) {
  amount <= user_limit
}

caveat ip_restricted(request_ip: string, allowed_ips: string_list) {
  request_ip in allowed_ips
}

caveat time_window(request_time: timestamp, start: timestamp, end: timestamp) {
  request_time >= start && request_time <= end
}

definition account {
  relation owner: user
  
  // Delegate can transfer up to $5000 per transaction
  relation delegate: user with transaction_limit
  
  // High-value access restricted to office IPs
  relation high_value_admin: user with ip_restricted
  
  // Temporary access during business hours only
  relation temp_support: user with business_hours_caveat
}
```

#### Permission States with Caveats

When checking a caveated permission, SpiceDB returns one of three states:

| State | Meaning |
|-------|---------|
| **PERMISSIONSHIP_HAS_PERMISSION** | Clear "yes" — all conditions met |
| **PERMISSIONSHIP_NO_PERMISSION** | Clear "no" — subject lacks access |
| **PERMISSIONSHIP_CONDITIONAL_PERMISSION** | "Maybe" — missing context needed to determine (client must provide context to resolve) |

#### Performance Consideration

**⚠️ Warning:** Caveats incur a **performance penalty**. Caveated relationships are harder to cache and slow graph walks. Use only for:
- Context available at request time (IP, timestamp, amount)
- ABAC logic that can't be expressed as relationships
- Avoid over-caveating; use for exceptional cases, not the rule

---

### 2.6 Wildcards: Public & Anonymous Access

**Wildcards** (`user:*`) allow granting permissions to all users or public access.

#### Syntax

```
relation viewer: user | user:*
```

This means: "Either a specific user OR any user (wildcard)"

#### Practical Banking Examples

```
definition article {
  relation author: user
  relation internal_viewer: user
  relation public_viewer: user | user:*  // Public articles
  
  permission read = author + internal_viewer + public_viewer
}

definition account {
  relation owner: user
  relation public_readonly: user:*  // Public viewing (rare in banking)
}
```

#### Security Best Practices

⚠️ **Use wildcards cautiously:**
- Grant them only to **read permissions**, not write/transfer/admin
- Avoid wildcards in **intersection or exclusion** operations (security advisory: they can be bypassed in Lookup operations)
- Prefer explicit allowlists over blanket wildcards
- Audit wildcard usage in banking contexts closely (regulatory risk)

---

### 2.7 SpiceDB Core APIs

SpiceDB provides five primary APIs corresponding to Zanzibar's operations.

#### CheckPermission

Determines if a subject has a specific permission on a resource.

**Request:**
```
{
  resource: { type: "account", id: "checking_789" },
  permission: "transfer",
  subject: { object: { type: "user", id: "alice" } },
  consistency: { at_least_as_fresh: zedtoken }
}
```

**Response:**
```
{
  permissionship: PERMISSIONSHIP_HAS_PERMISSION,
  checked_at: zedtoken
}
```

**Use in banking:**
- Pre-authorization checks before money transfers
- Display/hide UI controls based on permissions
- Enforce permission on API endpoints

---

#### WriteRelationships

Creates or updates relationships between objects and subjects.

**Request:**
```
{
  updates: [
    {
      operation: OPERATION_CREATE,
      relationship: {
        resource: { type: "account", id: "checking_789" },
        relation: "delegate",
        subject: { object: { type: "user", id: "bob" } }
      }
    }
  ]
}
```

**Response:**
```
{
  written_at: zedtoken
}
```

**Use in banking:**
- Grant user access to account (onboarding)
- Establish delegation relationships (power of attorney)
- Update account ownership

---

#### LookupResources

Finds all resources where a subject has a specific permission. Walks the permission graph "backwards."

**Request:**
```
{
  resource_type: "account",
  permission: "transfer",
  subject: { object: { type: "user", id: "alice" } },
  consistency: { at_least_as_fresh: zedtoken }
}
```

**Response:**
```
{
  results: [
    { resource_id: "checking_789" },
    { resource_id: "savings_456" },
    { resource_id: "business_001" }
  ]
}
```

**Use in banking:**
- Populate user dashboard with accounts they can access
- Filter account lists based on permissions
- Regulatory reporting (enumerate what user can access)

---

#### LookupSubjects

Finds all subjects with a specific permission on a resource. Reverse of LookupResources.

**Request:**
```
{
  resource: { type: "account", id: "checking_789" },
  permission: "view_statements",
  subject_type: "user"
}
```

**Response:**
```
{
  subjects: [
    { subject: { type: "user", id: "alice" } },
    { subject: { type: "user", id: "bob" } }
  ]
}
```

**Use in banking:**
- Audit: "Who can view this account's statements?"
- Permission management UI: show current access holders
- Compliance: enumerate access for regulatory review

---

#### ReadRelationships

Retrieves stored relationships matching filters. Simple CRUD read.

**Request:**
```
{
  resource_filter: { type: "account", id: "checking_789" },
  relation_filter: "delegate"
}
```

**Response:**
```
{
  relationships: [
    {
      resource: { type: "account", id: "checking_789" },
      relation: "delegate",
      subject: { type: "user", id: "bob" }
    }
  ]
}
```

**Use in banking:**
- Audit trail queries
- Account reconciliation
- Permission backups/exports

---

#### DeleteRelationships

Deletes relationships matching filters. Transactional bulk delete.

**Request:**
```
{
  resource_filter: { type: "account", id: "checking_789" },
  relation_filter: "delegate",
  subject_filter: { type: "user", id: "bob" }
}
```

**Response:**
```
{
  deleted_at: zedtoken,
  deletion_progress: PROGRESS_COMPLETE
}
```

**Use in banking:**
- Revoke delegation (power of attorney ends)
- Offboard user (remove all account access)
- Correct access errors

---

### 2.8 Watch API: Real-Time Change Streaming

SpiceDB Watch API subscribes to real-time relationship changes (create, update, delete).

**Use case in banking:**
- Audit logging system subscribing to permission changes
- Real-time permission cache invalidation
- Compliance events (e.g., "User X added to high-value account")
- Downstream system sync (sync permissions to payment system)

---

### 2.9 Consistency Model in SpiceDB

SpiceDB offers three consistency options per request, using **ZedTokens** (analogous to Zookies):

#### 1. **Fully Consistent** ❌ Not Recommended

Forces the most recent datastore revision.

**Trade-off:** Highest accuracy, but lowest cache hit rate, highest latency/load.

```
consistency: { fully_consistent: true }
```

---

#### 2. **At Least As Fresh** ✅ Recommended

Uses any cached snapshot fresher than the provided ZedToken.

**Trade-off:** Balances consistency and performance. Use when you need to respect causal ordering (e.g., ACL change → content access check).

```
consistency: { 
  at_least_as_fresh: previous_zedtoken  // From prior write
}
```

**Use in banking:**
- Permission check after revoking access (prevents new enemy problem)
- Auditing that respects ordered events

---

#### 3. **Minimize Latency** ⚡ Fast But Risky

Uses whatever is in cache, even if stale.

**Trade-off:** Fastest performance, but can create race conditions (new enemy problem).

```
consistency: { minimize_latency: {} }
```

**Use in banking:**
- Read-heavy UI operations (display list of accounts)
- Low-risk checks (viewing old statements)
- NOT for authorization before transactions

---

#### ZedTokens

A **ZedToken** is an opaque byte sequence encoding a point-in-time timestamp. Returned by every SpiceDB API response.

**Pattern:**
1. Write permission → returns ZedToken T1
2. Subsequent check request includes `at_least_as_fresh: T1`
3. Check is guaranteed to reflect the write from T1

**This solves the new enemy problem by respecting causal ordering.**

---

## Part 3: Schema Design Patterns for Banking

### 3.1 Hierarchical Permissions (Org → Account → Product)

Most retail banking systems need multi-level hierarchies: organizations → accounts → products.

#### Schema

```
definition user {}

definition organization {
  relation admin: user
  relation member: user
}

definition account {
  relation organization: organization
  relation owner: user
  relation delegate: user
  relation beneficiary: user
  
  permission org_admin = organization#admin
  permission full_control = owner | delegate
  permission read_only = beneficiary | delegate | org_admin
}

definition transaction {
  relation account: account
  relation initiator: user
  
  permission approve = account#full_control
  permission view = account#read_only
}
```

#### Permission Flow

```
User has "approve" on Transaction
  ↓
Is user in Transaction#account#full_control?
  ↓
Transaction linked to Account
  ↓
Is user in Account#full_control?
  ↓
Full control = owner | delegate
  ↓
Is user Account#owner OR Account#delegate?
  ↓
[Check specific relationships]
```

#### Key Principle

**Arrow notation** (`→` or `#`) represents graph traversal. `account#owner` means "follow the account relation to the organization object, then check admin on that organization."

---

### 3.2 Role-Based Access Control (RBAC) on Top of ReBAC

Simple RBAC can be layered using relations representing roles.

#### Schema

```
definition user {}

definition role {
  relation member: user
}

definition account {
  relation admin_role: role
  relation editor_role: role
  relation viewer_role: role
  
  // Permissions grant access through role membership
  permission admin = admin_role#member
  permission edit = editor_role#member + admin
  permission view = viewer_role#member + edit
}
```

#### Assigning Users to Roles

```
WriteRelationships:
  role:admin_team#member@user:alice      // Alice is member of admin_team
  account:checking_789#admin_role@role:admin_team  // account delegates to admin_team
```

Now Alice has admin access to the account through role membership.

---

### 3.3 Delegation Patterns

Delegation allows users to grant limited access to other users (power of attorney, account management).

#### Schema

```
definition user {}

definition account {
  relation owner: user
  relation delegate: user
  
  // Delegation constraint: delegates can't grant access themselves
  permission can_delegate = owner
  permission can_access = owner | delegate
}

definition delegation {
  relation delegating_user: user
  relation delegated_to: user
  relation on_account: account
  relation expires_at: timestamp  // Caveat
  
  caveat delegation_active(request_time: timestamp, expiry: timestamp) {
    request_time < expiry
  }
  
  relation delegation: user with delegation_active
}
```

**Constraint enforcement:** The schema allows only `owner` to have `can_delegate` permission. This is enforced at the application layer — the schema enables it, but your application must validate.

---

### 3.4 Conditional/Contextual Permissions with Caveats

Use caveats for context-dependent rules that can't be stored as static relationships.

#### Schema

```
caveat ip_restricted(request_ip: string, allowed_ips: list) {
  request_ip in allowed_ips
}

caveat transaction_amount_limit(amount: int, limit: int) {
  amount <= limit
}

caveat business_hours(request_time: timestamp) {
  request_time.getHours('UTC') >= 9 && request_time.getHours('UTC') < 17
}

definition account {
  relation owner: user
  
  // Unlimited access for owner
  relation delegate: user
  
  // Limited access for support staff (office hours only, IP restricted, $5k/day)
  relation support_staff: user with business_hours with ip_restricted
  
  permission transfer = owner | (delegate with transaction_amount_limit)
  permission admin = owner
}
```

#### CheckPermission with Caveats

```
CheckPermission:
  resource: account:checking_789
  permission: transfer
  subject: user:charlie
  consistency: at_least_as_fresh
  context: {
    amount: 3000,
    limit: 5000,
    request_time: 2026-03-15T14:30:00Z,
    request_ip: "192.168.1.100",
    allowed_ips: ["10.0.0.0/8", "172.16.0.0/12"]
  }

Response: PERMISSIONSHIP_HAS_PERMISSION (all caveats satisfied)
```

---

## Part 4: Implementation Patterns for Retail Banking

### 4.1 Multi-Tenant Architecture

In multi-tenant systems (SaaS banking platform), permission models often need tenant isolation.

#### Approach 1: Tenant as Root Object

```
definition tenant {}

definition organization {
  relation tenant: tenant
  relation admin: user
}

definition account {
  relation organization: organization
  relation owner: user
  
  permission org_admin = organization#admin
  permission owner_access = owner | org_admin
}
```

Each organization belongs to a tenant. Permission checks implicitly scope to the tenant through the organization.

#### Approach 2: Tenant in Caveat

```
caveat same_tenant(request_tenant_id: string, resource_tenant_id: string) {
  request_tenant_id == resource_tenant_id
}

definition account {
  relation tenant: tenant with same_tenant
  relation owner: user
}
```

Pass tenant context in caveat to enforce isolation per request.

#### Session Pattern

Common implementation:
1. User authenticates → session contains `tenant_id`
2. All permission checks include tenant caveat context
3. Prevents cross-tenant leaks even if schema has bugs

---

### 4.2 Audit & Compliance

#### Pattern 1: Permission Audit Trail

Use Watch API to subscribe to permission changes:

```
Watch:
  namespaces: ["account", "delegation", "user"]
  
// Events flow to audit log:
{
  timestamp: 2026-03-15T14:30:00Z,
  operation: "create",
  relationship: {
    resource: "account:checking_789",
    relation: "delegate",
    subject: "user:bob"
  },
  initiated_by: "user:alice"
}
```

#### Pattern 2: Access Review Reports

Use LookupSubjects to generate who-has-access reports:

```
For each account in portfolio:
  LookupSubjects(account, "transfer") 
    → list of users who can transfer funds
  LookupSubjects(account, "admin")
    → list of admins
  
Generate compliance report: 
  "Account XYZ has 3 admins, 2 transfer delegates, 5 readonly viewers"
```

---

### 4.3 Performance Optimization

#### 1. Schema Simplification

Minimize deep graph traversals. This schema requires 3 hops:

```
❌ user → delegation → account → transaction
```

Better to denormalize:

```
✅ user → transaction directly, with account relation for context
```

#### 2. Caching Strategy

- **Use `minimize_latency`** for high-volume reads (balance display)
- **Use `at_least_as_fresh`** only after writes (permission changes)
- Cache ZedTokens from recent writes; reuse in subsequent requests

#### 3. Materialize Plugin (if available)

If running SpiceDB with Materialize plugin, pre-compute expensive permission paths:

```
Define "materialized" permissions that Materialize pre-computes continuously
→ Dramatic speedup for LookupResources/LookupSubjects queries
```

---

## Part 5: Terminology Quick Reference

### Zanzibar Core Terms

| Term | Definition | Banking Example |
|------|-----------|-----------------|
| **Relation Tuple** | Atomic permission unit (subject-relation-object) | `account:789#owner@user:alice` |
| **Namespace** | Schema defining object/relation types | "account" namespace |
| **Userset Rewrite** | Rule computing permission from relations | `transfer = owner \| delegate` |
| **ACL** | Access Control List (collection of tuples) | All tuples for account:789 |
| **Zookie** | Timestamp for consistency control | Encode last write time |
| **New Enemy Problem** | Race condition when ACL and content updates conflict | ACL revoked, but stale content still visible |
| **Check** | Query if subject has permission | "Can Alice transfer?" |
| **Expand** | Find all subjects with permission | "Who can transfer?" |

### SpiceDB Core Terms

| Term | Definition | Banking Example |
|------|-----------|-----------------|
| **Definition** | Object type in schema | `definition account {}` |
| **Relation** | Relationship type on an object | `relation owner: user` |
| **Permission** | Computed set derived from relations | `permission transfer = owner \| delegate` |
| **Caveat** | Conditional expression on relationship | `with ip_restricted` |
| **ZedToken** | Consistency timestamp (SpiceDB's zookie) | Returned by all API calls |
| **ReBAC** | Authorization model based on relationships | Instead of static roles |
| **Wildcard** | Grant access to all users | `user:*` |
| **Subject** | User or object holding a relation | `user:alice` or `team:finance` |

---

## Part 6: Key Insights for PMs

### 1. **Trust is the product.** Every permission decision is a security decision. Schema mistakes have audit/compliance consequences.

### 2. **Friction has a cost.** Extra permission checks add latency. Design for simplicity; complex hierarchies slow down permission evaluation.

### 3. **Consistency is a trade-off.** Fully consistent = slow. Minimize latency = potentially stale. Use ZedTokens to balance.

### 4. **Caveats are escape hatches.** If permission logic can be expressed as relationships, do that. Caveats (ABAC) are powerful but slower.

### 5. **Schema changes are safe.** Permissions are derived, not stored. Refactor permission logic anytime without touching the database.

### 6. **Graph traversal depth matters.** Shallow hierarchies (user → account) are fast. Deep hierarchies (user → team → org → account → product) are slow.

### 7. **Audit the access, not just the action.** Use LookupSubjects to enumerate who has access. Essential for compliance.

---

## Sources

Research for this document was conducted against authoritative sources:

- [Google Zanzibar - Authzed Docs](https://authzed.com/docs/spicedb/concepts/zanzibar)
- [The Google Zanzibar Paper, Annotated by AuthZed](https://authzed.com/zanzibar)
- [Zanzibar: Google's Consistent, Global Authorization System (USENIX)](https://www.usenix.org/system/files/atc19-pang.pdf)
- [SpiceDB Schema Language Reference - AuthZed Docs](https://authzed.com/docs/spicedb/concepts/schema)
- [SpiceDB Concepts: Relationships](https://authzed.com/docs/spicedb/concepts/relationships)
- [Caveats - AuthZed Docs](https://authzed.com/docs/spicedb/concepts/caveats)
- [SpiceDB Consistency Model](https://authzed.com/docs/spicedb/concepts/consistency)
- [ZedTokens/Zookies - AuthZed](https://authzed.com/blog/zedtokens)
- [New Enemies Problem - AuthZed](https://authzed.com/blog/new-enemies)
- [SpiceDB Best Practices](https://authzed.com/docs/best-practices)
- [Schema Language Patterns](https://authzed.com/blog/schema-language-patterns)
- [Relationship-Based Access Control (ReBAC) Academy - OSO](https://www.osohq.com/academy/relationship-based-access-control-rebac)
- [How Caching Works in SpiceDB](https://authzed.com/blog/how-caching-works-in-spicedb)
- [SpiceDB Consistency: Performance vs. Accuracy Trade-offs](https://akoserwal.medium.com/spicedb-consistency-a-deep-dive-into-performance-vs-accuracy-trade-offs-76e2fb2f29b9)

