# Stage 6: Dynamic Analysis (DAST)

## Overview
Tests the running application in staging from the outside, authenticated and unauthenticated, and verifies web protections and payment-page script controls.

## Tool & Version
- **Primary Tool:** OWASP ZAP using the automation framework, with a NovaPay script to verify CSP, SRI and the payment-page script allowlist. Versions pinned and recorded in the tool register.
- **Alternative:** Burp Suite Enterprise.

## Inputs
- Deployed candidate build in the staging environment
- OpenAPI/GraphQL specifications and crawl seeds
- Test credentials for each role (authenticated scanning)
- Payment-page script inventory and allowlist
- WAF configuration state for the target
- Waiver register

## Configuration Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Scan modes | Quick baseline in pipeline; full authenticated active scan nightly and before major releases | Balances speed and depth |
| Authentication | Scans run per role (customer, merchant, admin) | Covers access-control flaws (PCI 6.2.4) |
| Target scope | Public-facing apps and APIs only, in staging | PCI 6.4.1 |
| WAF verification | Confirm WAF is active in front of the target and blocking mode is on | PCI 6.4.2 |
| Payment-page scripts | Every script loaded on payment pages is on the allowlist, has an SRI hash and a written justification | PCI 6.4.3 |
| Security headers | CSP, HSTS, frame and content-type protections validated | Reduces client-side attack surface |
| Rate and safety limits | Scan throttled; synthetic data only; no production targets | Protects environments and PCI 6.5.5 |
| Result ownership | Findings published by a security-owned account | Independence (RBI 26(c) principle) |

## Quality Gates
| Gate | Threshold | Action on Failure |
|------|-----------|-------------------|
| G7 DAST and WAF | 0 unwaived High or Critical findings; WAF active | Block release |
| G8 Payment-page scripts | Script inventory equals allowlist; SRI and CSP present | Block release |
| Authenticated coverage | All defined roles scanned successfully | Fail; unauthenticated-only result is not accepted |
| Scan completion | Scan finished within time limit and covered the defined scope | Fail pipeline |

## Failure Mode & Remediation
- **Failure:** High or Critical finding on a public-facing endpoint.
- **Remediation:** Fix the application defect and redeploy to staging. A WAF rule is a compensating measure, not a fix.
- **Failure:** Unrecognised or unapproved script on a payment page.
- **Remediation:** Remove it, or add it to the inventory with justification and SRI hash through a reviewed change. Investigate how it was introduced.
- **Exception Process:** Waivers for High findings need the service owner and a CISO delegate with a maximum of 14 days and documented WAF compensating controls. Payment-page script findings and WAF-inactive findings cannot be waived.

## SLA Target
- **Expected:** 20 minutes (baseline scan)
- **Maximum:** 45 minutes

## Output Artefacts
- DAST report (findings, role coverage, scan configuration)
- Payment-page script inventory and verification result
- WAF state evidence
- Waiver references applied

## Regulatory Mapping
| Framework | Requirement | How This Stage Satisfies It |
|-----------|-------------|----------------------------|
| RBI | 26 Vulnerability assessment and penetration testing | Lifecycle vulnerability assessment on customer-facing systems before release; supports, but does not replace, independent annual PT |
| RBI | 24(c) CISO independence | Security owns scan configuration and results |
| PCI-DSS v4.0 | 6.4.1, 6.4.2 Protect public-facing web applications | DAST plus verification that an automated WAF is in front of the application |
| PCI-DSS v4.0 | 6.4.3 Payment-page scripts | Inventory, authorisation and integrity checks enforced |
| PCI-DSS v4.0 | 6.2.4 Methods against common attacks | Dynamic testing of injection and access-control flaws |
| PCI-DSS v4.0 | 11.3.1 Authenticated internal vulnerability scanning | Authenticated scan evidence supports quarterly scanning but does not replace the scheduled scans |

## AI Attribution
- **Tool:** Claude (Anthropic)
- **Date:** 2026-10-11
- **Human review:** Drafted for NovaPay; pending human review. Reviewer name and date to be recorded here.
