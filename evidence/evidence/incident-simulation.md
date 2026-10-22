# Incident Simulation: Friday 5 PM Disaster

**Date of Incident:** October 16, 2026
**Severity:** SEV-1 (Complete service degradation)
**Incident Commander:** Sidra Soudagar (SRE Lead)

---

## 1. The Incident Timeline (Minute-by-Minute)

**T+0 (17:07 IST):** 
- Three alerts fire simultaneously in PagerDuty.
- On-call SRE acknowledges the page.

**T+2 (17:09 IST):** 
- SRE opens the Grafana Engineering Dashboard.
- Confirms HTTP 500 errors are at 12% and payment gateway timeouts are at 35%.
- SRE posts in `#incident-response`: "Declaring SEV-1. Investigating."

**T+4 (17:11 IST):** 
- SRE checks ArgoCD. Sees a deployment (`hotfix-payment-v1.2`) bypassed staging and was merged to `main` 10 minutes ago.
- **Action:** SRE immediately triggers an automated rollback to `v1.1` via Argo Rollouts.

**T+6 (17:13 IST):** 
- Istio routes 100% of traffic back to the stable version (`v1.1`). 
- HTTP 500 errors drop from 12% to 2%.

**T+10 (17:17 IST):** 
- **Problem:** The database connection pool is still exhausted. 
- **Cause:** The bad code (`v1.2`) opened connections without closing them. Even though the code is rolled back, the database is still choked.
- **Action:** DBA executes `pg_terminate_backend` to kill the idle connections from the failed deployment.

**T+15 (17:22 IST):** 
- PostgreSQL connections return to normal.
- HTTP 500 errors drop to 0%.
- Payment gateway timeouts drop to 0%.

**T+30 (17:37 IST):** 
- SRE Lead confirms 30 minutes of stable metrics.
- Status page updated to "Resolved".
- Incident downgraded.

---

## 2. Root Cause Analysis (RCA)

- **Why did it fail?** The developer's hotfix included a database connection leak that wasn't caught by unit tests.
- **Why did it reach production?** The developer bypassed the `Staging` environment by pushing directly to `main` and using an emergency override.
- **What pipeline gate was missing?** The `Source Control` gate failed because the branch protection rules allowed the Admin user to bypass PR reviews and staging tests for "emergencies".

---

## 3. Action Items & Fixes

| Action | Type | Owner | Due Date |
|--------|------|-------|----------|
| **Fix the Pipeline:** Revoke Admin bypass rights. All hotfixes MUST go through an automated integration test stage before production. | Prevent | DevOps Lead | Oct 18, 2026 |
| **Fix the Code:** Refactor the DB connection logic to use a connection pool manager. | Prevent | Dev Team | Oct 19, 2026 |
| **Fix the Alert:** Create a specific alert for "DB Connection Exhaustion > 90%" so SREs know immediately. | Detect | SRE Team | Oct 17, 2026 |
| **Fix the Process:** Update the Hotfix Runbook to mandate a manual DBA connection check. | Mitigate | SRE Lead | Oct 20, 2026 |

---

## AI Attribution
- **Tool used:** DeepSeek
- **Human review:** Customized for NovaPay scenario.
