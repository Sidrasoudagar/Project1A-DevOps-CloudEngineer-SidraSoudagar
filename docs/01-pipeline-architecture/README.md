# Deliverable 1: Pipeline Architecture

This folder contains the design and specifications for the 8-stage zero-downtime CI/CD pipeline.

## Contents
- **[architecture.md](./architecture.md)**: The main architectural overview, including the 8 stages and compliance mapping.
- **[diagrams/](./diagrams/)**: Architecture flow diagrams (Mermaid).
- **[stage-details/](./stage-details/)**: Detailed specifications for each of the 8 individual stages (e.g., SAST, DAST, Build).

## Key Highlights
- Reduces commit-to-production time to 34 minutes.
- Implements parallel scanning (SAST and Dependency) to save time.
