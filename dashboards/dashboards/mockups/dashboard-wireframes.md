# Dashboard Wireframes

## 1. Engineering Dashboard (Live Ops)
```mermaid
block-beta
  columns 2
  block:header:2
    title["🟢 NovaPay Live System Health (Refreshes every 10s)"]
  end
  block:error
    err_title["HTTP 5xx Error Rate"]
    err_val["0.02% ✅"]
  end
  block:latency
    lat_title["p99 Latency"]
    lat_val["145ms ✅"]
  end
  block:deploys:2
    dep_title["Active Deployments"]
    dep_val["Canary: payment-service v2.1 (10% traffic)"]
  end
