# Documentation
Placeholder for NovaPay CI/CD pipeline documentation.

# Project1A: DevOps & Cloud Engineer - Zero-Downtime CI/CD Pipeline
**Target Organization:** NovaPay Digital Bank (Fictional RBI-Licensed Entity)
**Author:** Sidra Soudagar
**Date:** October 2026

---

## Executive Summary

NovaPay Digital Bank currently operates with manual SSH deployments, a 4.5-hour MTTR, and 17 outstanding RBI audit non-conformances. This project delivers a production-grade, zero-downtime CI/CD pipeline architecture that solves these issues. 

The solution implements an 8-stage pipeline combining rigorous security scanning (SAST, DAST, Trivy), automated compliance gates (mapped to RBI & PCI-DSS v4.0), and Infrastructure as Code. It utilizes Blue-Green and Canary deployment strategies via Argo Rollouts and Istio to achieve five-nines availability and reduce commit-to-production time to under 35 minutes. The architecture includes a comprehensive observability strategy and automated rollback triggers to reduce MTTR to under 15 minutes.

---

## 📑 Table of Contents

### [01. Pipeline Architecture](./01-pipeline-architecture/README.md)
- The 8-stage pipeline design.
- Stage-by-stage specifications (Build, SAST, DAST, etc.).

### [02. Deployment Strategies](./02-deployment-strategies/README.md)
- Blue-Green and Canary deployment flows.
- Traffic routing and Expand-Contract database patterns.

### [03. Compliance Gates](./03-compliance-gates/README.md)
- The 10 automated regulatory gates (RBI & PCI-DSS).
- OPA policies and exception workflows.

### [04. Database Migration](./04-database-migration/README.md)
- Zero-downtime Expand-Contract strategy.
- SQL scripts and version compatibility matrix.

### [05. Environment Promotion](./05-environment-promotion/README.md)
- The 4-environment model (Dev → Staging → Pre-Prod → Prod).
- Approval gates and data masking rules.

### [06. Rollback Specification](./06-rollback-specification/README.md)
- Category A, B, and C rollback triggers.
- Automated recovery flows and Prometheus alerts.

### [07. Runbook & Playbook](../runbooks/README.md) *(Located in root `runbooks/` folder)*
- 3 AM operational deployment runbook.
- Incident response playbook and communication templates.

### [08. Observability](./08-observability/README.md)
- DORA metrics and Grafana dashboard designs.
- Alerting routing strategy.


---

## 🛠️ Tools & Technologies Used

- **CI/CD:** GitHub Actions
- **Container & Orchestration:** Docker, Kubernetes (EKS), Helm
- **Security (DevSecOps):** SonarQube (SAST), OWASP ZAP (DAST), Trivy (SCA)
- **Policy as Code:** OPA (Open Policy Agent)
- **GitOps & Deployment:** ArgoCD, Argo Rollouts, Istio
- **Infrastructure as Code:** Terraform
- **Observability:** Prometheus, Grafana
- **Database Migration:** PostgreSQL, `pgroll` (Expand-Contract)

---

## 🔒 Security & Compliance

- **RBI Master Direction:** Mapped to change management (4.2) and segregation of duties (4.3).
- **PCI-DSS v4.0:** Mapped to requirements 6.2, 6.3, 6.4, 6.5, and 10.2.
- **Repo Compliance:** This repository is strictly PRIVATE and adheres to the NDA. All AI usage is attributed in individual files.

---
*End of README.*
