# Deployment Topology Diagram

## 1. Blue-Green (standard releases)

```mermaid
flowchart TD
    User([Users]) --> DNS[DNS / Load Balancer]
    DNS --> Istio{Istio VirtualService}

    subgraph Prod["Production Environment"]
        Istio -->|"100% before switch"| Blue["Blue Environment<br/>Stable v1.0"]
        Istio -.->|"100% after switch"| Green["Green Environment<br/>New v1.1"]
    end

    Blue --> Redis[(Redis Session Store)]
    Green --> Redis
    Blue --> DB[("Shared PostgreSQL<br/>Expand-Contract")]
    Green --> DB
```

Green is verified with smoke tests, then Istio switches all traffic. If Green fails during the 15-minute monitoring window, traffic is routed back to Blue within 30 seconds.

## 2. Canary (high-risk releases)

```mermaid
flowchart TD
    User([Users]) --> DNS[DNS / Load Balancer]
    DNS --> Istio{Istio VirtualService}

    subgraph Prod["Production Environment"]
        Istio -->|"90 to 99%"| Stable["Stable v1.0"]
        Istio -->|"1 to 10%"| Canary["Canary v1.1"]
    end

    Canary --> Analysis["Argo Rollouts AnalysisTemplate<br/>Prometheus metrics"]
    Analysis -->|"Pass: promote"| Istio
    Analysis -->|"Fail: abort"| Istio

    Stable --> DB[("Shared PostgreSQL<br/>Expand-Contract")]
    Canary --> DB
```

Traffic increases in phases (1 to 2%, 5 to 10%, 25 to 50%, 100%). If the canary fails the automated analysis or a Category A trigger fires, traffic returns to the stable version.
