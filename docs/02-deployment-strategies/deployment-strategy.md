# Deliverable 2: Deployment Strategies

**Project:** NovaPay Digital Bank
**Author:** Sidra Soudagar

---

## 1. Strategy Selection

| Release type | Strategy | Target commit-to-production time |
|---|---|---|
| Standard release | Blue-green | 40 to 60 minutes |
| High-risk release (payments, ledger, auth changes) | Progressive canary | Measured separately; the progressive rollout phases take about 105 minutes, plus a 24-hour bake |

The two-hour commit-to-production target (see the pipeline validation in the evidence folder) applies to the standard blue-green path. Canary releases are measured separately because progressive traffic shifting is intentionally slower.

---

## 2. Blue-Green Deployment

NovaPay runs two identical production environments: **Blue** (live) and **Green** (new version).

### Traffic Switching Protocol
1. **Deploy:** New code is deployed to Green.
2. **Verify:** Automated smoke tests and health checks run against Green.
3. **Approve:** A production approver who is not the change author approves the switch (separation of duties).
4. **Switch:** The Istio VirtualService moves 100% of traffic from Blue to Green.
5. **Monitor:** Green is monitored for 15 minutes.
6. **Finalize or roll back:** If healthy, Green becomes the new Blue. If failing, traffic switches back to Blue.

### Sessions and Draining
- **Sessions:** A shared Redis cluster holds sessions, so users stay logged in across the switch. The session format must remain backward compatible between versions N-1 and N.
- **Connection draining:** Blue stops accepting new connections but lets in-flight payment transactions finish (up to 5 minutes) before shutdown.

---

## 3. Canary Deployment (High-Risk Releases)

Implemented with Argo Rollouts and Istio traffic splitting.

| Phase | Traffic | Duration | Success criteria | Action on failure |
|---|---|---|---|---|
| Canary | 1 to 2% | 15 min | Error rate < 0.1%, p99 latency < 200 ms, payment success rate not below baseline | Automatic rollback |
| Early adopter | 5 to 10% | 30 min | Error rate < 0.05%, no critical alerts | Automatic rollback |
| Expansion | 25 to 50% | 60 min | All SLOs met, no degradation | Automatic rollback |
| Full rollout | 100% | 24-hour bake | Stable SLO compliance | Rollback (manual, or automatic on Category A triggers) |

### Automated Analysis
Analysis is implemented as an Argo Rollouts `AnalysisTemplate` that runs queries and statistical checks against Prometheus metrics for the canary and stable versions.

- **Latency (p99):** Compared with a Mann-Whitney U test or a bootstrapped percentile comparison, because latency is skewed and not normally distributed (p < 0.05).
- **Error rate:** Compared with a chi-squared test, or Fisher's exact test when counts are low.
- **Minimum sample size:** No pass or fail verdict is issued until at least 1,000 requests have been served by the canary. Below that, the phase continues.
- **Baseline comparison:** The canary must stay within 2 to 3 standard deviations of the baseline. The baseline is the same hour on the previous weeks (for example, the same weekday and hour over the last 4 weeks), because banking traffic has strong daily and weekly patterns.

---

## 4. Zero-Downtime Database Migration (Expand-Contract)

Blue and Green share one database, so every schema change must work with both application versions.

1. **EXPAND (backward compatible):** Add new columns or tables. Both V(N-1) and V(N) work.
2. **MIGRATE (backfill):** A throttled batch job copies data from old to new columns.
3. **SWITCH:** The application reads and writes the new structure (dual-write during transition).
4. **CONTRACT (cleanup):** Drop the old column in a **separate deployment** with its own approval gate.

### Rules
- CONTRACT runs only after the 24-hour bake and a defined rollback window. After CONTRACT, the old version cannot run again, so the fix path is forward-only.
- Use `lock_timeout` and `CREATE INDEX CONCURRENTLY` (PostgreSQL) so migrations do not block live traffic.
- A CI step lints migrations and blocks destructive statements (`DROP`, `TRUNCATE`, unbatched `UPDATE`) outside a CONTRACT release.

---

## 5. Automated Rollback

### Triggers

| Category | Trigger | Threshold | Response |
|---|---|---|---|
| A (immediate) | HTTP 5xx rate | > 5% for 60 s | Detect within 60 s, reroute within 30 s |
| A (immediate) | Pod crash | CrashLoopBackOff | Detect within 60 s, reroute within 30 s |
| A (immediate) | Payment success rate | Drops more than 2 percentage points below baseline for 60 s | Automatic rollback |
| A (immediate) | Transaction failure rate | > 1% for 60 s | Automatic rollback |
| B (escalated) | p99 latency | > 2x baseline for 5 min | Alert on-call; automatic rollback if no response in 10 min |
| B (escalated) | DB connection pool | > 90% used | Alert on-call; automatic rollback if no response in 10 min |

### Threshold Note
Canary gates use strict thresholds during rollout (for example, 0.1% errors) so problems are caught at low traffic. Category A triggers are emergency thresholds that apply at any stage, including after full traffic shift.

---

## 6. Implementation Files and Compliance

| Item | Location |
|---|---|
| Blue-green manifests and Istio VirtualService | `pipeline/helm/` |
| Argo Rollout and AnalysisTemplate | `pipeline/helm/` |
| Migration SQL examples | `docs/04-database-migration/` |
| Compliance mapping (RBI, PCI-DSS v4.0, SoD) | `docs/03-compliance-gates/README.md` |

Production deployment requires manual approval from a person other than the change author. This is enforced with GitHub Environments required reviewers and is mapped to the separation-of-duties controls in the compliance document.

---

## AI Attribution
- **Tool used:**  Claude
- **Prompt:** "Design blue-green and canary deployment strategies with statistical analysis and expand-contract DB migrations for a banking app."
- **Human review:** Content customized for the NovaPay architecture and RBI compliance context.
