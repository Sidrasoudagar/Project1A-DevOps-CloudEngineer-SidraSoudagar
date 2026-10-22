# NovaPay Deployment Runbook

**Version:** 1.0
**Owner:** SRE Team
**Last Updated:** 17/10/2026

---

## 1. Pre-Deployment Checklist (Must be completed before starting)

- [ ] Deployment window verified (not during peak hours, salary days, or festivals).
- [ ] Change Request (CR) approved in ServiceNow.
- [ ] Dual approval obtained: Release Manager + SRE Lead.
- [ ] On-call SRE confirmed available and briefed.
- [ ] Rollback plan reviewed and understood.
- [ ] Database migration status checked (if applicable).
- [ ] Customer support team notified of potential maintenance window.

---

## 2. Deployment Execution Procedure

### Step 1: Initiate Pipeline
- Navigate to GitHub Actions and select the `Production Deployment` workflow.
- Click "Run workflow" and select the `main` branch.
- Enter the Change Request (CR) ID in the input box.

### Step 2: Monitor Pre-Deployment Gates
- Watch the pipeline logs. If any gate fails (SAST, DAST, Compliance), **STOP** and notify the developer.
- Verify that the approval step shows "Approved by RM and SRE Lead."

### Step 3: Canary Rollout (Automated)
- The pipeline will automatically deploy to 1% of traffic.
- **Decision Point:** Watch the Grafana dashboard for 15 minutes.
  - **If Green (Healthy):** The pipeline will auto-promote to the next phase.
  - **If Red (Unhealthy):** The pipeline will auto-rollback. Proceed to Step 5.

### Step 4: Full Rollout (Automated)
- After successful canary phases, the pipeline deploys to 100%.
- Verify the "Production Health Check" step turns green.

### Step 5: Post-Deployment Verification
- [ ] Run synthetic transaction test (login, check balance, transfer ₹1).
- [ ] Check Grafana: Error rate < 0.1%.
- [ ] Check Grafana: Latency p99 < 200ms.
- [ ] Confirm no new alerts in PagerDuty.
- [ ] Update the CR ticket with "Deployment Successful."

---

## 3. Emergency Hotfix Deployment

If a critical bug is found in production:
1. Create a branch `hotfix/issue-xyz` from `main`.
2. Apply the fix and run the expedited pipeline (bypasses unit tests but still requires security scans).
3. Requires **CISO** approval to bypass the test gate.
4. Deploy using the canary process above.

---

## AI Attribution
- **Tool used:** DeepSeek
- **Human review:** Customized for NovaPay SRE workflow.
