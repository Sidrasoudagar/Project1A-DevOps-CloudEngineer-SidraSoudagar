# Stage 2: Build & Compilation

## Overview
Produces a reproducible, signed build artefact and its SBOM on an ephemeral, isolated runner, and stops the pipeline if secrets or test data are found in the source.

## Tool & Version
- **Primary Tool:** GitLab CI on ephemeral, isolated runners with BuildKit, Syft (CycloneDX SBOM), Cosign (artefact signing) and Gitleaks (secrets). Versions pinned by digest and recorded in the NovaPay tool register.
- **Alternative:** Tekton or Jenkins with equivalent ephemeral agents.

## Inputs
- Commit SHA from Stage 1 (signed, approved)
- Pinned base images and dependency lock files
- Build definition (pipeline-as-code, reviewed under Stage 1 controls)
- Secrets-scan and test-data rule sets

## Configuration Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Runners | Ephemeral, single-use, no inbound access, no long-lived credentials | Limits tampering and credential theft (RBI 19; PCI 6.5.3) |
| Base images | Approved registry only; pinned by digest | Controlled provenance and repeatability |
| Dependency resolution | Lock files required; internal proxy or mirror only | Prevents unreviewed components being pulled in |
| Secrets scan | Gitleaks over the commit range and full history on first run; custom PAN and key patterns | PCI 6.5.5, 6.5.6; keeps credentials out of artefacts |
| Test-data scan | Fixtures and seed data scanned for live PAN patterns, test accounts and default credentials | PCI 6.5.5, 6.5.6 |
| SBOM | CycloneDX generated for every build, attached to the artefact | PCI 6.3.2; RBI 12(g) |
| Artefact signing | Cosign signature with key held in HSM or KMS; signed by the pipeline identity only | Integrity and attribution (RBI 15) |
| Build provenance | Record commit SHA, builder identity, inputs and digest | Forensic trace from artefact to source |
| Build logging | Start, stop, failure and config events to central log store | PCI 10.2.1.6, 10.2.1.7 |

## Quality Gates
| Gate | Threshold | Action on Failure |
|------|-----------|-------------------|
| G5 Secrets and test-data scan | Zero live PAN patterns, credentials, test accounts or default credentials | Fail build |
| Reproducible build | Compiles from locked inputs with no network access beyond the approved mirror | Fail build |
| SBOM generated | Present, valid CycloneDX, matches artefact digest | Fail build |
| Artefact signed | Signature verifies against the pipeline identity | Fail build |

## Failure Mode & Remediation
- **Failure:** Secrets or live PAN patterns detected.
- **Remediation:** Remove the data, rotate any exposed credential immediately, and purge it from history where needed. If a real PAN was found, treat it as a security incident.
- **Failure:** Build not reproducible, or a dependency cannot be resolved from the approved mirror.
- **Remediation:** Update the lock file through a normal reviewed MR. Request the component be added to the approved mirror after Stage 4 checks.
- **Exception Process:** Secrets and PAN findings cannot be waived; only a documented false positive may be suppressed, approved by the CISO's delegate and expiring in 90 days. Other build-gate waivers: service owner plus security approver, maximum 14 days.

## SLA Target
- **Expected:** 8 minutes
- **Maximum:** 15 minutes

## Output Artefacts
- Signed build artefact or container image with digest
- CycloneDX SBOM
- Build provenance record
- Secrets and test-data scan report
- Build and runner audit events

## Regulatory Mapping
| Framework | Requirement | How This Stage Satisfies It |
|-----------|-------------|----------------------------|
| RBI | 12(g) Assurance on vulnerabilities and malware in delivered software | SBOM and provenance give the component inventory needed for later scans and vendor attestations |
| RBI | 13 Change and patch management | Only the approved commit is built, and the artefact is immutable and traceable |
| RBI | 15 Audit trails | Signed artefacts, provenance and build logs support forensics and non-repudiation |
| RBI | 19 Access control | Ephemeral runners with no standing credentials; build identity separated from human users |
| PCI-DSS v4.0 | 6.2.1 Secure development | Controlled, repeatable build forms part of the documented secure SDLC |
| PCI-DSS v4.0 | 6.3.2 Software inventory | SBOM generated per build |
| PCI-DSS v4.0 | 6.5.5, 6.5.6 No live PAN and no test data or accounts in production | Automated scans block builds containing PAN patterns, test accounts or default credentials |
| PCI-DSS v4.0 | 10.2.1.6, 10.2.1.7 Log changes and system-object events | Build and runner lifecycle events logged centrally |

## AI Attribution
- **Tool:** Claude (Anthropic)
- **Date:** 2026-10-11
- **Human review:** Drafted for NovaPay; pending human review. Reviewer name and date to be recorded here.
