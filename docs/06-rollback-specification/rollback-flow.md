# Rollback Flow

```mermaid
flowchart TD
    A[Deploy Canary / Green] --> B[Monitor Metrics]
    B --> C{Critical Alert?}
    C -->|Category A Trigger| D[Auto-Route Traffic to Blue]
    D --> E[Run Smoke Tests]
    E --> F[Notify Engineering Team]
    F --> G[Create Jira Incident]
    
    C -->|Category B Trigger| H[Page On-Call Engineer]
    H --> I{Respond in 10 min?}
    I -->|No| D
    I -->|Yes| J[Engineer Investigates]
    
    C -->|Category C Trigger| K[Manual Review]
    K --> L{Decision}
    L -->|Rollback| D
    L -->|Fix Forward| M[Deploy Hotfix]
