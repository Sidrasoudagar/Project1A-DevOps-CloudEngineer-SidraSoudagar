# Deliverable 4: Zero-Downtime Database Migration

**Project:** NovaPay Digital Bank
**Author:** Sidra Soudagar

---

## 1. Expand-Contract Pattern

Blue and Green (and App V(N-1) and V(N)) share one PostgreSQL database holding more than 100M rows. Every schema change must work with both application versions, so we never take the database offline.

Worked example: add `encrypted_email` to `customer_profiles` and retire the plaintext `email` column.

| Phase | Action | Rollback |
|---|---|---|
| 1. EXPAND | Add the nullable column `encrypted_email`. Metadata-only change, no table rewrite. | Drop the new column |
| 2. MIGRATE | Deploy App V(N), which writes both columns. A throttled backfill job fills existing rows, committing after every batch. | Stop the job, safe to restart (idempotent) |
| 3. SWITCH | Shift all traffic to App V(N), retire App V(N-1). Run the final reconcile and verification. | Redeploy V(N-1) (old column still exists) |
| 4. CONTRACT | Step A: rename `email` to `email_deprecated`. After the rollback window, Step B: drop it in a later release. | Step A: rename back. Step B: **irreversible**, restore from backup |

CONTRACT is always a separate deployment with its own approval gate.

---

## 2. Tools

- **Migration runner:** Flyway (versioned plain SQL), with `lock_timeout` set in each script.
- **Migration linter:** Squawk, run in CI to block unsafe patterns (blocking index builds, unsafe column changes, drops outside the contract folder).
- **Backfill job:** Python script (`pipeline/scripts/backfill_encrypted_email.py`), run as a separate job from the deploy pipeline.
- **Alternative:** pgroll is a valid option for automated versioned schemas, but this project uses plain SQL for transparency.

---

## 3. Version Compatibility Matrix

| Schema state | App V(N-1) | App V(N) | Next action |
|---|---|---|---|
| Before EXPAND | Works | Fails (column missing) | Run EXPAND |
| After EXPAND | Works | Works (writes both) | Deploy V(N), start backfill |
| After MIGRATE | Works | Works (reads new, writes both) | Verify, shift all traffic |
| V(N-1) retired | None | Works | Final reconcile and verify, then DBA approval |
| After CONTRACT step A (renamed) | Fails | Works | Wait through rollback window |
| After CONTRACT step B (dropped) | Fails | Works | Forward-only fixes |

---

## 4. Safety Rules for Large Tables

- `SET lock_timeout` on every DDL script. If the lock is not obtained, the job retries rather than queueing behind live traffic.
- No long transactions. The backfill commits every batch (default 1000 rows) and sleeps between batches.
- Batches use keyset pagination (`WHERE id > last_id ORDER BY id LIMIT n`), so each batch cost stays constant as the job progresses.
- No index on encrypted values. Ciphertext is randomised, so an index cannot be used for lookups.
- The backfill pauses when lock waiters appear. CPU and latency thresholds are enforced from monitoring: pause the job if CPU stays above 80% or p99 latency rises more than 20%.
- Encryption happens in the job, not in SQL. The key comes from the secrets manager (environment variable in the test setup), never from a script or Git. If the column ever holds account data, PCI-DSS Requirement 3 key management applies.
- Rows updated by App V(N-1) during the overlap are corrected by a final reconcile pass (`backfill --resync`) after V(N-1) is retired, followed by `verify`.

---

## 5. Timing and the Two-Hour Target

Only the EXPAND step runs in the commit-to-production path. The backfill and contract run as separate, scheduled jobs and are not counted in the two-hour measurement. Throughput is measured on the test dataset and extrapolated:

- Test dataset: 1,000,000 rows. Result: see `evidence/backfill-run.txt`.
- Estimate for 100M rows: (measured rows per second) x 100M. Fill in after the run.

---

## 6. Governance and Compliance

- CONTRACT requires approval through a GitHub Environment by a DBA who is not the change author (separation of duties, PCI-DSS 6.5.4).
- Every migration phase writes a record to `schema_audit_log` with the pipeline run ID and approver (audit trail, PCI-DSS 10.2).
- The migration linter and the contract approval are enforced as gates (see `docs/03-compliance-gates/compliance-gates.md`).
- Backups: a verified backup or snapshot is taken before CONTRACT step B.

---
## Related Deliverables
- For the deployment strategies used during this migration, see [Deployment Strategies](../02-deployment-strategies/deployment-strategy.md).
- The actual migration SQL scripts are located in `pipeline/migrations/`.
---

## AI Attribution

- **Tool used:** Claude
- **Human review:** Customized for the NovaPay PostgreSQL 16 context.
