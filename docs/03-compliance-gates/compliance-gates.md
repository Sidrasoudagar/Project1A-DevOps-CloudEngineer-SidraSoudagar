# Deliverable 3: Compliance Gates Specification

**Project:** NovaPay Digital Bank
**Author:** Sidra Soudagar

---

## 1. Automated Compliance Gates

Every gate is a hard block. If a gate fails, the pipeline stops and production deployment is not possible unless a valid, independently approved exception exists (section 4). Gate 9 (separation of duties) cannot be overridden.

| # | Gate | Tool | Threshold | Action on failure | Exception approver (never the change author) | PCI-DSS v4.0 |
|---|---|---|---|---|---|---|
| 1 | SAST | SonarQube or Semgrep | 0 Critical, at most 2 High | Block build | CISO, within 24 hours | 6.2.1 to 6.2.4 |
| 2 | Dependency scan and secrets scan | Trivy (fs), Gitleaks | 0 Critical CVE; 0 secrets | Block build | CISO; 72-hour remediation window for CVEs | 6.3.1, 6.3.3 |
| 3 | Container image scan | Trivy (image) | 0 Critical; 0 High with a fix available | Block image promotion | CISO | 6.3.1, 6.3.3 |
| 4 | DAST | OWASP ZAP | 0 High or Critical findings | Block production | CISO and risk committee | 6.4.1, 6.4.2 |
| 5 | Licence compliance | FOSSA | No GPL, AGPL or SSPL dependencies | Block build | Legal team | Not a PCI control (legal and policy) |
| 6 | IaC scan | Checkov | No privileged containers, resource limits set, no public storage | Block deploy | Platform security lead, independent of the author | 6.5.1 |
| 7 | Admission policy | OPA (or Gatekeeper) | All cluster policies pass | Block deploy | Dual approval (security plus platform) | 6.5.1, 6.5.3 |
| 8 | Image signing and SBOM | Cosign, Syft | Image signed by the trusted key; SBOM attached | Block deploy | CISO | 6.3.2, 6.5.1 |
| 9 | Separation of duties | GitHub branch protection, CODEOWNERS, Environment required reviewers | PR approved by a non-author; production deploy approved by a second person who did not write or approve the change | Block deploy | **No exception possible** | 6.5.1, 6.5.4 |

---

## 2. RBI Mapping

Fill in the exact clause numbers after checking each document.

| Gate(s) | RBI document | Topic | Clause (verify) |
|---|---|---|---|
| 1, 2, 3, 4 | Master Direction on IT Governance, Risk, Controls and Assurance Practices | Secure development, vulnerability management, testing | |
| 1, 2, 3, 4 | Cyber Security Framework in Banks | Vulnerability assessment and secure configuration | |
| 2, 5, 8 | Master Direction on Outsourcing of IT Services | Third-party and open-source component risk | |
| 6, 7, 9 | Master Direction on IT Governance, Risk, Controls and Assurance Practices | Change management, access control, separation of duties | |
| All (audit log) | Master Direction on IT Governance, Risk, Controls and Assurance Practices | Audit trail, log retention | |
| Audit log storage | RBI directive on storage of payment system data | Data stored in India | |

---

## 3. Audit Trail and Evidence

Every gate execution writes a JSON record.

- **Storage:** an S3 bucket with Object Lock in compliance mode, in an Indian region (for example `ap-south-1`), so records cannot be altered or deleted during retention.
- **Retention:** 7 years. This is a NovaPay policy choice. PCI-DSS 10.5.1 requires at least 12 months, with the last 3 months immediately available.
- **Tamper evidence:** each record carries a SHA-256 hash, and each record includes the previous record's hash.

```json
{
  "timestamp": "2026-10-15T14:30:00Z",
  "pipeline_run_id": "run-8942",
  "git_commit_sha": "a1b2c3d4",
  "gate_name": "SAST",
  "tool": "SonarQube",
  "tool_version": "10.x",
  "status": "PASSED",
  "findings": { "critical": 0, "high": 1, "medium": 12 },
  "approved_by": "automated",
  "exception_id": null,
  "regulatory_mapping": ["PCI-DSS 6.2"],
  "previous_record_sha256": "<hash of the previous record>",
  "log_sha256": "<hash of this record>"
}
```

---

## 4. Exception Workflow (Separation of Duties)

A team cannot bypass a gate itself.

1. The developer files an exception request in ServiceNow, naming the gate, commit SHA, risk and remediation plan.
2. An approver who is independent of the author (CISO, risk committee or Legal, per the gate table) reviews it.
3. If approved, ServiceNow issues an exception token that is:
   - scoped to one gate and one commit SHA,
   - time-limited (maximum 7 days),
   - single-use.
4. The pipeline validates the token through the ServiceNow API before continuing.
5. The exception, approver ID and timestamp are written to the audit trail permanently.

**Controls that stop circumvention**
- The workflow files and `pipeline/policies/` are protected by CODEOWNERS and branch protection. A developer cannot edit the pipeline to skip a gate without an independent review.
- Gate 9 has no exception path.
- Quarterly review: the security team reviews all exceptions that were granted.

---

## 5. Related Files

| Item | Location |
|---|---|
| OPA admission policy | `pipeline/policies/no-privileged-containers.rego` |
| Policy unit tests | `pipeline/policies/no-privileged-containers_test.rego` |
| Gate flow diagram | `docs/03-compliance-gates/gate-orchestration-diagram.md` |

---

## AI Attribution

- **Tool used:** Claude
- **Human review:** Customized for the NovaPay banking context.
