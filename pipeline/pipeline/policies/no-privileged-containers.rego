package kubernetes.admission

import rego.v1

# Regular and init containers are both checked.
all_containers := array.concat(
  object.get(input.request.object.spec, "containers", []),
  object.get(input.request.object.spec, "initContainers", []),
)

# Deny privileged containers (PCI-DSS 6.5.1)
deny contains msg if {
  input.request.kind.kind == "Pod"
  some c in all_containers
  c.securityContext.privileged == true
  msg := sprintf("Privileged container not allowed: %v", [c.name])
}

# Deny containers with no memory limit
deny contains msg if {
  input.request.kind.kind == "Pod"
  some c in all_containers
  not c.resources.limits.memory
  msg := sprintf("Memory limit required for container: %v", [c.name])
}
