-- CONTRACT STEP A: only in a separate, DBA-approved deployment.
-- Run after App V(N-1) is retired and the final verify has passed.
SET lock_timeout = '3s';

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM customer_profiles
             WHERE email IS NOT NULL AND encrypted_email IS NULL) THEN
    RAISE EXCEPTION 'Contract blocked: rows are missing encrypted_email';
  END IF;
END $$;

ALTER TABLE customer_profiles RENAME COLUMN email TO email_deprecated;

INSERT INTO schema_audit_log (migration_id, description, executed_by, phase)
VALUES ('V2.0', 'Rename email to email_deprecated', current_user, 'CONTRACT-A');
