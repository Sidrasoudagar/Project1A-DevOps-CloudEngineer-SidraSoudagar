# Gate Orchestration Flow

Gates follow the eight pipeline stages. Any failure blocks the pipeline. An independently approved, single-use exception token is the only way past a failed gate (except Gate 9).

```mermaid
flowchart TD
    A["1. Source: signed commit, PR approved by non-author (Gate 9)"] --> B["2. Build and 3. Unit tests"]
    B --> C{"4. SAST, dependency, secrets, licence (Gates 1, 2, 5)"}
    C -->|Fail| X["Block: exception token needed"]
    C -->|Pass| D{"5. Container image scan (Gate 3)"}
    D -->|Fail| X
    D -->|Pass| E{"5. Sign image and attach SBOM (Gate 8)"}
    E -->|Fail| X
    E -->|Pass| F["6. Deploy to staging"]
    F --> G{"DAST and contract tests (Gate 4)"}
    G -->|Fail| X
    G -->|Pass| H{"IaC scan and admission policy (Gates 6, 7)"}
    H -->|Fail| X
    H -->|Pass| I{"7. Production approval by a second person (Gate 9)"}
    I -->|Rejected| Z["Stop: no exception possible"]
    I -->|Approved| J["7. Deploy to production: blue-green or canary"]
    J --> K["8. Post-deploy checks and automatic rollback"]
    X --> L["Independent approver reviews in ServiceNow"]
    L -->|Approved: scoped, time-limited token| M["Continue and log exception in audit trail"]
    L -->|Rejected| Z
```

Every gate result and every exception is written to the audit log (see `compliance-gates.md`, section 3).
