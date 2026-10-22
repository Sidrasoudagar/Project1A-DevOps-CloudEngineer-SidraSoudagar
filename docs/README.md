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

## 🗺️ Navigation Guide

Click the links below to explore the deliverables:

- 📁 **[01 - Pipeline Architecture](./docs/01-pipeline-architecture/architecture.md)** - The 8-stage design and stage specifications.
- 📁 **[02 - Deployment Strategies](./docs/02-deployment-strategies/deployment-strategy.md)** - Blue-Green, Canary, and Expand-Contract DB migrations.
- 📁 **[03 - Compliance Gates](./docs/03-compliance-gates/compliance-gates.md)** - 7 automated gates mapped to RBI and PCI-DSS.
- 📁 **[04 - Database Migration](./docs/04-database-migration/migration-strategy.md)** - Zero-downtime schema changes for 100M+ rows.
- 📁 **[05 - Environment Promotion](./docs/05-environment-promotion/promotion-workflow.md)** - Dev → Staging → Pre-Prod → Prod workflow.
- 📁 **[06 - Rollback Specification](./docs/06-rollback-specification/rollback-spec.md)** - Automated rollback categories and triggers.
- 📁 **[07 - Runbook & Playbook](./runbooks/deployment-runbook.md)** - 3 AM operational procedures.
- 📁 **[08 - Observability](./docs/08-observability/observability-strategy.md)** - DORA metrics and Grafana dashboards.
- 📁 **[TRC Presentation](./evidence/trc-presentation.md)** - Committee presentation outline.
- 📁 **[Incident Simulation](./evidence/incident-simulation-2026-10-16.md)** - Post-mortem of the Friday 5 PM disaster.

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
