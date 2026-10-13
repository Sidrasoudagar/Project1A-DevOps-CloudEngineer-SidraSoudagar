# Stage 5: Integration & Contract Testing

## Overview
Verifies in an isolated pre-production environment that services behave correctly together and keep their API contracts, using only synthetic data.

## Tool & Version
- **Primary Tool:** Pact (consumer-driven contract testing) with Testcontainers-based integration suites. Versions pinned and recorded in the tool register.
- **Alternative:** Postman/Newman collections or Spring Cloud Contract.

## Inputs
- Signed artefact and SBOM from Stage 2, passed by Stages 3 and 4
- Pact contracts from the broker (consumer and provider)
- Synthetic, tokenised test data set
- Pre-production environment definition (isolated network, separate credentials)
- QA test plan and approved acceptance criteria

## Configuration Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Environment | Dedicated pre-production, separate accounts, network and secrets from production | PCI 6.5.3 |
| Test data | Synthetic or tokenised only; automated PAN-pattern check before each run | PCI 6.5.5 |
| Contract verification | All provider contracts verified against the candidate build; "can-i-deploy" check required | Prevents breaking dependent services |
| Payment-flow coverage | Authorisation, capture, refund, reversal, timeout and idempotency scenarios | Business-logic abuse and data integrity (PCI 6.2.4; RBI 17) |
| Access-control tests | Negative tests for role and tenant boundaries | PCI 6.2.4 access control attacks |
| Test accounts | Created per run and destroyed afterwards; none promoted to production | PCI 6.5.6 |
| Test evidence | Results stored with commit SHA and environment identity | RBI 13; audit evidence |
| Flaky-test policy | Retry once; two inconsistent results quarantine the test and raise a ticket | Keeps the gate trustworthy |

## Quality Gates
| Gate | Threshold | Action on Failure |
|------|-----------|-------------------|
| Contract verification | 100% of contracts verified; can-i-deploy passes | Fail pipeline |
| Integration suite | 100% of critical payment-flow tests pass | Fail pipeline |
| Test-data check | Zero live PAN patterns in data and logs | Fail pipeline; raise incident |
| Environment isolation | Test identity scoped to pre-production only | Fail pipeline |
| QA sign-off | Required for product changes under RBI 12(h) | Block promotion |

## Failure Mode & Remediation
- **Failure:** Contract break between consumer and provider.
- **Remediation:** Fix the provider or agree a versioned contract change with the consumer team. Do not override can-i-deploy.
- **Failure:** Live PAN pattern or real customer data detected in the test environment.
- **Remediation:** Stop the run, quarantine and purge the data, find the source of the leak, and treat it as a security incident.
- **Exception Process:** Skipping a non-critical test needs the service owner and QA lead, with a maximum of 7 days. Contract and payment-flow tests cannot be waived. Environment-isolation and live-PAN failures cannot be waived.

## SLA Target
- **Expected:** 15 minutes
- **Maximum:** 30 minutes

## Output Artefacts
- Integration and contract test reports
- can-i-deploy result
- Test-data verification result
- QA sign-off record where applicable
- Environment and test-run audit events

## Regulatory Mapping
| Framework | Requirement | How This Stage Satisfies It |
|-----------|-------------|----------------------------|
| RBI | 12(h) Product approval and QA | QA sign-off required before promotion |
| RBI | 13 Change management | Testing of changes before implementation with documented results |
| RBI | 17 Controls on critical data flows | Tests confirm data integrity across services without manual intervention |
| PCI-DSS v4.0 | 6.5.1 Testing before change | Automated verification that changes do not adversely affect security |
| PCI-DSS v4.0 | 6.5.3 Pre-production separated from production | Isolated environment with separate identities |
| PCI-DSS v4.0 | 6.5.5, 6.5.6 No live PAN and no test accounts in production | Synthetic data enforced; test accounts destroyed after the run |
| PCI-DSS v4.0 | 6.2.4 Methods against common attacks | Negative and access-control tests for payment flows |

## AI Attribution
- **Tool:** Claude (Anthropic)
- **Date:** 2026-10-11
- **Human review:** Drafted for NovaPay; pending human review. Reviewer name and date to be recorded here.
