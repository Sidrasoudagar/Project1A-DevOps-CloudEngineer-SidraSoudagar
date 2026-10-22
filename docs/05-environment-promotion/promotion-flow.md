# Promotion Flow Diagram

```mermaid
flowchart TD
    A[Developer Commits Code] --> B[Dev Environment]
    B -->|Automated Tests Pass| C[Staging Environment]
    C -->|DAST Pass, Perf Pass, Tech Lead Approves| D[Pre-Prod Environment]
    D -->|UAT Sign-off, Dual Approval RM + SRE| E[Production Environment]
    
    subgraph "Data Masking Rules"
        C -.->|Anonymized Data| C1[Data]
        D -.->|Masked Prod Data| D1[Data]
    end
