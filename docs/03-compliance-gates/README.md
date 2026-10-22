# Deliverable 3: Compliance Gates

This folder contains the automated regulatory gates mapped to RBI and PCI-DSS v4.0.

## Contents
- **[compliance-gates.md](./compliance-gates.md)**: The 10 automated gates, thresholds, exception workflows, and audit JSON schema.
- **[no-privileged-containers.rego](./no-privileged-containers.rego)**: OPA policy to block privileged Kubernetes containers.
- **[gate-orchestration-diagram.md](./gate-orchestration-diagram.md)**: Flowchart showing how gates block bad code.
