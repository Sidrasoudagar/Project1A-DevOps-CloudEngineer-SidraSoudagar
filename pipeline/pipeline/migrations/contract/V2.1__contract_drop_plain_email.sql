-- CONTRACT STEP B: irreversible. Separate release, after the rollback window
-- and a verified backup or snapshot.
SET lock_timeout = '3s';

ALTER TABLE customer_profiles DROP COLUMN IF EXISTS email_deprecated;

INSERT INTO schema_audit_log (migration_id, description, executed_by, phase)
VALUES ('V2.1', 'Drop email_deprecated', current_user, 'CONTRACT-B');
