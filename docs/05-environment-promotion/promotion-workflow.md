# Deliverable 5: Environment Promotion Workflow

**Project:** NovaPay Digital Bank
**Author:** Sidra Soudagar

---

## 1. The 4-Environment Model

| Environment | Purpose | Data Profile | Access Control | Deploy Trigger |
|-------------|---------|--------------|----------------|----------------|
| **Development** | Feature dev, unit testing | Synthetic mock data only | All Developers | Automatic on PR merge |
| **Staging** | Integration testing, DAST, Perf | Anonymized production-like data | Dev Team + QA | Automatic after Dev gates pass |
| **Pre-Production** | UAT, Compliance verification | Masked production data subset | QA + Compliance + DBA | Manual approval after Staging |
| **Production** | Live customer-facing | Real production data | SRE + Release Manager | Dual approval (RM + SRE Lead) |

---

## 2. Promotion Criteria (The Gates)

### Dev → Staging (Automated)
- All unit tests pass (100%).
- Code coverage ≥ 80% line, ≥ 70% branch.
- SAST: 0 Critical, ≤ 2 High findings.
- Build artifact signed and pushed to container registry.

### Staging → Pre-Prod (Manual Gate)
- Integration & contract tests pass.
- DAST: 0 Critical/High findings (OWASP Top 10).
- Performance test: p99 latency < 500ms under 2x expected load.
- Dependency scan: 0 Critical CVEs, SBOM generated.
- **Requires Tech Lead Approval.**

### Pre-Prod → Production (Dual Approval)
- UAT sign-off from Product Owner.
- All regulatory compliance gates passed (RBI + PCI-DSS).
- Database migration tested with production-scale data.
- Deployment runbook reviewed and signed by SRE Lead.
- **Requires CAB (Change Advisory Board) OR pre-approved change.**
- **Requires Dual Approval: Release Manager AND SRE Lead (Segregation of Duties).**
- Deployment window check: Not in blackout period.

---

## 3. Configuration Management ("Same Artifact, Different Config")

The exact same container image deployed to Dev must be promoted to Prod. **Code never changes between environments; only configuration does.**

### Secrets Management
- **Tool:** HashiCorp Vault.
- **Rule:** No plaintext secrets in Git, Helm values, or Kubernetes manifests.
- **Rotation:** 90-day rotation for database passwords, 30-day for API keys.

### Configuration Hierarchy
1.  **Base Config:** Shared across all environments (`values.yaml`).
2.  **Environment Override:** (`values-staging.yaml`, `values-production.yaml`).
3.  **Service Override:** Per-service customizations.

---

## 4. Data Masking & Privacy (PCI-DSS Compliance)

To comply with PCI-DSS (no real credit card data in non-prod), we use data masking.

| Environment | Customer Names | Credit Card Numbers | Passwords |
|-------------|----------------|---------------------|-----------|
| **Dev** | Fake ("John Doe") | Fake (`4111...`) | Fake |
| **Staging** | Anonymized (`User_892`) | Tokenized (`tok_123`) | Hashed |
| **Pre-Prod** | Masked (`J*** D**`) | Masked (`4111***`) | Hashed |
| **Prod** | Real | Real (Encrypted) | Hashed |

---

## AI Attribution
- **Tool used:** DeepSeek 
- **Human review:** Customized for NovaPay 4-env model.
