# Stage 3: Static Analysis (SAST)

## Overview
Analyses NovaPay's own source code for security defects before release and blocks the pipeline on unwaived high-severity findings.

## Tool & Version
- **Primary Tool:** Semgrep with NovaPay-maintained rule sets. Version and rule-set version pinned and recorded in the tool register.
- **Alternative:** SonarQube (security rules) or Checkmarx.

## Inputs
- Source at the Stage 1 commit SHA
- NovaPay rule set (injection, access control, crypto misuse, business-logic patterns for payments)
- Existing waiver register (finding ID, approver, expiry)
- Baseline of previously triaged findings

## Configuration Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Scan scope | Full scan on merge to protected branch; diff scan on MRs; nightly full scan | Fast feedback plus complete coverage |
| Rule coverage | Attack classes required by PCI 6.2.4: injection, data-structure attacks, crypto misuse, business-logic abuse, access control, other high-risk flaws | Evidence that methods exist against common attacks |
| Severity model | Critical, High, Medium, Low, mapped to CVSS-style scoring where applicable | Consistent risk ranking (RBI 26) |
| Waiver handling | Waiver must have finding ID, justification, approver and expiry | Controlled exceptions (RBI 7, 24(c)) |
| Rule updates | Rule set versioned and reviewed through the Stage 1 process | Prevents silent weakening of checks |
| Result integrity | Results written by a security-owned service account, not by the project team | Independence of the check (RBI 26(c) principle) |

## Quality Gates
| Gate | Threshold | Action on Failure |
|------|-----------|-------------------|
| G3 SAST | 0 unwaived Critical or High findings | Fail build |
| Medium findings | Triaged within 30 days; none past due date | Warn, then block after due date |
| Scan completeness | 100% of changed files analysed; scan did not time out or skip | Fail build |
| Rule-set integrity | Rule-set version matches approved version | Fail build |

## Failure Mode & Remediation
- **Failure:** High or Critical finding in changed code.
- **Remediation:** Fix the defect and push a new commit; approvals reset under Stage 1 rules. Consult the secure-coding guidance for the flagged class.
- **Failure:** Suspected false positive.
- **Remediation:** Submit a false-positive request with evidence to the security team. Do not edit rules or inline suppressions without review.
- **Exception Process:** Waivers for High findings need the service owner and a CISO delegate, with a maximum of 30 days. Critical findings need CISO approval, maximum 14 days. The Head of IT cannot waive alone. All active waivers are reported to the Information Security Committee quarterly.

## SLA Target
- **Expected:** 6 minutes
- **Maximum:** 12 minutes

## Output Artefacts
- SAST report (findings, severity, rule IDs, rule-set version)
- Waiver references applied
- Scan coverage record (files analysed)
- Trend data for the quarterly ITSC pack

## Regulatory Mapping
| Framework | Requirement | How This Stage Satisfies It |
|-----------|-------------|----------------------------|
| RBI | 26 Vulnerability assessment across the lifecycle | Automated code-level assessment before release with time-bound fixes |
| RBI | 12(g) Assurance on vulnerabilities in delivered software | Same analysis applied to vendor-supplied source where available |
| RBI | 24(c) CISO independence | Security owns the rules and the waiver decision |
| PCI-DSS v4.0 | 6.2.3 Review of code before release | Automated review of all changed code before production |
| PCI-DSS v4.0 | 6.2.4 Methods against common attacks | Rule coverage mapped to required attack classes |
| PCI-DSS v4.0 | 6.2.1 Secure development per industry standards | SAST is a mandatory stage in the secure SDLC |

## AI Attribution
- **Tool:** Claude (Anthropic)
- **Date:** 2026-10-11
- **Human review:** Drafted for NovaPay; pending human review. Reviewer name and date to be recorded here.
