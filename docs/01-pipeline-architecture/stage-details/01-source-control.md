# Stage 1: Source Control & Trigger

## Overview
Every change enters the pipeline only through a reviewed, change-linked merge request on a protected branch, and the merge itself is what triggers the build.

## Tool & Version
- **Primary Tool:** GitLab Self-Managed (protected branches, CODEOWNERS, signed-commit enforcement). Version pinned in the NovaPay tool register; do not float.
- **Alternative:** GitHub Enterprise Server with equivalent branch rulesets.

## Inputs
- Merge request containing one or more commits
- Approved change record ID (e.g. CHG-12345) referenced in the MR metadata
- CODEOWNERS file and role-to-group mapping from the identity provider
- Developer training record feed (secure coding, refreshed every 12 months)
- Branch-protection policy-as-code (versioned, reviewed)

## Configuration Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Protected branches | Default and release branches: no direct push, no force-push, no deletion | Only reviewed changes reach production (PCI 6.5.4; RBI 13) |
| Required approvals | 1 independent CODEOWNER; 2 for payment-core / CDE repos | Reviewer differs from author (PCI 6.2.3.1) |
| Self-approval | Disabled; approvals reset when new commits are pushed |Prevents approve-then-change (RBI 9(b), 23(b)) |
| Commit signing | Required (SSH or GPG, verified) | Attribution and non-repudiation (RBI 15) |
| Change linkage | MR must reference a change ID; validated through the change-system API | Documented, approved change (RBI 13; PCI 6.5.1) |
| Authentication | SSO with MFA for all contributors; admin rights via just-in-time elevation | Need-based, supervised privileged access (RBI 19)|
| Pipeline trigger | Only on merge to protected branch or signed release tag; forks and external MRs get no secrets | Limits untrusted code reaching privileged runners |
| Training currency | Author and approver training date within 12 months | PCI 6.2.2 |
| Audit log streaming | Admin, permission and group-membership events sent to central log store | PCI 10.2.1.2, 10.2.1.5 |

## Quality Gates
| Gate | Threshold | Action on Failure |
|------|-----------|-------------------|
| G1 Change linkage | Valid change ID in an approved or scheduled state | Block merge|
| G2 Independent revie | Required approvals met, none by the author, CODEOWNERS satisfied|Block merge|
| Commit signature | 100% of commits in the MR verified |	Block merge |
| Training currency | Author and approver records current | Block merge; manager attestation fallback (see Exception Process)|

## Failure Mode & Remediation
- **Failure:** MR blocked because no valid change ID is attached, or the change is not approved. MR blocked because the only available approver is the author or is not a CODEOWNER.
- **Remediation:** Raise or link the change record, obtain approval, and re-run the check. No pipeline resources are consumed until the check passes. Request review from an eligible CODEOWNER on another team. Do not change CODEOWNERS in the same MR to unblock it.
- **Exception Process:** Emergency changes use a break-glass path approved by the on-call duty manager and a CISO delegate. The independent review is completed within 1 business day after merge, the exception is logged with an expiry of 24 hours, and all break-glass uses are reported to the Information Security Committee. Training-currency fallback: an engineering manager attestation valid for 14 days.

## SLA Target
- **Expected:** 2 minutes of automated checks (excludes human review time)
- **Maximum:** 5 minutes

## Output Artefacts
- MR approval record (approver IDs, timestamps, CODEOWNER match)
- Change-linkage record (change ID, state, approver)
- Commit-signature verification result
- Trigger metadata (commit SHA, pipeline ID, branch, actor)
- Access and administration audit events

## Regulatory Mapping
| Framework | Requirement | How This Stage Satisfies It |
|-----------|-------------|----------------------------|
| RBI | 9(b), 23(b) Segregation of duties and role conflicts | Author cannot approve; approvals reset on new commits; role conflicts checked against group membership |
| RBI | 13 Change management | Every change is documented, justified and approved before it can trigger the build |
| RBI | 19 Access control | SSO with MFA, just-in-time admin elevation, privileged activity logged |
| RBI | 15 Audit trails | Signed commits and approval records give attributable, forensic-grade history |
| PCI-DSS v4.0 | 6.2.3 / 6.2.3.1 Code review before release | Mandatory independent CODEOWNER review, not the author |
| PCI-DSS v4.0 | 6.2.2 Developer training | Training currency checked at merge time |
| PCI-DSS v4.0 | 6.5.1, 6.5.4 Secure change procedures and role separation | Change ID required; only approved, reviewed changes reach protected branches |
| PCI-DSS v4.0 | 10.2.1.2, 10.2.1.5 Admin actions and account changes logged | Administrative and permission events streamed to central logging |

## AI Attribution
- **Tool:** Claude (Anthropic)
- **Date:** [today]
- **Human review:** Drafted for NovaPay; pending human review. Reviewer name and date to be recorded here.
