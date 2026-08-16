# Post-Mortems & Architectural Scars Vault

> **The Invariant**: Making a mistake is the cost of engineering velocity; making the same mistake twice is a failure of memory. This vault turns production incidents into living architectural guardrails.

---

## 📋 Incident Registry & Scar Catalog

### Scar Template
```markdown
### SCAR-[ID]: [Incident Title]
* **Date**: YYYY-MM-DD
* **Root Cause**: What underlying assumption or race condition failed?
* **Blast Radius**: What services or users were impacted?
* **Architectural Fix**: What deterministic code guardrail or test was added to prevent recurrence?
* **Living Rule**: What 1-sentence invariant must all future engineers follow?
```

---

### Example Entry

### SCAR-001: Multi-Agent Infinite Negotiation Deadlock
* **Date**: 2026-08-14
* **Root Cause**: Two autonomous agents negotiated resource allocation without a monotonic time-to-live (TTL) counter or exponential backoff.
* **Blast Radius**: Background daemon CPU pegged at 100% for 42 minutes.
* **Architectural Fix**: Added a 10-iteration limit and deterministic escalation callback to human supervisor.
* **Living Rule**: *Every autonomous agent negotiation loop MUST include an integer iteration ceiling and an explicit human escalation fallback.*
