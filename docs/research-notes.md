# Research Notes — RBI Master Direction & PCI-DSS v4.0

**Author:** Sidra Soudagar
**Project:** NovaPay Digital Bank — Zero-Downtime CI/CD Pipeline
**Date:** [Today's date]

---

I'll check the Master Direction's structure first, since the section numbering matters for the mapping.# RBI IT Governance Master Direction and PCI-DSS v4.x: CI/CD Compliance Summary

## Before you rely on this

- **Sections 4-7 of the RBI Direction are governance provisions only.** I checked the published text (RBI/2023-24/107, effective 1 April 2024). Paras 4-7 cover the governance framework, the Board, the IT Strategy Committee (ITSC) and the IT Steering Committee. There are no numbered sub-sections like 4.1, because the Direction uses (a), (b), (c) lettering. Change management, audit trails, access control and VA/PT sit in **paras 9-26 and 30**, so I've included those too.
- **PCI-DSS:** v4.0 was retired on 31 Dec 2024 and v4.0.1 is the current version. The requirement numbers you listed are unchanged, and the "future-dated" v4.0 items became mandatory on 31 Mar 2025. I summarised the PCI requirements from my own knowledge of the standard, not from the PCI SSC document, so check the wording against the official text.
- The pipeline mappings are my interpretation, not regulator-endorsed. Have your QSA and compliance team confirm them.

---

## 1. RBI Master Direction: key sections and pipeline control mapping

**Applicability:** commercial banks (including SFBs and payments banks), NBFCs in the Top, Upper and Middle layers, CICs, and AIFIs. Local Area Banks and NBFC-CICs are excluded. Foreign bank branches follow "comply or explain".

### 1a. Governance paras (4-8)

| Para | What it requires | Pipeline control mapping |
|---|---|---|
| **4** IT Governance Framework | A framework covering strategic alignment, risk, resources, performance and BC/DR. It must define roles, authority and oversight, and bring IT risk into enterprise risk policy. | Keep a **control catalogue** (controls-as-code) where each pipeline gate has a named owner, a risk reference and a policy reference. |
| **5** Board | The Board approves IT, infosec, cyber and BCP strategies and policies, and reviews them at least annually. | Store policies as versioned, signed artefacts. Gates cite the **policy version ID**, and an annual-review-overdue check flags stale policies. |
| **6** ITSC | Board-level committee of at least 3 directors, chaired by an independent director with IT expertise. It meets quarterly and oversees IT risk processes and the adequacy of security budgets. | Produce an automated **quarterly pack** (gate pass/fail rates, exceptions, vulnerability ageing, failed-change rate) for ITSC review. |
| **7** Senior Management and IT Steering Committee | Senior management executes the strategy and builds a culture of IT risk awareness and cyber hygiene. The Steering Committee, with IT and business members, meets quarterly. | Exception and waiver workflow routes to the Steering Committee or the Information Security Committee. Each waiver has an expiry date and an approver ID. |
| **8** Head of IT | Acts as first line of defence, responsible for assessing and managing IT controls and risk. | The Head of IT is the named **first-line control owner** in the catalogue and attests control effectiveness periodically. |

### 1b. Operational paras that actually govern the pipeline

| Para | Requirement (paraphrased) | Pipeline control mapping |
|---|---|---|
| **9(b)** | IT service management must ensure effective segregation of duties. | Role separation in SCM, CI and CD (see Section 3). |
| **9(d)-(e)** | Avoid unsupported hardware and software, and track end-of-support dates. | EOL/EOS gate on base images, runtimes and libraries. |
| **12(f)-(g)** | Obtain source code (or escrow) for critical applications. Get vendor confirmation that the app is free of known vulnerabilities, malware and covert channels, renewed on material changes. | Vendor-delivery intake pipeline with SCA, SAST and malware scanning plus an attestation artefact. |
| **12(h)** | New IT products need product approval and QA. | Release gate requiring an approved product ID and QA sign-off record. |
| **13(a)-(d)** | Documented change and patch policy. It requires a business-impact assessment, secure and timely implementation with approvals, justification and documentation, and a recovery mechanism for failed changes. | Change-record linkage, approval gate, automated rollback and post-deploy verification. |
| **14** | Data migrations need sign-offs at each stage and audit trails. | Migration jobs run through the pipeline with approver sign-off and a logged reconciliation report. |
| **15(a)-(c)** | Applications touching critical data must log and provide audit trails detailed enough for audit, forensics and non-repudiation. Logs must be monitored regularly. | See Section 4. |
| **17** | No manual modification of critical data between processes. Transfers should be automated with checks and audit trails. | Ban ad-hoc production data edits. Operational scripts run only via the pipeline with approvals and logs. |
| **19(a)-(c)** | Need-based access under standards approved by the ITSC. Privileged users are supervised, logged and reviewed, with MFA for privileged users of critical systems. | MFA on pipeline admin and deploy roles, just-in-time elevation, and periodic access recertification. |
| **23(b)** | Identify and eliminate or manage role conflicts and accountability gaps, including for third-party staff. | An automated SoD-conflict check on pipeline role assignments. |
| **24(c)** | The CISO has no direct reporting line to the Head of IT and no business targets. | The security gate is owned by the CISO's office, and the Head of IT cannot waive it unilaterally. |
| **26** | VA at least every 6 months and PT at least every 12 months for critical and customer-facing DMZ systems, plus VA/PT across the lifecycle (pre- and post-implementation, after major changes). Testers must be independent. Vulnerabilities must be fixed in a time-bound manner, with a documented approach and scoring such as CVSS. | Scan gates (see Section 5), plus a scheduler and tracker for PT. |
| **30** | IS Audit is overseen by the Audit Committee, with risk-based planning. Continuous auditing is encouraged for critical systems. | A read-only auditor view of the evidence store, with continuous control monitoring. |

---

## 2. PCI-DSS v4.x: requirements and CI/CD mapping

| Req | Summary | CI/CD implementation |
|---|---|---|
| **6.2.1** | Bespoke and custom software is developed securely, with security built into the SDLC. | Documented secure SDLC, with templates enforcing mandatory pipeline stages. |
| **6.2.2** | Developers receive secure-coding training at least every 12 months. | Pipeline checks that the committer or approver has a current training record. This is a policy gate, so keep a manual fallback. |
| **6.2.3 / 6.2.3.1** | Code is reviewed before release. Manual reviews must be done by someone other than the author, who is knowledgeable, and management must approve the results before release. | Branch protection that requires a CODEOWNERS review. Block self-approval. Add an automated SAST gate for coverage. |
| **6.2.4** | Techniques are in place against common attacks (injection, access control flaws, crypto misuse, logic abuse and others). | SAST/DAST rule sets mapped to OWASP-style classes. Fail on high-severity findings. |
| **6.3.1** | Vulnerabilities are identified from recognised sources and risk-ranked. | SCA and image scans with CVE/CVSS feeds and a defined risk-ranking policy. |
| **6.3.2** | Maintain an inventory of bespoke code and third-party components (SBOM). | Generate and sign an SBOM at build and store it as a release artefact. |
| **6.3.3** | Apply applicable security patches. Critical and high patches go in within one month of release. | Dependency ageing gate and an auto-PR for updates, with SLA clocks per finding. |
| **6.4.1 / 6.4.2** | Public-facing web apps are protected, with an automated solution (WAF) that continually detects and prevents web attacks. | WAF-in-front check in release criteria, and DAST on staging. |
| **6.4.3** | Payment-page scripts are authorised, integrity-checked and inventoried with justification. | SRI hashes, a script allowlist and a CSP review gate for payment pages. |
| **6.5.1** | Production changes follow procedure: reason, security impact, authorised approval, testing, and a way back to a secure state. | Change ticket required, approval gate, automated tests and a rollback plan. |
| **6.5.2** | After a significant change, confirm applicable PCI requirements are in place on changed systems and update documentation. | A post-change checklist job that triggers scans and updates the evidence record. |
| **6.5.3** | Pre-production is separated from production, with access controls enforcing the separation. | Separate accounts, networks and credentials per environment, with no shared secrets. |
| **6.5.4** | Roles are separated between production and pre-production so only reviewed and approved changes are deployed. | Developers cannot deploy to production. Only a release role or pipeline identity can. |
| **6.5.5** | Live PANs are not used in pre-production unless it is protected as CDE. | DLP and PAN-pattern scan on test data and fixtures. |
| **6.5.6** | Test data and test accounts are removed before go-live. | Release gate scanning for test accounts, default credentials and fixtures. |
| **10.2** | Audit logs are enabled and capture the defined events (see Section 4). | Central, tamper-evident pipeline logging. |
| **11.3.1** | Internal scans at least quarterly, using authenticated scanning. Scans are repeated after significant changes. High and critical findings are fixed and re-scanned. Scanners must be qualified and organisationally independent. | Scheduled authenticated scans plus a post-deploy scan trigger. Block on unresolved critical findings. |
| **11.3.2** | External scans at least quarterly by an ASV, plus after significant changes. | ASV scan scheduling and tracking. Block release if a scan after a significant change has failed. |

---

## 3. Segregation of duties (SoD)

| Source | Requirement | Control |
|---|---|---|
| RBI 9(b) | SoD within IT service management | Role model across SCM, CI and CD |
| RBI 23(b) | Identify and eliminate role conflicts, including third parties | Automated conflict detection on role assignment |
| RBI 24(c) | CISO independent of Head of IT | CISO-owned security gate, with no unilateral waiver by IT |
| RBI 19(b) | Privileged activity is supervised, logged and reviewed | Just-in-time admin access with session logging |
| RBI 26(c) | Independent VA/PT testers | A separate identity and team for testing |
| RBI 30(d) | Separate IS Audit function | Read-only auditor access to evidence |
| PCI 6.2.3.1 | Reviewer is not the author | Self-approval blocked |
| PCI 6.5.3 / 6.5.4 | Environment separation and role separation | Environment-scoped identities, no developer production deploys |
| PCI 11.3.1 | Scanner has organisational independence | Scan results are written by a security-owned service account |

**Suggested role matrix** (✔ = permitted, ✘ = prohibited):

| Action | Developer | Reviewer | Release approver | Deployer / pipeline | Security | Auditor |
|---|---|---|---|---|---|---|
| Commit code | ✔ | ✘ | ✘ | ✘ | ✘ | ✘ |
| Approve own change | ✘ | ✘ | ✘ | ✘ | ✘ | ✘ |
| Approve peer change | ✘ | ✔ | ✘ | ✘ | ✘ | ✘ |
| Approve release | ✘ | ✘ | ✔ | ✘ | ✘ | ✘ |
| Deploy to production | ✘ | ✘ | ✘ | ✔ | ✘ | ✘ |
| Modify gate or policy | ✘ | ✘ | ✘ | ✘ | ✔ (with change control) | ✘ |
| Read all evidence | ✘ | ✘ | ✘ | ✘ | ✔ | ✔ |

Neither framework prescribes this exact matrix. It is one way to satisfy both.

---

## 4. Audit trail requirements for banking CI/CD pipelines

**RBI para 15** requires audit trails that are:
- detailed enough for audit and forensics,
- usable as evidence in disputes (non-repudiation), and
- regularly monitored to detect unauthorised activity.

**PCI 10.2.1** lists the events to capture, and **10.2.2** lists the fields each record must carry. Pipeline systems that can change the CDE are typically treated as in scope, so confirm scoping with your QSA.

| Pipeline event | Basis | Minimum fields |
|---|---|---|
| Administrative actions on CI/CD, SCM and artefact registry | PCI 10.2.1.2 | Actor ID, action, target, timestamp, outcome, source |
| Failed logins and denied access | PCI 10.2.1.4 | Actor ID, source, timestamp |
| Role, credential and permission changes | PCI 10.2.1.5; RBI 19 | Who changed what, old and new value, approver |
| Access to the audit logs themselves | PCI 10.2.1.3 | Actor ID, timestamp |
| Log stop, start or pause | PCI 10.2.1.6 | Component, actor, timestamp |
| Creation or deletion of system-level objects (pipelines, runners, environments, secrets) | PCI 10.2.1.7 | Object, actor, timestamp |
| Access to cardholder data (e.g. through pipeline jobs) | PCI 10.2.1.1 | Actor ID, data reference, timestamp |
| Change lifecycle: request, review, approval, build, test, deploy, rollback | RBI 13, 15; PCI 6.5.1 | Change ID, commit SHA, approver IDs, artefact digest, gate results, deploy target |
| Waivers and exceptions | RBI 7, 24 | Approver, scope, expiry, justification |

**Fields on every record (PCI 10.2.2):** user ID, event type, date and time, success or failure, origin, and the affected data, component or resource.

**Adjacent requirements:**
- **PCI 10.3 and 10.5.** Protect logs from modification and retain them for 12 months, with 3 months immediately available. The RBI Direction sets no retention period, so follow other applicable law and your own policy.
- **RBI 15(c).** Alert on anomalies such as deploys outside change windows, approvals by unusual identities, or gate-config edits.
- **Implementation notes.** Use an append-only or write-once store, hash-chain or sign records, synchronise time sources, and keep the logs outside the control of the people the pipeline logs.

---

## 5. Translating requirements into automated compliance gates

| Gate | Stage | Source | Automated check | On failure | Evidence emitted |
|---|---|---|---|---|---|
| **G1 Change linkage** | PR / merge | RBI 13(c); PCI 6.5.1 | Commit or PR references an approved, justified change record | Block merge | Change ID, approver |
| **G2 Independent review** | PR | PCI 6.2.3.1; RBI 9(b), 23(b) | At least one approver who is not the author; CODEOWNERS satisfied | Block merge | Reviewer IDs |
| **G3 SAST** | Build | PCI 6.2.3, 6.2.4 | No unwaived high or critical findings | Fail build | Report, rule-set version |
| **G4 SCA, SBOM and EOL** | Build | PCI 6.3.1-6.3.3; RBI 9(d), 12(g) | SBOM generated. No critical or high CVEs past SLA, and no EOL components | Fail build | Signed SBOM, findings |
| **G5 Secrets and test-data scan** | Build | PCI 6.5.5, 6.5.6 | No live PAN patterns, test accounts or default credentials | Fail build | Scan result |
| **G6 Vendor intake** | Intake | RBI 12(f)-(h) | Vendor attestation present for this version, with malware and SCA scans | Block promotion | Attestation, scan report |
| **G7 DAST and WAF** | Staging | PCI 6.4.1, 6.4.2; RBI 26(a) | DAST passes. WAF is in front of public-facing apps | Block release | DAST report |
| **G8 Payment-page scripts** | Staging | PCI 6.4.3 | Script inventory matches the allowlist, with SRI and CSP present | Block release | Script inventory |
| **G9 Release approval and SoD** | Pre-prod to prod | PCI 6.5.4; RBI 9(b), 24(c) | Release approver differs from the author and deployer. Security gate green | Block deploy | Approval record |
| **G10 Environment isolation** | Deploy | PCI 6.5.3 | Deploy identity is scoped to the target environment, with no cross-environment secrets | Block deploy | Identity, target |
| **G11 Deploy and rollback** | Deploy | RBI 13(d); PCI 6.5.1 | Health checks run, and rollback is automated on failure | Auto-rollback | Deploy log |
| **G12 Post-change verification** | Post-deploy | RBI 26(a); PCI 6.5.2, 11.3.1.3, 11.3.2.1 | Authenticated scan triggered after significant changes. Checklist confirms controls are intact | Raise incident or block next release | Scan result |
| **G13 Scheduled VA/PT** | Scheduled | RBI 26(a)-(f); PCI 11.3.1, 11.3.2 | VA at least every 6 months and PT at least every 12 months for critical systems, internal scans quarterly, ASV scans quarterly. Overdue items block releases to that system | Escalate or block | Scan reports, tester identity |
| **G14 Log integrity** | Continuous | PCI 10.2, 10.3; RBI 15(c) | Logging is active, records are signed, and there are no gaps | Alert, freeze deployments | Integrity attestation |
| **G15 Waiver control** | Any | RBI 7, 24 | Waivers have an approver, scope and expiry, and are CISO-approved for security gates | Waiver rejected | Waiver record |

**Requirements that automation can only support, not satisfy:**
- Board and ITSC approvals and reviews (RBI 5, 6)
- Developer training (PCI 6.2.2), where the pipeline can only check records
- Independent penetration testing (RBI 26(c)), where the pipeline schedules and tracks it
- ASV scans, which only an approved vendor can perform
- DR drills (RBI 29)

For these, have the pipeline verify that a **current, approved attestation exists** rather than trying to perform the activity itself.

**Related requirements to consider:** the RBI IT Outsourcing Directions (2023) for third-party-run pipelines or SaaS CI, and PCI Req 7 and 8 (access control and authentication) as the basis for the SoD and MFA controls above.

**Sources:** RBI Master Direction on IT Governance, Risk, Controls and Assurance Practices (RBI/2023-24/107, 7 Nov 2023), at rbi.org.in. PCI SSC, PCI DSS v4.0.1.

---

## AI Attribution

- **Tool used:** [Claude]
- **Prompt:** "Summarize RBI Master Direction on IT Governance sections 4-7 and PCI-DSS v4.0 requirements 6.2-6.5, 10.2, 11.3..."
- **Date generated:** [Today's date]
- **Human review:** Content reviewed and customized for NovaPay banking context.
