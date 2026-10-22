# NovaPay Incident Response Playbook

**Version:** 1.0
**Owner:** SRE Lead
**Last Updated:** 17/10/2026

---

## 1. Incident Severity Classification

| Severity | Definition | Response Time | Escalation Path |
|----------|------------|---------------|-----------------|
| **SEV-1** | Complete service outage, data breach, or payment failure for > 50% users | **< 5 minutes** | CTO + CISO + VP Engineering |
| **SEV-2** | Major feature degradation affecting > 10% users | **< 15 minutes** | VP Engineering + SRE Lead |
| **SEV-3** | Minor degradation, workaround exists | **< 1 hour** | SRE On-Call + Tech Lead |
| **SEV-4** | Cosmetic issue, no user impact | Next business day | Assigned Engineer |

---

## 2. The 7-Step Incident Response Workflow

### Step 1: Detection & Acknowledgment
- Acknowledge the alert in PagerDuty within 5 minutes (SEV-1) or 15 minutes (SEV-2).
- Post in `#incident-response` Slack channel: "Investigating [Alert Name] - SEV-[Level]."

### Step 2: Triage & Classification
- Open Grafana dashboards.
- Check recent deployments: Was there a deployment in the last 2 hours?
- If yes → **ROLLBACK IMMEDIATELY** (Category A rule).
- If no → Proceed to Step 3.

### Step 3: Assemble the Team
- For SEV-1: Page the Incident Commander (IC), CTO, and CISO.
- For SEV-2: Page the SRE Lead and relevant Engineering Manager.

### Step 4: Communicate (External & Internal)
- **Internal:** Update Slack every 30 minutes.
- **External (Status Page):** Update `status.novapay.com` within 15 minutes of SEV-1 confirmation.

### Step 5: Mitigate & Resolve
- Apply the shortest path to recovery (rollback, scale up, failover to DR).
- Document all actions in the incident channel with timestamps.

### Step 6: Resolution & Monitoring
- Once mitigated, monitor for 30 minutes to ensure stability.
- Declare incident resolved in Slack.

### Step 7: Post-Incident Review (Post-Mortem)
- Schedule a blameless post-mortem within 48 hours.
- Document: Timeline, Root Cause, Impact, Action Items.

---

## 3. Communication Templates

### Template 1: Initial Acknowledgment (Internal Slack)
> 🚨 **INCIDENT DECLARED: SEV-1**
> **Impact:** Users unable to complete UPI transactions.
> **Start Time:** 14:30 IST
> **Status:** Investigating. Rollback initiated.
> **IC:** @john-doe

### Template 2: External Status Page Update
> **Investigating Payment Issues**
> We are currently experiencing issues with UPI transactions. Our engineering team is actively investigating. We apologize for the inconvenience.

### Template 3: Resolution Notification
> ✅ **RESOLVED: UPI Transactions**
> The issue has been resolved as of 15:15 IST. All systems are operating normally. A full post-mortem will be published within 48 hours.

---

## 4. Post-Mortem Template 

**Incident Title:** Payment Gateway Timeout & Database Connection Pool Exhaustion
**Date:** October 16, 2026
**Severity:** SEV-1
**Duration:** 45 minutes (14:30 IST to 15:15 IST)

### Root Cause
A recent configuration change to the payment service (increasing the maximum HTTP timeout from 5s to 30s) caused worker threads to hang during a downstream gateway slowdown. This led to a cascading failure, exhausting the PostgreSQL connection pool and resulting in 12% HTTP 500 errors for users.

### Timeline (All times IST)
- **14:30** - Prometheus Alert `HighErrorRate` fires (HTTP 5xx > 5%). PagerDuty alerts on-call engineer.
- **14:32** - On-call acknowledges. Notices a deployment happened at 14:00. Initiates Category A auto-rollback via Argo Rollouts.
- **14:35** - Traffic routed back to the stable Blue environment. Error rate drops to 0%, but database connections remain saturated.
- **14:40** - SRE Lead joins. They identify connection pool exhaustion. Executes `pg_terminate_backend` on idle transactions to free up connections.
- **14:50** - Error rate stabilizes at 0.1%. Customer support confirms UPI and card payments are processing again.
- **15:15** - After 25 minutes of stable metrics, the Incident Commander declares the incident resolved.

### Impact
- **Customers affected:** ~45,000 users during the 45-minute window.
- **Financial impact:** 12,000 failed transactions (users retried successfully later).
- **Regulatory impact:** None (outage was under the 1-hour RBI reporting threshold, but logged internally).

### Action Items
| Action | Type | Owner | Due Date | Ticket |
|--------|------|-------|----------|--------|
| Revert HTTP timeout config to 5s and enforce strict limits in Helm | Prevent | Dev Team | Oct 17, 2026 | JIRA-882 |
| Add synthetic test for downstream gateway timeouts | Detect | QA | Oct 20, 2026 | JIRA-883 |
| Update PostgreSQL max_connections and tune PgBouncer | Mitigate | DBA | Oct 25, 2026 | JIRA-884 |
| Update Alerting rules to fire on DB Pool Exhaustion (>90%) | Detect | SRE | Oct 18, 2026 | JIRA-885 |

---

## AI Attribution
- **Tool used:** DeepSeek
- **Human review:** Customized for NovaPay SRE workflow.
