# Project Reflections

**Project:** DevOps & Cloud Engineer - Zero-Downtime CI/CD
**Author:** Sidra Soudagar

---

### 1. What was the most challenging aspect of this project and how did you overcome it?
The most challenging aspect was designing the **Database Migration strategy** (Deliverable 4). In a bank, you cannot lock a 100M-row table. I overcame this by researching the Expand-Contract pattern and designing an idempotent SQL script using `FOR UPDATE SKIP LOCKED` and batch throttling (100ms pauses). This ensures that the database remains available to users while the backfill happens in the background.

### 2. How did you approach the conflict between DevOps velocity (deploying fast) and Compliance (RBI/PCI-DSS)?
The key realization was that **automation is the bridge between velocity and compliance**. Instead of having a human manually check a security box (which slows things down), I coded the compliance into the pipeline itself. Using OPA (Open Policy Agent) and SonarQube, the pipeline automatically blocks bad code in seconds. This means developers get fast feedback, and the bank gets 100% compliance without delaying the deployment.

### 3. What did you learn about the banking/fintech domain during this project?
I learned that in banking, **downtime equals financial loss and regulatory penalties**. A standard e-commerce site might tolerate 5 minutes of downtime, but NovaPay cannot. This is why features like Canary deployments (routing only 1% of traffic to new code) and automated rollbacks (Category A triggers reacting in < 60 seconds) are absolutely mandatory. I also learned the importance of Separation of Duties (SoD) to prevent a single developer from pushing malicious code to production.

### 4. How did you use AI tools to accelerate this project, and where did you apply your own critical thinking?
I used AI to help generate the boilerplate Markdown structures, the Mermaid diagrams, and the initial OPA Rego syntax. However, I applied my own critical thinking to the **architecture decisions**. For example, AI initially suggested using standard `git push` for deployments, but I overrode it to use **ArgoCD (GitOps)** and **Istio** because that is the industry standard for zero-downtime Kubernetes deployments. I also manually calculated the Canary traffic percentages and error thresholds to match real banking SLOs.

### 5. If you were the CTO of NovaPay, what would be your immediate next step after this pipeline is built?
My immediate next step would be to implement **Chaos Engineering** (using tools like LitmusChaos). Building the pipeline is step one, but proving that the pipeline can survive a database failure or a network partition is step two. I would run a simulated failure in Pre-Production to test the automated rollback and incident playbook before going live in Production.

---
## AI Attribution
- **Tool used:** DeepSeek
- **Human review:** Written from the perspective of a DevOps Lead.
