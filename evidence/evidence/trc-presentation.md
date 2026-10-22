# NovaPay TRC Presentation: Zero-Downtime CI/CD Architecture

## Slide 1: Title Slide
- **Project:** NovaPay Digital Bank Zero-Downtime CI/CD
- **Presenter:** Sidra Soudagar (DevOps Lead)
- **Audience:** Technology Risk Committee (TRC)
- **Date:** October 19 2026

## Slide 2: The Current Crisis (Problem Statement)
- **Manual Deployments:** SSH into servers (High human error risk).
- **Frequency:** Once every 2 weeks (Too slow).
- **MTTR:** 4.5 Hours (Unacceptable for UPI).
- **Compliance:** 17 outstanding RBI audit non-conformances.

## Slide 3: The Goal (Target State)
- **Velocity:** Deploy multiple times per day.
- **Safety:** Zero-downtime (Five-nines availability).
- **Recovery:** MTTR < 15 minutes (Automated rollback).
- **Compliance:** 100% automated audit trails mapped to RBI & PCI-DSS.

## Slide 4: Solution Architecture (The 8-Stage Pipeline)
- Stage 1: Source Control (GitHub)
- Stage 2: Build (Gradle)
- Stage 3 & 4: Security (SonarQube, Trivy) - *Parallel*
- Stage 5 & 6: Testing (Pact, OWASP ZAP)
- Stage 7: Compliance (OPA, Cosign)
- Stage 8: Deployment (ArgoCD, Istio)

## Slide 5: Zero-Downtime Deployment Strategy
- **Blue-Green:** Instant traffic switch via Istio.
- **Canary:** 1% -> 5% -> 25% -> 100% with statistical analysis.
- **Database:** Expand-Contract pattern (No locking of 100M rows).

## Slide 6: Automated Rollback (The Safety Net)
- **Category A (<60s):** Auto-rollback on HTTP 5xx spike or Pod crash.
- **Category B (<15m):** Auto-rollback on latency spike if on-call doesn't respond.
- **Category C:** Manual rollback for minor bugs.

## Slide 7: Compliance Gates (RBI & PCI-DSS)
- **SAST:** 0 Critical. (PCI 6.2 / RBI 5.1)
- **DAST:** 0 Critical/High. (PCI 6.4)
- **Dependency:** 0 Critical CVE. (PCI 6.3)
- **Separation of Duties:** Enforced via GitHub Environments (PCI 6.5).

## Slide 8: Audit Trail Evidence
- Every gate execution writes an immutable JSON log to S3 (WORM).
- Retention: 7 years.
- Includes: Commit SHA, Gate Status, Approver ID, Regulatory Mapping.

## Slide 9: Observability & DORA Metrics
- **Dashboard 1:** Engineering (Live errors, p99 latency).
- **Dashboard 2:** Management (Deployment Frequency, Lead Time).
- **Dashboard 3:** Audit (Gate pass rates, Exception logs).

## Slide 10: Incident Response Playbook
- **SEV-1:** < 5 min response. Page CTO/CISO. Update status page.
- **SEV-2:** < 15 min response. Page VP Eng.
- **Post-Mortem:** Mandatory blameless review within 48 hours.

## Slide 11: Database Migration (Expand-Contract)
- **Expand:** Add new column (App V1 and V2 both work).
- **Migrate:** Backfill 100M rows with `pgroll` (Throttled).
- **Contract:** DBA approval gate to drop old column.

## Slide 12: Developer Experience (Dev Team Persona)
- **Friction:** Pipeline runs in < 35 minutes.
- **Self-Service:** Ephemeral environments for testing.
- **Feedback:** Fast PR feedback loops (Tests + SAST run in parallel).

## Slide 13: Risk Mitigation (CISO Persona)
- **Supply Chain:** Trivy SBOM + Cosign Image Signing.
- **Network:** Istio mTLS for all service-to-service traffic.
- **Secrets:** HashiCorp Vault with 90-day rotation.

## Slide 14: Implementation Timeline (90 Days)
- **Month 1:** Setup GitHub, Terraform, and base pipeline. (Stages 1-4)
- **Month 2:** Integrate DAST, Pact, and Blue-Green deployment.
- **Month 3:** Implement OPA gates, Canary, and TRC Audit.

## Slide 15: Cost & ROI
- **Cost:** Cloud infrastructure increase (Argo, Istio, Prometheus).
- **Savings:** Eliminate 4.5-hour outages (Costing ₹X Lakhs/hour).
- **Efficiency:** 50+ developers save 2 hours/week on manual deployments.

## Slide 16: Addressing RBI Non-Conformances
- **NC 1:** Manual testing -> Automated DAST/SAST gates.
- **NC 2:** No audit trail -> Immutable JSON logs.
- **NC 3:** No SoD -> Dual approval on GitHub.

## Slide 17: Next Steps
1. TRC Approval today.
2. Kick-off engineering sprint next Monday.
3. First pipeline deployment to Staging in 4 weeks.

## Slide 18: Q&A Preparation (Anticipated Questions)
- *Q: What if OPA blocks a critical hotfix?* -> A: CISO dual-approval override logged in Jira.
- *Q: How do you handle DB locks?* -> A: `pgroll` and batch throttling (1000 rows/100ms).
- *Q: What if Istio fails?* -> A: Route53 DNS failover to backup load balancer.

## Slide 19: Summary
- Faster deployments.
- Zero downtime.
- 100% RBI/PCI-DSS compliance.
- Happy developers.

## Slide 20: Thank You & Approval Request
- Formal request to approve the NovaPay CI/CD Architecture.

---
## AI Attribution
- **Tool used:** DeepSeek
- **Human review:** Content structured for TRC presentation.
