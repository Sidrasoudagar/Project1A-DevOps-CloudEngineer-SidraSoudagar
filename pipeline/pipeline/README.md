# Pipeline Code & Configuration

This folder contains the actual code, configuration, and Infrastructure as Code (IaC) for the NovaPay CI/CD pipeline.

## Contents
- **[.github/workflows/](./.github/workflows/)**: GitHub Actions YAML files (CI pipeline, Policy tests).
- **[helm/](./helm/)**: Kubernetes Helm charts for deploying the application.
- **[terraform/](./terraform/)**: Terraform modules to provision the AWS VPC and EKS cluster.
- **[policies/](./policies/)**: OPA Rego policies and test files for compliance enforcement.
- **[argocd/](./argocd/)**: ArgoCD Application manifests for GitOps.
- **[scripts/](./scripts/)**: Prometheus alerting rules and utility scripts.
- **[migrations/](./migrations/)**: SQL scripts for the Expand-Contract database migration.

*Note: Policies are written for the OPA admission webhook format and tested with `opa test`.*
