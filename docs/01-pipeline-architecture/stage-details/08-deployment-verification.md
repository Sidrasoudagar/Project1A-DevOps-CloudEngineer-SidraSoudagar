# Stage 8: Deployment & Verification

## Overview
Deploys the approved, signed artefact to production using only the pipeline identity, verifies health and security after release, and rolls back automatically on failure.

## Tool & Version
- **Primary Tool:** Argo CD with Argo Rollouts (progressive delivery), plus post-deploy smoke tests and an authenticated verification scan. Versions pinned and recorded in the tool register.
- **Alternative:** Spinnaker or Flux.

## Inputs
- Signed artefact digest and evidence bundle from Stage 7
- Approved change record and change window
- Deployment manifests (reviewed, version-controlled)
- Health and SLO definitions for the service
- Post-deploy smoke test suite and scan profile

## Configuration Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Deploy identity | Production deploys by the pipeline identity only; no human deploy rights | PCI 6.5.4; RBI 9(b), 19 |
| Signature verification | Cluster admission rejects unsigned or unverified artefacts | Only approved builds run (RBI 13) |
| Environment isolation | Credentials and network scoped to the target environment | PCI 6.5.3 |
| Change window | Deploy only within the approved window for the change record | Controlled change (RBI 13) |
| Rollout strategy | Canary, then progressive increase with automated analysis | Limits impact of a faulty release |
| Auto-rollback | Roll back on failed health check, SLO breach or error-rate threshold | RBI 13(d); PCI 6.5.1 |
| Post-change verification | Authenticated scan and control checklist after significant changes | PCI 6.5.2, 11.3.1.3, 11.3.2.1; RBI 26 |
| Test data and accounts | Final check that no test accounts or default credentials exist in production | PCI 6.5.6 |
| Deployment logging | Deploy, rollback and config events sent to central, tamper-evident log | PCI 10.2.1.2, 10.2.1.7; RBI 15 |

## Quality Gates
| Gate | Threshold | Action on Failure |
|------|-----------|-------------------|
| G10 Environment isolation | Identity scoped to target environment; no cross-environment secrets | Block deploy |
| Admission control | Artefact signature and digest match the evidence bundle | Reject deployment |
| G11 Deploy and rollback | Health checks and SLOs pass at each canary step | Automatic rollback |
| G12 Post-change verification | Smoke tests pass; authenticated scan shows no new unwaived High or Critical findings | Raise incident or block next release |
| G14 Log integrity | Deployment events present in the central log | Alert and freeze deployments |

## Failure Mode & Remediation
- **Failure:** Health check or SLO breach during rollout.
- **Remediation:** Automatic rollback to the last known good digest. The service owner investigates from the logged evidence before another attempt, and a new change record is raised if the fix needs code.
- **Failure:** Post-deploy scan finds a High or Critical issue, or required logging is missing.
- **Remediation:** Roll back or apply a hotfix through the full pipeline. Restore logging before any further deployments.
- **Exception Process:** Deploying outside the approved window needs the duty manager and a CISO delegate, with the exception logged and limited to 24 hours. Skipping post-deploy verification cannot be waived for critical systems. Rollback overrides are permitted only for the incident commander and are reviewed within 1 business day.

## SLA Target
- **Expected:** 10 minutes
- **Maximum:** 20 minutes (excludes approval and change-window wait time)

## Output Artefacts
- Deployment record (digest, environment, approver IDs, change ID, timestamps)
- Rollout and health analysis results
- Post-deploy verification report and scan result
- Rollback record where applicable
- Deployment and administrative audit events

## Regulatory Mapping
| Framework | Requirement | How This Stage Satisfies It |
|-----------|-------------|----------------------------|
| RBI | 13(a)-(d) Change management including recovery | Approved, windowed deployment with automatic rollback for failed changes |
| RBI | 19 Access control | Production deploy is limited to the pipeline identity; no standing human access |
| RBI | 15 Audit trails | Deployment events logged with actor, target and outcome |
| RBI | 26 Vulnerability assessment after major changes | Post-deploy authenticated scan after significant changes |
| PCI-DSS v4.0 | 6.5.1 Secure change procedures including return to secure state | Approval, testing and automatic rollback |
| PCI-DSS v4.0 | 6.5.2 Confirm requirements after significant change | Post-change checklist and verification report |
| PCI-DSS v4.0 | 6.5.3, 6.5.4, 6.5.6 Environment and role separation; no test accounts | Scoped identity, pipeline-only deploys, final test-account check |
| PCI-DSS v4.0 | 10.2 Audit logs | Deployment and administrative events captured with required fields |
| PCI-DSS v4.0 | 11.3.1.3, 11.3.2.1 Scans after significant change | Post-deploy scan triggered automatically |

## AI Attribution
- **Tool:** Claude (Anthropic)
- **Date:** 2026-10-11
- **Human review:** Drafted for NovaPay; pending human review. Reviewer name and date to be recorded here.
