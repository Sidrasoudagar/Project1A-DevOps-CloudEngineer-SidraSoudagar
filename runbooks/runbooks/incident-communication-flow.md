# Incident Communication Flow

```mermaid
flowchart TD
    A[Alert Fires in PagerDuty] --> B[On-Call Acknowledges]
    B --> C{Severity?}
    C -->|SEV-1| D[Page CTO, CISO, IC]
    C -->|SEV-2| E[Page SRE Lead, Eng Manager]
    C -->|SEV-3/4| F[SRE Handles Solo]
    
    D --> G[Update Slack #incident-response]
    G --> H[Update External Status Page]
    
    H --> I[Investigate & Mitigate]
    I --> J{Resolved?}
    J -->|No| I
    J -->|Yes| K[Update Status Page: Resolved]
    K --> L[Schedule Post-Mortem]
