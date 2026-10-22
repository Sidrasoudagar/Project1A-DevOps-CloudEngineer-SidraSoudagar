# Stage Details: The 8 Canonical Stages

This folder contains the detailed technical specifications for each stage of the NovaPay CI/CD pipeline. 

Each document defines the tool, configuration parameters, numeric quality gates, failure modes, and regulatory mapping (RBI / PCI-DSS).

## Stage Index

1. **[Stage 1: Source Control](./01-source-control.md)** - GitHub Enterprise, signed commits, branch protection.
2. **[Stage 2: Build & Compilation](./02-build.md)** - Gradle, unit tests, coverage gates.
3. **[Stage 3: SAST](./03-sast.md)** - SonarQube, vulnerability scanning.
4. **[Stage 4: Dependency & Container Scan](./04-dependency-container-scan.md)** - Trivy, SBOM generation.
5. **[Stage 5: Integration & Contract Testing](./05-integration-contract-testing.md)** - Pact, API compatibility.
6. **[Stage 6: DAST](./06-dast.md)** - OWASP ZAP, runtime security scanning.
7. **[Stage 7: Compliance Gates](./07-compliance-gates.md)** - OPA/Kyverno, image signing, SoD.
8. **[Stage 8: Deployment & Verification](./08-deployment-verification.md)** - Argo Rollouts, Blue-Green, Canary.

---
*Note: These stages are executed in the exact order listed above, with Stages 3 and 4 running in parallel to reduce total pipeline execution time.*
