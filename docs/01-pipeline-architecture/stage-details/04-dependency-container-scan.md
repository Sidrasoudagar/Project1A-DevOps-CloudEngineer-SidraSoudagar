# Stage 4: Dependency & Container Scan

## Overview
Checks third-party libraries, base images and vendor-delivered components for known vulnerabilities and end-of-life status, and enforces the patch timelines.

## Tool & Version
- **Primary Tool:** Trivy (dependencies, container images, IaC misconfiguration) with OWASP Dependency-Track for continuous SBOM monitoring. Versions pinned and recorded in the tool register.
- **Alternative:** Grype with Snyk.

## Inputs
- CycloneDX SBOM and signed artefact from Stage 2
- Container image digest and base-image lineage
- Vulnerability feeds (NVD and vendor advisories) with update timestamp
- End-of-life data for runtimes, frameworks and base images
- Vendor attestation package (for vendor-delivered software)
- Waiver register

## Configuration Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Feed freshness | Vulnerability database no older than 24 hours | Stale feeds hide new issues (PCI 6.3.1) |
| Risk ranking | Critical, High, Medium, Low using CVSS plus exploit-availability flag | Recognised, documented ranking (PCI 6.3.1; RBI 26) |
| Patch SLA | Critical and High: fix within 30 days of patch release at most; NovaPay target Critical 7 days, High 14 days | PCI 6.3.3 sets one month as the ceiling |
| End-of-life check | Block runtimes, frameworks and base images past vendor end-of-support | RBI 9(d)-(e) |
| Image policy | Approved registry, non-root user, no `latest` tags, pinned by digest | Controlled supply chain |
| Continuous monitoring | Dependency-Track re-evaluates every deployed SBOM when new CVEs appear | Vulnerabilities found after release are still caught |
| Vendor intake | Vendor attestation plus SCA, SAST and malware scan required per version | RBI 12(f)-(h) |
| IaC checks | Misconfiguration scan for Kubernetes and cloud manifests | Prevents insecure deployment definitions |

## Quality Gates
| Gate | Threshold | Action on Failure |
|------|-----------|-------------------|
| G4 SCA, SBOM and EOL | 0 unwaived Critical or High with a fix available; no EOL components; SBOM present | Fail build |
| Patch SLA breach | Any Critical or High finding older than its SLA | Block promotion for that service |
| G6 Vendor intake | Attestation present for this exact version, with clean scans | Block promotion |
| Feed freshness | Vulnerability DB updated within 24 hours | Fail scan; do not pass on stale data |
| Image policy | Registry, tag and user rules satisfied | Fail build |

## Failure Mode & Remediation
- **Failure:** Critical or High CVE in a dependency or base image with a fix available.
- **Remediation:** Upgrade through an auto-generated PR. If no fix exists, document compensating controls and request a time-limited waiver.
- **Failure:** Component past end-of-support, or vendor attestation missing or out of date.
- **Remediation:** Plan migration to a supported version; request a fresh attestation from the vendor before the release date.
- **Exception Process:** Waiver for a Critical or High finding with no available fix needs the service owner, a CISO delegate and documented compensating controls, with a maximum of 30 days and a renewal review. EOL waivers need Steering Committee approval and a dated migration plan, maximum 90 days.

## SLA Target
- **Expected:** 5 minutes
- **Maximum:** 10 minutes

## Output Artefacts
- Vulnerability report with risk ranking and fix availability
- Updated SBOM record in Dependency-Track
- EOL status report
- Vendor attestation record and scan results
- Waiver references and SLA-ageing data

## Regulatory Mapping
| Framework | Requirement | How This Stage Satisfies It |
|-----------|-------------|----------------------------|
| RBI | 9(d)-(e) Unsupported hardware and software | EOL and end-of-support gate on runtimes, libraries and images |
| RBI | 12(f)-(h) Vendor assurance and product approval | Intake gate with attestation and independent scans per version |
| RBI | 26 Vulnerability assessment and time-bound remediation | Ranked findings with enforced fix timelines |
| PCI-DSS v4.0 | 6.3.1 Identify and rank vulnerabilities | Recognised feeds plus defined risk-ranking model |
| PCI-DSS v4.0 | 6.3.2 Software component inventory | SBOM maintained for every build and monitored continuously |
| PCI-DSS v4.0 | 6.3.3 Patch within required timeframes | Patch SLA enforced as a gate, with one month as the outer limit |

## AI Attribution
- **Tool:** Claude (Anthropic)
- **Date:** 2026-10-11
- **Human review:** Drafted for NovaPay; pending human review. Reviewer name and date to be recorded here.
