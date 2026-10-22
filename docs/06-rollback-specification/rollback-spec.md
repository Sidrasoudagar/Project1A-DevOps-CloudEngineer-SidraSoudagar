# Deliverable 6: Automated Rollback Specification

**Project:** NovaPay Digital Bank
**Author:** Sidra Soudagar

---

## 1. Rollback Trigger Categories

### Category A: Immediate Auto-Rollback (< 60 seconds)
These triggers bypass human approval because the system is actively failing.
- **HTTP 5xx Error Rate:** > 5% for 60 seconds.
- **Health Checks:** 3 consecutive readiness probe failures.
- **Pod Status:** CrashLoopBackOff or OOMKilled (Out of Memory).
- **Database:** Connection pool exhaustion > 90%.

### Category B: Escalated Auto-Rollback (< 15 minutes)
These triggers signal severe degradation. The on-call engineer is paged. If no action is taken within the escalation window, the system rolls back automatically.
- **Latency (p99):** > 2x the 7-day baseline for 5 minutes.
- **Error Budget:** Burn rate > 10x normal for 10 minutes.
- **Transaction Success:** Drops > 2% below baseline.
- **CPU/Memory:** Sustained > 90% utilization for 5 minutes.

### Category C: Manual Decision
- Gradual degradation below thresholds.
- Customer support reports of UI bugs.
- Downstream dependency correlation issues.

---

## 2. The 8-Step Rollback Execution Workflow

When a Category A trigger fires, the automated system (Argo Rollouts + Prometheus) executes this exact sequence:

1.  **Detect:** Prometheus Alertmanager fires the alert.
2.  **Correlate:** Argo Rollouts verifies the failure started *after* the new deployment.
3.  **Freeze:** The pipeline pauses all further promotions.
4.  **Rollback:** Istio instantly routes 100% of traffic back to the stable (Blue) environment.
5.  **Verify:** Automated smoke tests run against the stable environment.
6.  **Notify:** Slack/PagerDuty alerts the engineering team that a rollback occurred.
7.  **Incident:** A Jira incident ticket is auto-created.
8.  **Postmortem:** The team reviews the failure the next business day.

---

## 3. Post-Rollback Verification

A rollback is not complete just because traffic was re-routed. The system must verify:
- Error rates return to < 0.1%.
- Latency p99 returns to < 200ms.
- Database connections are healthy.
- Automated synthetic login/checkout tests pass.

---

## AI Attribution
- **Tool used:** DeepSeek
- **Human review:** Customized for NovaPay architecture.
