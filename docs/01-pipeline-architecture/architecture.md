# Deliverable 1: Zero-Downtime CI/CD Pipeline Architecture

**Project:** NovaPay Digital Bank
**Author:** Sidra Soudagar
**Date:** [Today's date]

---

## 1. Executive Summary

NovaPay Digital Bank currently runs manual SSH deployments with a 4.5-hour MTTR, fortnightly deployment cycles, and 17 outstanding RBI audit non-conformances. This document specifies an 8-stage zero-downtime CI/CD pipeline that reduces commit-to-production time to under 2 hours while achieving five-nines availability and full RBI/PCI-DSS v4.0 compliance.

---

## 2. The 8 Canonical Pipeline Stages

### Stage 1: Source Control & Trigger
- **Tool:** GitHub Enterprise
- **Input:** Developer commit or pull request
- **Controls:** Branch protection on `main`, signed commits (GPG/SSH), mandatory PR review
- **Trigger:** Push to `main` or PR merge
- **Output:** Webhook event to pipeline orchestrator
- **Failure Mode:** Rejected commit if signature invalid
- **SLA:** < 1 minute

### Stage 2: Build & Compilation
- **Tool:** Gradle (Java 21 / Spring Boot 3.x) + Docker multi-stage build
- **Input:** Source code from Stage 1
- **Controls:** Dependency lock file enforcement, unit tests, coverage check
- **Output:** Container image tagged with SemVer + Git SHA
- **Gate:** 80% line coverage, 70% branch coverage, 0 test failures
- **Failure Mode:** Pipeline blocked; developer notified
- **SLA:** 4 minutes

### Stage 3: Static Analysis & SAST
- **Tool:** SonarQube (custom banking quality profile)
- **Input:** Source code
- **Controls:** PII handling rules, encryption usage, SQL injection patterns
- **Gate:** 0 Critical, ≤2 High, technical debt ratio ≤5% for new code
- **Failure Mode:** Pipeline blocked; auto-ticket created
- **Exception:** CISO approval within 24 hours
- **SLA:** 3 minutes

### Stage 4: Dependency & Container Scanning
- **Tool:** Trivy (container scan) + Syft (SBOM generation)
- **Input:** Container image from Stage 2
- **Controls:** CVE severity gating, licence compliance (GPL blacklist)
- **Gate:** 0 Critical CVE, High blocked if CVSS > 8.0, SBOM in CycloneDX format
- **Failure Mode:** Pipeline blocked if CVSS ≥ 9.0
- **Exception:** 72-hour remediation window
- **SLA:** 2 minutes

### Stage 5: Integration & Contract Testing
- **Tool:** Pact (consumer-driven contracts) + Testcontainers
- **Input:** Container image + ephemeral test namespace
- **Controls:** API backward compatibility, database integration tests
- **Gate:** All contract tests pass, `can-i-deploy` returns compatible
- **Failure Mode:** Pipeline blocked; consumer/provider teams notified
- **SLA:** 6 minutes

### Stage 6: Dynamic Analysis & DAST
- **Tool:** OWASP ZAP (authenticated scan)
- **Input:** Staging deployment
- **Controls:** Active + passive scanning, OpenAPI spec input
- **Gate:** 0 Critical/High from OWASP Top 10
- **Failure Mode:** Pipeline blocked; risk acceptance form required
- **Exception:** TRC approval
- **SLA:** 5 minutes

### Stage 7: Policy & Compliance Gates
- **Tool:** OPA/Kyverno (K8s policies) + Cosign (image signing)
- **Input:** Kubernetes manifests + signed image
- **Controls:** RBI technology risk codification, PCI-DSS checks, SoD enforcement
- **Gate:** All policies pass, image signed, dual approval for production
- **Failure Mode:** Deployment rejected; dual approval override required
- **SLA:** 3 minutes

### Stage 8: Deployment & Verification
- **Tool:** Argo Rollouts + Istio VirtualService
- **Input:** Signed image + approved manifests
- **Controls:** Blue-green or canary execution, post-deploy smoke tests
- **Gate:** SLOs met (error rate < 0.1%, p99 < 200ms), automated rollback ready
- **Failure Mode:** Automated rollback triggered within 60 seconds
- **SLA:** 10 minutes

---

## 3. Pipeline Flow Summary

| # | Stage | Duration | Gate |
|---|-------|----------|------|
| 1 | Source Control | < 1 min | Signed commits |
| 2 | Build | 4 min | 80% coverage |
| 3 | SAST | 3 min | 0 Critical, ≤2 High |
| 4 | Dependency & Container | 2 min | 0 Critical CVE |
| 5 | Integration & Contract | 6 min | All tests pass |
| 6 | DAST | 5 min | 0 Critical/High |
| 7 | Compliance Gates | 3 min | All policies pass |
| 8 | Deployment | 10 min | SLOs met |

**Total:** 34 minutes (well under the 2-hour target)

---

## 4. Parallel Execution

Stages 3 (SAST) and 4 (Dependency & Container Scan) run in parallel. This saves approximately 3 minutes.

---

## 5. Zero-Downtime Guarantee

- **Blue-Green:** Two identical environments; atomic traffic switch via Istio VirtualService
- **Canary:** 4-phase rollout (1-2% → 5-10% → 25-50% → 100%)
- **Database:** Expand-contract migration pattern (add → backfill → cutover → drop)
- **Rollback:** Automated within 60 seconds for Category A triggers

---

## 6. Compliance Mapping

| Stage | RBI Section | PCI-DSS v4.0 |
|-------|-------------|--------------|
| SAST | 5.1 (Vulnerability Assessment) | 6.2 (Bespoke Software Security) |
| Dependency Scan | 5.1 | 6.3 (Security Vulnerabilities) |
| DAST | 5.1 | 6.4 (Public-Facing Web App Protection) |
| Compliance Gates | 4.2 (Change Management) | 6.5 (Change Management Processes) |
| Deployment | 4.3 (Segregation of Duties) | 10.2 (Audit Log Recording) |

---

## 7. AI Attribution

- **Tool used:** [ChatGPT / Claude / Gemini]
- **Prompt:** "Design an 8-stage CI/CD pipeline for a regulated bank..."
- **Date generated:** [Today's date]
- **Human review:** Customized for NovaPay banking context with RBI/PCI-DSS mapping.
