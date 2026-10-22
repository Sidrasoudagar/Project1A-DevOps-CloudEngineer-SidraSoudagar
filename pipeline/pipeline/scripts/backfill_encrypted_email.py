#!/usr/bin/env python3
"""Throttled, idempotent backfill: customer_profiles.email -> encrypted_email.

Env vars: DATABASE_URL, FERNET_KEY (from a secrets manager in production).
Usage:
  backfill_encrypted_email.py backfill [--batch-size N] [--sleep S] [--resync]
  backfill_encrypted_email.py verify [--sample-percent P]
"""
import argparse
import os
import sys
import time

import psycopg2
from cryptography.fernet import Fernet
from psycopg2 import errors
from psycopg2.extras import execute_values


def connect():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    with conn.cursor() as cur:
        cur.execute("SET lock_timeout = '2s'")
        cur.execute("SET statement_timeout = '60s'")
    conn.commit()
    return conn


def backfill(conn, fernet, batch_size, sleep_s, resync, max_waiters):
    cond = "email IS NOT NULL"
    if not resync:
        cond += " AND encrypted_email IS NULL"
    last_id, total, batches = 0, 0, 0
    started = time.time()

    while True:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT count(*) FROM pg_stat_activity "
                            "WHERE wait_event_type = 'Lock'")
                if cur.fetchone()[0] > max_waiters:
                    conn.rollback()
                    print("Lock waiters detected, pausing 5s", flush=True)
                    time.sleep(5)
                    continue

                cur.execute(
                    f"SELECT id, email FROM customer_profiles "
                    f"WHERE id > %s AND {cond} ORDER BY id LIMIT %s",
                    (last_id, batch_size),
                )
                rows = cur.fetchall()
                if not rows:
                    conn.commit()
                    break

                data = [(r[0], fernet.encrypt(r[1].encode())) for r in rows]
                execute_values(
                    cur,
                    "UPDATE customer_profiles AS c SET encrypted_email = v.enc "
                    "FROM (VALUES %s) AS v(id, enc) WHERE c.id = v.id",
                    data,
                    template="(%s::bigint, %s::bytea)",
                )
            conn.commit()  # commit every batch: no long transaction
        except errors.LockNotAvailable:
            conn.rollback()
            print("Lock timeout, retrying batch", flush=True)
            time.sleep(1)
            continue

        last_id = rows[-1][0]
        total += len(rows)
        batches += 1
        if batches % 10 == 0:
            print(f"migrated {total} rows (last id {last_id})", flush=True)
        time.sleep(sleep_s)  # throttle between batches

    elapsed = max(time.time() - started, 0.001)
    print(f"DONE: {total} rows in {elapsed:.1f}s ({total / elapsed:.0f} rows/s)")


def verify(conn, fernet, sample_percent):
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM customer_profiles "
                    "WHERE email IS NOT NULL AND encrypted_email IS NULL")
        missing = cur.fetchone()[0]

        cur.execute(
            "SELECT id, email, encrypted_email FROM customer_profiles "
            "TABLESAMPLE BERNOULLI (%s) WHERE encrypted_email IS NOT NULL",
            (sample_percent,),
        )
        checked = mismatches = 0
        for _id, email, enc in cur:
            checked += 1
            try:
                ok = fernet.decrypt(bytes(enc)).decode() == email
            except Exception:
                ok = False
            if not ok:
                mismatches += 1

    print(f"Rows missing encrypted_email: {missing}")
    print(f"Sample checked: {checked}, mismatches: {mismatches}")
    result = "PASS" if missing == 0 and mismatches == 0 else "FAIL"
    print(f"VERIFY {result}")
    sys.exit(0 if result == "PASS" else 1)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("backfill")
    b.add_argument("--batch-size", type=int, default=1000)
    b.add_argument("--sleep", type=float, default=0.1)
    b.add_argument("--resync", action="store_true",
                   help="re-encrypt all rows (final reconcile)")
    b.add_argument("--max-lock-waiters", type=int, default=10)
    v = sub.add_parser("verify")
    v.add_argument("--sample-percent", type=float, default=0.01)
    args = p.parse_args()

    fernet = Fernet(os.environ["FERNET_KEY"])
    conn = connect()
    if args.cmd == "backfill":
        backfill(conn, fernet, args.batch_size, args.sleep,
                 args.resync, args.max_lock_waiters)
    else:
        verify(conn, fernet, args.sample_percent)


if __name__ == "__main__":
    main()
