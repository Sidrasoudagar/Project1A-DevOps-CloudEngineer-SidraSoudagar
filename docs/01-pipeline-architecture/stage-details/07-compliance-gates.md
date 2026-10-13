# Stage 7: Policy & Compliance Gates

## Overview
Evaluates the evidence from Stages 1 to 6 against policy-as-code, enforces segregation of duties and waiver rules, and writes the tamper-evident evidence bundle that authorises deployment.

## Tool & Version
- **Primary Tool:** Open Policy Agent with Conftest, writing evidence to write-once (object-lock) storage. Versions pinned and recorded in the tool register.
- **Alternative:** Kyverno or HashiCorp Sentinel.

## Inputs
- Evidence from earlier stages (change record, approvals, SAST, SCA/SBOM, contract tests, DAST)
- Policy bundle (versioned, signed, Board- or committee-approved version IDs)
- Role assignments from the identity provider
- Waiver register with approvers and expiry dates
- Scan-currency data (last VA, PT, internal and ASV scan dates per system)
- Release request naming author, release approver and target environment

## Configuration Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Policy source | Policy bundle in a protected repo; each rule cites a policy version ID | Traceability to approved policy (RBI 4, 5) |
| SoD rule | Author, release approver and deployer must be three different identities | RBI 9(b), 23(b); PCI 6.5.4 |
| Security gate ownership | Gate policy changes need CISO-office approval; Head of IT cannot waive alone | RBI 24(c) |
| Waiver validity | Approver, scope and expiry required; expired waivers are ignored | RBI 7; time-bound exceptions |
| Scan-currency rule | VA within 6 months, PT within 12 months for critical systems; internal and ASV scans within 3 months | RBI 26; PCI 11.3.1, 11.3.2 |
| Evidence bundle | Hash-chained, signed, stored write-once, retained per policy | RBI 15; PCI 10.3 |
| Log integrity check | Verifies central logging active with no gaps for the pipeline | PCI 10.2, 10.3 |
| Policy review date | Gate fails if the governing policy is past its annual review date | RBI 5 |

## Quality Gates
| Gate | Threshold | Action on Failure |
|------|-----------|-------------------|
| G9 Release approval and SoD | Three distinct identities; release approver authorised; security gates green | Block deploy |
| G13 Scheduled VA/PT currency | All scan dates within required periods for the target system | Block release to that system |
| G14 Log integrity | Logging active, records signed, no gaps | Alert and freeze deployments |
| G15 Waiver control | Every waiver valid; CISO-approved for security gates | Reject waiver and block |
| Evidence completeness | All required evidence present and hash-verified | Block deploy |
| Policy currency | Governing policy within annual review | Warn 30 days before; block after |

## Failure Mode & Remediation
- **Failure:** Same person appears as author and release approver, or approver lacks the release role.
- **Remediation:** Assign a different authorised approver and resubmit. Role assignments are fixed only through the access-management process.
- **Failure:** Required scan overdue for the target system, or evidence missing.
- **Remediation:** Complete the scan or obtain the missing evidence. The pipeline can schedule and track independent tests but cannot perform them.
- **Exception Process:** Waivers on this stage need CISO approval and Steering Committee notification, with a maximum of 14 days. SoD and log-integrity failures cannot be waived. All waivers feed the quarterly ITSC pack.

## SLA Target
- **Expected:** 2 minutes
- **Maximum:** 5 minutes

## Output Artefacts
- Signed policy-decision record (inputs, rules, policy versions, result)
- Evidence bundle with hash and storage location
- Waiver usage log
- Control metrics for the quarterly ITSC pack
- Gate-decision audit event

## Regulatory Mapping
| Framework | Requirement | How This Stage Satisfies It |
|-----------|-------------|----------------------------|
| RBI | 4, 5, 6, 7 Governance framework and oversight | Policy versions, exception routing and committee reporting built into the gate |
| RBI | 9(b), 23(b) Segregation of duties | Three-identity rule enforced automatically |
| RBI | 24(c) CISO independence | Security-gate changes and waivers need CISO-office approval |
| RBI | 15 Audit trails | Signed, write-once evidence bundle |
| RBI | 26 Vulnerability assessment and PT cadence | Scan-currency check blocks releases to systems with overdue tests |
| RBI | 30 IS audit | Auditors have read-only access to evidence for continuous auditing |
| PCI-DSS v4.0 | 6.5.1, 6.5.4 Change approval and role separation | Documented approval and separation of roles before production |
| PCI-DSS v4.0 | 10.2, 10.3 Audit logs and their protection | Log-integrity gate and write-once evidence storage |
| PCI-DSS v4.0 | 11.3.1, 11.3.2 Quarterly internal and external scans | Scan-currency rule verifies evidence exists; the scans themselves run separately |

## AI Attribution
- **Tool:** Claude (Anthropic)
- **Date:** 2026-10-11
- **Human review:** Drafted for NovaPay; pending human review. Reviewer name and date to be recorded here.
