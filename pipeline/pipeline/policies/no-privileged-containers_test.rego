package kubernetes.admission

import rego.v1

good_pod := {"request": {
  "kind": {"kind": "Pod"},
  "object": {"spec": {"containers": [
    {"name": "app", "resources": {"limits": {"memory": "256Mi"}}}
  ]}}
}}

privileged_pod := {"request": {
  "kind": {"kind": "Pod"},
  "object": {"spec": {"containers": [
    {"name": "app", "securityContext": {"privileged": true},
     "resources": {"limits": {"memory": "256Mi"}}}
  ]}}
}}

no_limit_pod := {"request": {
  "kind": {"kind": "Pod"},
  "object": {"spec": {"containers": [{"name": "app"}]}}
}}

privileged_init_pod := {"request": {
  "kind": {"kind": "Pod"},
  "object": {"spec": {
    "containers": [{"name": "app", "resources": {"limits": {"memory": "256Mi"}}}],
    "initContainers": [{"name": "init", "securityContext": {"privileged": true},
                        "resources": {"limits": {"memory": "64Mi"}}}]
  }}
}}

test_good_pod_allowed if {
  count(deny) == 0 with input as good_pod
}

test_privileged_denied if {
  count(deny) == 1 with input as privileged_pod
}

test_missing_memory_limit_denied if {
  count(deny) == 1 with input as no_limit_pod
}

test_privileged_init_container_denied if {
  count(deny) == 1 with input as privileged_init_pod
}
