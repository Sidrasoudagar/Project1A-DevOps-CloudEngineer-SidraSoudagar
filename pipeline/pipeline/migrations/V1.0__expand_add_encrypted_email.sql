-- EXPAND PHASE: backward compatible, metadata-only change.
-- App V(N-1) ignores the new column.
SET lock_timeout = '3s';

ALTER TABLE customer_profiles
  ADD COLUMN IF NOT EXISTS encrypted_email BYTEA;

INSERT INTO schema_audit_log (migration_id, description, executed_by, phase)
VALUES ('V1.0', 'Add nullable encrypted_email column', current_user, 'EXPAND');
