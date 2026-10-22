# Deliverable 8: Observability & DORA Metrics Strategy

**Project:** NovaPay Digital Bank
**Author:** Sidra Soudagar

---

## 1. The 4 DORA Metrics (Elite Targets)

| Metric | Definition | NovaPay Target | Measurement Source |
|--------|------------|----------------|--------------------|
| **Deployment Frequency** | How often code deploys to production | **Multiple per day** | GitHub Actions API |
| **Lead Time for Changes** | Time from commit to production deploy | **< 1 hour** | GitHub Commit Timestamp vs ArgoCD Sync |
| **Change Failure Rate** | % of deployments causing SEV-1/SEV-2 incidents | **< 5%** | Jira Incident Tickets / Total Deploys |
| **MTTR** | Time to restore service after failure | **< 15 minutes** | PagerDuty Incident Duration |

---

## 2. The 15+ Pipeline-Specific Metrics

Beyond DORA, we track:
- **Build Success Rate:** > 95%
- **Flaky Test Rate:** < 1% (top 5 flaky tests tracked)
- **SAST Gate Pass Rate:** % of builds blocked by security.
- **Deployment Duration:** Time taken for Argo Rollouts to finish canary.
- **Rollback Frequency:** How often Category A/B triggers fire.
- **False Positive Rate per Scanner:** (e.g., ZAP DAST false positives).

---

## 3. The 3 Dashboard Personas

### Dashboard 1: Engineering (Real-time Ops)
- **Audience:** SREs, Developers.
- **Data:** Live HTTP error rates, p99 latency, Pod restarts, Deployment status.
- **Refresh Rate:** 10 seconds.
- **Action:** Triage active incidents.

### Dashboard 2: Management (Executive)
- **Audience:** CTO, VP Engineering.
- **Data:** The 4 DORA Metrics, team velocity, cost of cloud infrastructure.
- **Refresh Rate:** Daily.
- **Action:** Resource allocation, process improvement.

### Dashboard 3: Regulatory & Audit (Compliance)
- **Audience:** CISO, RBI Auditors.
- **Data:** Gate pass/fail history, SoD approval logs, Vulnerability remediation time (MTTR for CVEs), exception logs.
- **Refresh Rate:** Daily.
- **Action:** Prove compliance, audit sign-off.

---

## 4. Alerting Strategy & Routing

Alerts are useless if they go to the wrong place. We use severity-based routing via Alertmanager.

| Severity | Example Trigger | Routing Destination | Escalation |
|----------|-----------------|---------------------|------------|
| **Critical** | HTTP 5xx > 5% | PagerDuty (Phone Call + SMS) | Auto-rollback, Page CTO |
| **Warning** | CPU > 80% for 10m | Slack `#alerts-warning` | If unresolved in 15m, page on-call |
| **Info** | New deployment started | Slack `#deployments` | None |

---

## AI Attribution
- **Tool used:** DeepSeek
- **Human review:** Customized for NovaPay.
