# Blameless Post-Mortem Report

**Incident Title:** Friday 5 PM Hotfix Connection Leak
**Date:** October 16, 2026
**Author:** Sidra Soudagar
**Status:** Closed

---

## 1. Executive Summary

On October 16, 2026, at 17:07 IST, NovaPay experienced a SEV-1 outage resulting in a 12% HTTP 500 error rate for 15 minutes. The outage was caused by a critical hotfix pushed directly to production that bypassed the standard CI/CD pipeline. The lack of staging tests allowed a database connection leak to reach production. The automated rollback successfully restored application traffic within 6 minutes, but manual DBA intervention was required to clear the database connection pool.

## 2. Impact

- **Customer Impact:** ~45,000 users were unable to complete transactions for 15 minutes.
- **Financial Impact:** Estimated ₹10,00,000 in failed transaction fees.
- **Regulatory Impact:** RBI requires reporting of outages > 30 minutes. Because the outage was resolved in 15 minutes, regulatory reporting was **not** required.

## 3. Root Cause

1. **The Code:** The hotfix failed to close database connections properly.
2. **The Process:** The developer had Admin rights and bypassed the staging environment and SAST gates.
3. **The Architecture:** The pipeline did not have a hard block on direct pushes to `main` for emergency hotfixes.

## 4. What Went Well

- The alerting system (Prometheus/PagerDuty) correctly identified the issue in < 1 minute.
- The automated rollback (Argo Rollouts) successfully rerouted traffic in 6 minutes, preventing a longer outage.

## 5. What Went Wrong

- A human was allowed to bypass security/compliance gates.
- The automated rollback did not clear the database connections (because Istio only routes traffic, it doesn't reset the DB).

## 6. Action Plan

| Action | Owner | Due Date | Ticket |
|--------|-------|----------|--------|
| Remove "Admin Bypass" from GitHub branch protection. Hotfixes must use the `hotfix/` pipeline. | DevOps | Oct 18 | JIRA-101 |
| Implement `PgBouncer` to pool and limit database connections automatically. | DBA | Oct 25 | JIRA-102 |
| Add DB connection exhaustion alert to Prometheus. | SRE | Oct 17 | JIRA-103 |
| Conduct training on "How to deploy a hotfix safely." | Eng Manager | Oct 30 | JIRA-104 |

---

## AI Attribution
- **Tool used:** DeepSeek
- **Human review:** Verified against incident timeline.
