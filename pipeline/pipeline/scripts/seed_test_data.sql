CREATE TABLE IF NOT EXISTS customer_profiles (
  id BIGSERIAL PRIMARY KEY,
  email TEXT,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS schema_audit_log (
  id BIGSERIAL PRIMARY KEY,
  migration_id TEXT NOT NULL,
  description TEXT,
  executed_by TEXT,
  phase TEXT,
  pipeline_run_id TEXT,
  executed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 1,000,000 rows; every 100th has no email, which proves the NULL bug is fixed.
INSERT INTO customer_profiles (email)
SELECT CASE WHEN g % 100 = 0 THEN NULL
            ELSE 'user' || g || '@novapay.example' END
FROM generate_series(1, 1000000) AS g;
