> _Maintained copy for the agent fleet. Do not sync from `/knowledge` — that copy is archived._

# SpiceDB API Quick Reference

Practical guide to SpiceDB APIs with banking-relevant examples.

---

## Core API Overview

| API | Purpose | Returns | Banking Use Case |
|-----|---------|---------|-----------------|
| **CheckPermission** | Is subject allowed to do X? | Yes/No/Maybe | Pre-auth before transfer |
| **WriteRelationships** | Create/update relationships | ZedToken | Grant account access |
| **LookupResources** | Which resources can user access? | List of resources | Dashboard: show my accounts |
| **LookupSubjects** | Who can access this resource? | List of users | Admin: who has access? |
| **ReadRelationships** | Get stored relationships | List of tuples | Audit, reconciliation |
| **DeleteRelationships** | Remove relationships | ZedToken | Revoke access, offboard |
| **Watch** | Subscribe to relationship changes | Stream of events | Real-time audit logging |

---

## 1. CheckPermission

**Purpose:** Verify if a subject has a specific permission.

### Syntax

```
CheckPermission(
  resource: { type: string, id: string },
  permission: string,
  subject: { object: { type: string, id: string } },
  consistency: ConsistencyOptions,
  context: { [key: string]: any }
)
```

### Response

```
{
  permissionship: PERMISSIONSHIP_HAS_PERMISSION | PERMISSIONSHIP_NO_PERMISSION | PERMISSIONSHIP_CONDITIONAL_PERMISSION,
  checked_at: ZedToken,
  partially_evaluated_error: Error (if caveat context missing)
}
```

### Examples

#### Simple Check: Can user transfer from account?

```javascript
CheckPermission({
  resource: { type: "account", id: "checking_789" },
  permission: "transfer",
  subject: { object: { type: "user", id: "alice" } },
  consistency: { at_least_as_fresh: zedtoken_from_write }
})

// Response: PERMISSIONSHIP_HAS_PERMISSION
```

#### Check with Caveat Context: Can user transfer $500?

```javascript
CheckPermission({
  resource: { type: "account", id: "checking_789" },
  permission: "delegate_transfer",  // Has transfer_limit caveat
  subject: { object: { type: "user", id: "bob" } },
  consistency: { minimize_latency: {} },
  context: {
    amount: 500,
    limit: 1000
  }
})

// Response: PERMISSIONSHIP_HAS_PERMISSION (amount <= limit)
```

#### Check Missing Context

```javascript
CheckPermission({
  resource: { type: "account", id: "checking_789" },
  permission: "support_transfer",  // Requires IP and time caveats
  subject: { object: { type: "user", id: "support_1" } },
  // context: omitted
})

// Response: PERMISSIONSHIP_CONDITIONAL_PERMISSION
// Message: "Missing context fields: request_time, request_ip"
```

### Usage Pattern

```javascript
// 1. High-security operation (transfer, delete)
const perm = await checkPermission({
  resource: { type: "account", id: accountId },
  permission: "transfer",
  subject: { object: { type: "user", id: userId } },
  consistency: { at_least_as_fresh: lastWriteZedToken }
});

if (perm.permissionship !== "HAS_PERMISSION") {
  throw new Error("Not authorized");
}

// 2. UI rendering (show/hide buttons)
const readPerm = await checkPermission({
  resource: { type: "account", id: accountId },
  permission: "view",
  subject: { object: { type: "user", id: userId } },
  consistency: { minimize_latency: {} }  // Fast, acceptable staleness
});

if (readPerm.permissionship === "HAS_PERMISSION") {
  showAccountButton();
}
```

---

## 2. WriteRelationships

**Purpose:** Create or update relationships (grant access).

### Syntax

```
WriteRelationships(
  updates: [
    {
      operation: OPERATION_CREATE | OPERATION_DELETE | OPERATION_TOUCH,
      relationship: {
        resource: { type: string, id: string },
        relation: string,
        subject: { object: { type: string, id: string } }
      },
      caveat: {
        caveat_name: string,
        context: { [key: string]: any }
      }
    }
  ]
)
```

### Response

```
{
  written_at: ZedToken
}
```

### Examples

#### Grant Account Owner

```javascript
WriteRelationships({
  updates: [{
    operation: "OPERATION_CREATE",
    relationship: {
      resource: { type: "account", id: "checking_789" },
      relation: "owner",
      subject: { object: { type: "user", id: "alice" } }
    }
  }]
})

// Returns: { written_at: new_zedtoken }
```

#### Grant Temporary Delegate (Expires in 30 days)

```javascript
WriteRelationships({
  updates: [{
    operation: "OPERATION_CREATE",
    relationship: {
      resource: { type: "account", id: "checking_789" },
      relation: "delegate",
      subject: { object: { type: "user", id: "bob" } }
    },
    caveat: {
      caveat_name: "is_valid_delegation",
      context: {
        expires_at: new Date(Date.now() + 30*24*60*60*1000)
      }
    }
  }]
})
```

#### Batch Grant (Org Admin Gets Access to All Accounts)

```javascript
// Grant org_admin to 100 accounts for a new admin

const updates = accountIds.map(accountId => ({
  operation: "OPERATION_CREATE",
  relationship: {
    resource: { type: "account", id: accountId },
    relation: "organization",  // Link account to org
    subject: { object: { type: "organization", id: "org_hq" } }
  }
}));

WriteRelationships({ updates })

// Now org_hq#admin has inherited access to all accounts
```

#### Revoke Access (Delete Relationship)

```javascript
WriteRelationships({
  updates: [{
    operation: "OPERATION_DELETE",
    relationship: {
      resource: { type: "account", id: "checking_789" },
      relation: "delegate",
      subject: { object: { type: "user", id: "bob" } }
    }
  }]
})

// After this write, bob no longer has delegate access
```

### Usage Pattern

```javascript
// Onboard new account owner
async function grantAccountOwner(accountId, userId) {
  const response = await writeRelationships({
    updates: [{
      operation: "OPERATION_CREATE",
      relationship: {
        resource: { type: "account", id: accountId },
        relation: "owner",
        subject: { object: { type: "user", id: userId } }
      }
    }]
  });
  
  return response.written_at;  // Use for subsequent at_least_as_fresh checks
}

// Revoke access
async function revokeAccountAccess(accountId, userId, relation) {
  await writeRelationships({
    updates: [{
      operation: "OPERATION_DELETE",
      relationship: {
        resource: { type: "account", id: accountId },
        relation: relation,
        subject: { object: { type: "user", id: userId } }
      }
    }]
  });
}
```

---

## 3. LookupResources

**Purpose:** Find all resources where a subject has a specific permission.

### Syntax

```
LookupResources(
  resource_type: string,
  permission: string,
  subject: { object: { type: string, id: string } },
  consistency: ConsistencyOptions,
  context: { [key: string]: any }
)
```

### Response

```
{
  results: [
    { resource_id: string, permission: string },
    ...
  ]
}
```

### Examples

#### List All Accounts User Can Access

```javascript
LookupResources({
  resource_type: "account",
  permission: "view",
  subject: { object: { type: "user", id: "alice" } },
  consistency: { minimize_latency: {} }
})

// Response:
// {
//   results: [
//     { resource_id: "checking_789" },
//     { resource_id: "savings_456" },
//     { resource_id: "business_001" }
//   ]
// }
```

#### List Accounts User Can Perform Transfers On

```javascript
LookupResources({
  resource_type: "account",
  permission: "transfer",
  subject: { object: { type: "user", id: "bob" } },
  consistency: { at_least_as_fresh: zedtoken }
})

// Returns only accounts where bob has transfer permission
```

#### List with Caveat Context

```javascript
LookupResources({
  resource_type: "account",
  permission: "delegate_transfer",
  subject: { object: { type: "user", id: "charlie" } },
  context: {
    amount: 500,
    limit: 1000
  }
})

// Returns accounts where caveat evaluates to true
```

### Usage Pattern

```javascript
// Populate user dashboard
async function getUserDashboard(userId) {
  const accounts = await lookupResources({
    resource_type: "account",
    permission: "view",
    subject: { object: { type: "user", id: userId } },
    consistency: { minimize_latency: {} }
  });
  
  // Fetch account details from database
  return accounts.results.map(r => r.resource_id);
}

// Filter accessible accounts for transfer
async function getTransferable Accounts(userId, amount) {
  const accounts = await lookupResources({
    resource_type: "account",
    permission: "transfer",
    subject: { object: { type: "user", id: userId } },
    consistency: { at_least_as_fresh: recentZedToken },
    context: { amount, limit: userDailyLimit }
  });
  
  return accounts.results.map(r => r.resource_id);
}
```

---

## 4. LookupSubjects

**Purpose:** Find all subjects with a specific permission on a resource.

### Syntax

```
LookupSubjects(
  resource: { type: string, id: string },
  permission: string,
  subject_type: string,
  consistency: ConsistencyOptions,
  context: { [key: string]: any }
)
```

### Response

```
{
  subjects: [
    { subject: { object: { type: string, id: string } } },
    ...
  ]
}
```

### Examples

#### Who Can View This Account?

```javascript
LookupSubjects({
  resource: { type: "account", id: "checking_789" },
  permission: "view",
  subject_type: "user",
  consistency: { fully_consistent: true }
})

// Response:
// {
//   subjects: [
//     { subject: { object: { type: "user", id: "alice" } } },
//     { subject: { object: { type: "user", id: "bob" } } },
//     { subject: { object: { type: "user", id: "charlie" } } }
//   ]
// }
```

#### Who Are the Admins of This Account?

```javascript
LookupSubjects({
  resource: { type: "account", id: "business_001" },
  permission: "admin",
  subject_type: "user"
})

// Returns all users with admin permission (including through role membership)
```

### Usage Pattern

```javascript
// Compliance: Generate access report
async function generateAccessReport(accountId) {
  const admins = await lookupSubjects({
    resource: { type: "account", id: accountId },
    permission: "admin",
    subject_type: "user",
    consistency: { fully_consistent: true }
  });
  
  const viewers = await lookupSubjects({
    resource: { type: "account", id: accountId },
    permission: "view",
    subject_type: "user",
    consistency: { fully_consistent: true }
  });
  
  return {
    account: accountId,
    admins: admins.subjects.map(s => s.subject.object.id),
    viewers: viewers.subjects.map(s => s.subject.object.id)
  };
}

// Admin UI: Show who has access
async function listAccountAccess(accountId) {
  const subjects = await lookupSubjects({
    resource: { type: "account", id: accountId },
    permission: "full_access",
    subject_type: "user"
  });
  
  return subjects.subjects.map(s => ({
    userId: s.subject.object.id,
    accountId: accountId
  }));
}
```

---

## 5. ReadRelationships

**Purpose:** Retrieve stored relationships (raw tuples).

### Syntax

```
ReadRelationships(
  resource_filter: { type?: string, id?: string },
  relation_filter: string,
  subject_filter: { type?: string, id?: string }
)
```

### Response

```
{
  relationships: [
    {
      resource: { type: string, id: string },
      relation: string,
      subject: { object: { type: string, id: string } },
      caveat: { caveat_name: string, context: {...} }
    },
    ...
  ]
}
```

### Examples

#### Get All Relationships for an Account

```javascript
ReadRelationships({
  resource_filter: { type: "account", id: "checking_789" },
  relation_filter: "*",  // Any relation
  subject_filter: {}  // Any subject
})

// Response:
// {
//   relationships: [
//     { resource: {...}, relation: "owner", subject: {..., id: "alice"} },
//     { resource: {...}, relation: "delegate", subject: {..., id: "bob"} }
//   ]
// }
```

#### Get All Owners of an Account

```javascript
ReadRelationships({
  resource_filter: { type: "account", id: "checking_789" },
  relation_filter: "owner",
  subject_filter: {}
})

// Returns only owner relationships for this account
```

#### Audit: Get All Access Granted to User

```javascript
ReadRelationships({
  resource_filter: {},  // Any resource
  relation_filter: "*",  // Any relation
  subject_filter: { type: "user", id: "alice" }
})

// Returns all relationships where alice is the subject
```

### Usage Pattern

```javascript
// Audit trail: show all permissions on an account
async function auditAccountAccess(accountId) {
  const rels = await readRelationships({
    resource_filter: { type: "account", id: accountId },
    relation_filter: "*"
  });
  
  return rels.relationships.map(rel => ({
    account: accountId,
    relation: rel.relation,
    subject: rel.subject.object.id,
    caveat: rel.caveat ? rel.caveat.caveat_name : null
  }));
}

// Backup: Export all relationships for disaster recovery
async function backupAllRelationships() {
  const rels = await readRelationships({
    resource_filter: {},
    relation_filter: "*",
    subject_filter: {}
  });
  
  return rels.relationships;  // Store in backup
}
```

---

## 6. DeleteRelationships

**Purpose:** Delete relationships (revoke access).

### Syntax

```
DeleteRelationships(
  resource_filter: { type?: string, id?: string },
  relation_filter: string,
  subject_filter: { type?: string, id?: string }
)
```

### Response

```
{
  deleted_at: ZedToken,
  deletion_progress: PROGRESS_COMPLETE | PROGRESS_IN_PROGRESS
}
```

### Examples

#### Revoke Specific Delegate

```javascript
DeleteRelationships({
  resource_filter: { type: "account", id: "checking_789" },
  relation_filter: "delegate",
  subject_filter: { type: "user", id: "bob" }
})

// Deletes only the bob#delegate relationship for this account
// Returns: { deleted_at: zedtoken, deletion_progress: "COMPLETE" }
```

#### Offboard User (Remove All Access)

```javascript
DeleteRelationships({
  resource_filter: {},  // All accounts
  relation_filter: "*",  // All relations
  subject_filter: { type: "user", id: "charlie" }
})

// Removes charlie from all relationships across all resources
```

#### Disable Account (Remove All Access to Account)

```javascript
DeleteRelationships({
  resource_filter: { type: "account", id: "checking_789" },
  relation_filter: "*",  // All relations
  subject_filter: {}  // All subjects
})

// Removes all permissions on this account
```

### Usage Pattern

```javascript
// Offboarding workflow
async function offboardUser(userId) {
  const deleteResponse = await deleteRelationships({
    resource_filter: {},
    relation_filter: "*",
    subject_filter: { type: "user", id: userId }
  });
  
  console.log(`Offboarded ${userId} at ${deleteResponse.deleted_at}`);
  return deleteResponse.deleted_at;
}

// Revoke specific delegation
async function revokeDelegation(accountId, userId) {
  await deleteRelationships({
    resource_filter: { type: "account", id: accountId },
    relation_filter: "delegate",
    subject_filter: { type: "user", id: userId }
  });
}
```

---

## 7. Watch API

**Purpose:** Subscribe to real-time relationship changes.

### Syntax

```
Watch(
  namespaces: string[],
  consistency: ConsistencyOptions
)

// Returns: AsyncIterator<WatchResponse>
```

### Response (Stream)

```
{
  updates: [
    {
      timestamp: number,
      operation: "OPERATION_CREATE" | "OPERATION_TOUCH" | "OPERATION_DELETE",
      relationship: { ... }
    }
  ]
}
```

### Example

#### Real-Time Audit Logging

```javascript
// Subscribe to all permission changes
const watcher = watch({
  namespaces: ["account", "user", "organization"],
  consistency: { minimize_latency: {} }
});

for await (const event of watcher) {
  for (const update of event.updates) {
    const { timestamp, operation, relationship } = update;
    
    console.log(`[${timestamp}] ${operation}:`, {
      resource: relationship.resource.id,
      relation: relationship.relation,
      subject: relationship.subject.object.id
    });
    
    // Emit to audit system
    auditLog.log({
      timestamp,
      event_type: "permission_change",
      operation,
      resource: relationship.resource.id,
      relation: relationship.relation,
      subject: relationship.subject.object.id
    });
  }
}
```

### Usage Pattern

```javascript
// Start background audit listener
function startAuditListener() {
  const watcher = watch({
    namespaces: ["account", "organization", "user"],
    consistency: { minimize_latency: {} }
  });
  
  (async () => {
    for await (const event of watcher) {
      for (const update of event.updates) {
        // Send to audit/compliance system
        await auditService.logPermissionChange({
          timestamp: update.timestamp,
          operation: update.operation,
          resource: update.relationship.resource,
          relation: update.relationship.relation,
          subject: update.relationship.subject
        });
        
        // Optionally: invalidate permission cache
        permissionCache.invalidate(update.relationship.resource);
      }
    }
  })();
}
```

---

## Consistency Strategy Reference

| Scenario | Consistency | Rationale |
|----------|-------------|-----------|
| **Pre-transfer auth** | `at_least_as_fresh(recentZedToken)` | Prevent race condition (new enemy) |
| **UI: show/hide button** | `minimize_latency` | Fast, acceptable staleness |
| **Compliance report** | `fully_consistent` | Audit accuracy needed |
| **Dashboard: list accounts** | `minimize_latency` | Performance critical |
| **Post-write check** | `at_least_as_fresh(writeZedToken)` | Verify write took effect |
| **Admin: access review** | `fully_consistent` | Auditor needs fresh data |

---

## Error Handling Patterns

### Caveat Context Missing

```javascript
const result = await checkPermission({...});

if (result.permissionship === "CONDITIONAL_PERMISSION") {
  const missing = result.partially_evaluated_error?.message;
  // Return 422 Unprocessable Entity
  // Client should retry with context
  return { error: "Missing context", context_needed: missing };
}
```

### Transient Errors

```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (err) {
      if (err.code === "UNAVAILABLE" && i < maxRetries - 1) {
        await delay(Math.pow(2, i) * 100);  // Exponential backoff
        continue;
      }
      throw err;
    }
  }
}

// Usage
const result = await withRetry(() =>
  checkPermission({ ... })
);
```

---

## Banking-Specific Patterns

### Restrict Transfer Amount

```javascript
CheckPermission({
  resource: { type: "account", id: accountId },
  permission: "transfer",
  subject: { object: { type: "user", id: userId } },
  context: {
    amount: transferAmount,
    limit: userDailyLimit
  }
})
```

### Verify IP for High-Value Access

```javascript
CheckPermission({
  resource: { type: "account", id: accountId },
  permission: "high_value_transfer",
  subject: { object: { type: "user", id: userId } },
  context: {
    request_ip: req.ip,
    allowed_ips: userAllowedIPs
  }
})
```

### Time-Window Access (Business Hours Only)

```javascript
CheckPermission({
  resource: { type: "account", id: accountId },
  permission: "support_access",
  subject: { object: { type: "user", id: supportUserId } },
  context: {
    request_time: new Date()
  }
})
```

---

## Performance Tips

1. **Cache ZedTokens** — Reuse from recent writes in subsequent checks
2. **Batch writes** — Use single `WriteRelationships` call with multiple updates
3. **Use minimize_latency for reads** — Unless you need post-write guarantees
4. **LookupResources pagination** — Some implementations support cursor-based pagination
5. **Watch API** — Use for cache invalidation rather than polling CheckPermission

