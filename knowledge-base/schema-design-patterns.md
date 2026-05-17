> _Maintained copy for the agent fleet. Do not sync from `/knowledge` — that copy is archived._

# SpiceDB Schema Design Patterns for Retail Banking

Quick reference for common entitlements patterns in consumer banking.

---

## Pattern 1: Simple Account Access

**Use case:** Basic account owner and delegate access.

```
definition user {}

definition account {
  relation owner: user
  relation delegate: user
  
  permission transfer = owner | delegate
  permission view_statements = owner | delegate
  permission admin = owner
}
```

**Writing relationships:**
```
account:checking_789#owner@user:alice
account:checking_789#delegate@user:bob
```

**Checking permission:**
```
CheckPermission(
  resource: account:checking_789,
  permission: transfer,
  subject: user:bob
)
→ PERMISSIONSHIP_HAS_PERMISSION
```

---

## Pattern 2: Organization with Inherited Access

**Use case:** Users have permissions through org membership.

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
  
  permission org_admin = organization#admin
  permission full_access = owner | delegate | org_admin
  permission read_only = org_admin | owner
}
```

**Writing relationships:**
```
organization:bank_branch_01#admin@user:alice
account:checking_789#organization@organization:bank_branch_01
account:checking_789#owner@user:bob
```

**Permission flow:**
- User alice is admin of organization:bank_branch_01
- Account checking_789 belongs to that organization
- Therefore alice has org_admin access to checking_789

---

## Pattern 3: Hierarchical Permissions (Org → Team → Account)

**Use case:** Nested organizational structure with cascading permissions.

```
definition user {}

definition team {
  relation organization: organization
  relation lead: user
  relation member: user
}

definition organization {
  relation super_admin: user
  relation admin: user
}

definition account {
  relation organization: organization
  relation team: team
  relation owner: user
  
  permission org_super_admin = organization#super_admin
  permission org_admin = organization#admin
  permission team_lead = team#lead
  permission is_owner = owner
  
  permission full_control = is_owner | team_lead | org_admin | org_super_admin
  permission read_only = full_control
}
```

**Relationship graph:**
```
user:alice
  ↓
organization#super_admin (org:HQ)
  ↓
account#organization (account:checking_789)
  ↓
permission: full_control ✓
```

---

## Pattern 4: Role-Based Assignment

**Use case:** Assign users to roles, roles grant permissions.

```
definition user {}

definition role {
  relation member: user
  // Optionally: relation restricted_to_accounts: account
}

definition account {
  relation account_admin: role
  relation account_operator: role
  relation account_viewer: role
  
  permission admin = account_admin#member
  permission operate = account_operator#member | admin
  permission view = account_viewer#member | operate
}
```

**Writing relationships:**
```
role:finance_admins#member@user:alice
role:finance_admins#member@user:bob
account:checking_789#account_admin@role:finance_admins
```

**Effect:** Both alice and bob have admin access to checking_789 through role membership.

**Advantage over static RBAC:** Role definitions are stored as relationships. Adding/removing users from roles is a single write. Changing role permissions requires only schema change, no data updates.

---

## Pattern 5: Delegation with Expiry

**Use case:** User grants temporary access to another user (power of attorney, temporary delegate).

```
definition user {}

caveat is_valid_delegation(request_time: timestamp, expires_at: timestamp) {
  request_time < expires_at
}

definition account {
  relation owner: user
  relation delegate: user with is_valid_delegation
  
  permission transfer = owner | delegate
}
```

**Writing a temporary delegation (expires 2026-06-15):**
```
WriteRelationships:
  resource: account:checking_789
  relation: delegate
  subject: user:bob
  caveat_context: { expires_at: 2026-06-15T00:00:00Z }
```

**Checking permission:**
```
CheckPermission(
  resource: account:checking_789,
  permission: transfer,
  subject: user:bob,
  context: { request_time: 2026-03-15T14:30:00Z }
)
→ PERMISSIONSHIP_HAS_PERMISSION (before expiry)

// Later...
CheckPermission(
  ...
  context: { request_time: 2026-06-16T14:30:00Z }
)
→ PERMISSIONSHIP_NO_PERMISSION (after expiry)
```

---

## Pattern 6: Conditional Access (IP, Time, Amount)

**Use case:** Grant access only under certain conditions (support access during business hours, transfer limits, office network only).

```
definition user {}

caveat office_hours(request_time: timestamp) {
  request_time.getHours('UTC') >= 9 && request_time.getHours('UTC') < 17
}

caveat office_network(request_ip: string) {
  request_ip.isPrivateIP()  // Or check against allowlist
}

caveat transfer_limit(amount: int, limit: int) {
  amount <= limit
}

definition account {
  relation owner: user
  relation delegate: user
  
  // Support staff: office hours only, office network only
  relation support_agent: user with office_hours with office_network
  
  permission owner_transfer = owner  // No limits
  permission delegate_transfer = delegate with transfer_limit
  permission support_transfer = support_agent with transfer_limit
  
  permission all_transfer = owner_transfer | delegate_transfer | support_transfer
}
```

**Checking delegate with limit:**
```
CheckPermission(
  resource: account:checking_789,
  permission: delegate_transfer,
  subject: user:charlie,
  context: {
    amount: 500,  // Amount being transferred
    limit: 1000   // Delegate's daily limit
  }
)
→ PERMISSIONSHIP_HAS_PERMISSION
```

**Checking support agent (must satisfy all caveats):**
```
CheckPermission(
  resource: account:checking_789,
  permission: support_transfer,
  subject: user:support_1,
  context: {
    request_time: 2026-03-15T10:00:00Z,  // Within 9-17 UTC
    request_ip: 10.0.1.50,                // Office IP
    amount: 500,
    limit: 2000
  }
)
→ PERMISSIONSHIP_HAS_PERMISSION (all conditions met)
```

---

## Pattern 7: Public/Anonymous Access (Read-Only)

**Use case:** Public information accessible to any user (public statements, policy docs, etc.).

```
definition user {}

definition account {
  relation owner: user
  relation public_reader: user:*  // Wildcard: any user
  
  permission view_public_info = public_reader
  permission view_full = owner | public_reader
}
```

**Writing public access:**
```
account:public_info_789#public_reader@user:*
```

Now any user in the system can read public_info_789.

⚠️ **Security notes:**
- Only grant wildcards to read/view permissions
- Avoid wildcards in complex permission expressions (intersection, exclusion)
- Audit wildcard usage for compliance

---

## Pattern 8: Exclusion (Banned/Revoked Access)

**Use case:** User has access but is explicitly banned from it (e.g., dispute period).

```
definition user {}

definition account {
  relation owner: user
  relation delegate: user
  relation banned: user
  
  permission can_access = (owner | delegate) - banned
  permission can_transfer = can_access  // No transfers while banned
}
```

**Scenario:**
```
account:checking_789#owner@user:alice
account:checking_789#delegate@user:bob
account:checking_789#banned@user:bob  // Bob's access revoked due to dispute

CheckPermission(
  resource: account:checking_789,
  permission: can_access,
  subject: user:bob
)
→ PERMISSIONSHIP_NO_PERMISSION (in banned set)
```

**Semantics:** `(owner | delegate) - banned` means: "owner OR delegate, EXCEPT anyone in banned set."

---

## Pattern 9: Multi-Tenant with Isolation

**Use case:** SaaS platform with multiple isolated tenants.

### Approach A: Tenant at Root

```
definition tenant {}

definition user {
  relation tenant: tenant
}

definition account {
  relation tenant: tenant
  relation owner: user
  
  permission owner_access = owner
}
```

Permission check implicitly scoped by tenant link.

### Approach B: Tenant in Caveat

```
caveat tenant_isolation(user_tenant_id: string, resource_tenant_id: string) {
  user_tenant_id == resource_tenant_id
}

definition account {
  relation owner: user with tenant_isolation
}
```

Tenant context passed per-request, enforced in caveat.

**Recommendation:** Use Approach A (tenant as root) for simplicity and performance. Caveat approach adds latency.

---

## Pattern 10: Linked/Related Objects (Account → Transactions)

**Use case:** Permissions on parent propagate to children (access account = access all transactions).

```
definition user {}

definition account {
  relation owner: user
  relation delegate: user
  
  permission full_access = owner | delegate
  permission read_only = full_access
}

definition transaction {
  relation account: account
  
  // Computed through account relationship
  permission view = account#full_access
  permission approve = account#full_access
}
```

**Permission flow:**
```
user:alice has "full_access" on account:checking_789
  ↓
transaction:txn_001#account@account:checking_789
  ↓
transaction#view = account#full_access
  ↓
alice has "view" on transaction:txn_001 ✓
```

This is the power of ReBAC: define permissions at the parent, automatically inherited by children.

---

## Pattern 11: Intersection (User Needs Multiple Relations)

**Use case:** User must have access through two independent paths.

```
definition department {
  relation member: user
}

definition project {
  relation lead: user
}

definition task {
  relation on_project: project
  relation department: department
  
  // Can edit only if both project lead AND in department
  permission edit = (on_project#lead & department#member)
}
```

**Scenario:**
```
user:alice is project:proj_1#lead
user:alice is department:eng#member
task:task_001#on_project@project:proj_1
task:task_001#department@department:eng

CheckPermission(task:task_001, edit, user:alice)
→ PERMISSIONSHIP_HAS_PERMISSION (alice in both sets)
```

**Use sparingly:** Intersections are slower than unions. Consider if permission should be expressed differently.

---

## Pattern 12: Nested Teams (Teams within Organizations)

**Use case:** Organization contains teams; teams contain users.

```
definition user {}

definition organization {
  relation super_admin: user
  relation admin: user
}

definition team {
  relation organization: organization
  relation lead: user
  relation member: user
}

definition account {
  relation organization: organization
  relation team: team
  relation owner: user
  
  permission org_admin = organization#admin | organization#super_admin
  permission team_lead = team#lead
  permission team_member = team#member
  permission full_access = owner | team_lead | org_admin
  permission read_only = full_access | team_member
}
```

**Multiple paths to permission:**
```
User can have access via:
1. Direct ownership (owner)
2. Team lead of account's team
3. Organization admin
4. Organization super admin
5. Team member of account's team (read-only)
```

---

## Schema Design Checklist

- [ ] **Relations are nouns** (owner, delegate, member, lead)
- [ ] **Permissions are adjectives/verbs** (can_transfer, can_view, can_admin)
- [ ] **Write to relations only**, not permissions (permissions are computed)
- [ ] **Minimize graph depth** (aim for ≤3 hops for performance)
- [ ] **Use caveats sparingly** (only for context unavailable at storage time)
- [ ] **Audit permission paths** (what's the deepest hierarchy?)
- [ ] **Test permission combinations** (union, intersection, exclusion)
- [ ] **Document permission semantics** (what does "full_access" include?)
- [ ] **Plan for schema evolution** (how to add new roles/permissions without breaking existing?)

---

## Common Mistakes to Avoid

1. **Storing computed permissions** — Use relations, derive permissions from them
2. **Over-nesting** — Account → Org → Division → Team → Account creates cycles
3. **Wildcard on write permissions** — Avoid `user:*` on edit/transfer/delete
4. **Over-caveating** — Every caveat adds latency; use only when necessary
5. **Unclear permission semantics** — Document what each permission implies
6. **Forgetting audit needs** — Design for LookupSubjects to work efficiently
7. **Static role assignments** — Use relationships (dynamic), not hardcoded role memberships
8. **Cross-cutting permissions** — If access is really about "seniority," model it, don't hardcode it

---

## Testing Your Schema

1. **Draw the permission graph** — Visualize relationship flow for key scenarios
2. **Test happy path** — Does intended user get intended permission?
3. **Test negative case** — Does excluded user NOT get permission?
4. **Test revocation** — When relationship deleted, does permission disappear?
5. **Test delegation** — Do indirect accesses work (parent → child)?
6. **Test caveat edge cases** — What happens at expiry boundaries?
7. **Test performance** — How many hops does deepest permission query require?
8. **Test audit** — Can you enumerate all access holders (LookupSubjects)?

