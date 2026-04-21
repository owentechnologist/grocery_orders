import time
import uuid
from typing import List, Dict, Any
from private_stuff import *


def percentile(values: List[float], p: float) -> float:
    """
    Simple percentile (p in [0, 100]) using linear interpolation between closest ranks.
    Values are assumed non-empty.
    """
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    values_sorted = sorted(values)
    k = (len(values_sorted) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(values_sorted) - 1)
    if f == c:
        return values_sorted[f]
    d0 = values_sorted[f] * (c - k)
    d1 = values_sorted[c] * (k - f)
    return d0 + d1

def fetch_random_pks(n: int = 100) -> List[uuid.UUID]:
    sql = """
        SELECT pk
        FROM grocery.grocery_activity
        ORDER BY random()
        LIMIT %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (n,))
            result = [row[0] for row in cur.fetchall()]
    return result

def fetch_random_accountids( n: int = 100) -> List[str]:
    sql = """
        SELECT accountid
        FROM grocery.grocery_activity
        ORDER BY random()
        LIMIT %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (n,))
            result = [row[0] for row in cur.fetchall()]
    return result

def timed_get_order_by_pk(pk: uuid.UUID) -> float:
    """
    Run a single PK lookup and return duration in milliseconds.
    """
    sql = """
        SELECT
            pk,
            accountid,
            date_of_order,
            status,
            notes,
            promotion_code,
            order_data
        FROM grocery.grocery_activity
        WHERE pk = %s
    """
    start = time.perf_counter()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (pk,))
            _ = cur.fetchone()
    end = time.perf_counter()
    return (end - start) * 1000.0

def timed_get_line_item_count_for_account(accountid: str) -> float:
    """
    Run a single line_item count query for an accountid and return duration in ms.
    """
    sql = """
        SELECT
            COALESCE(SUM(jsonb_array_length(order_data->'lineItems')), 0)
        FROM grocery.grocery_activity
        WHERE accountid = %s
    """
    start = time.perf_counter()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (accountid,))
            _ = cur.fetchone()
    end = time.perf_counter()
    return (end - start) * 1000.0

def summarize_latencies(label: str, latencies_ms: List[float]) -> Dict[str, Any]:
    if not latencies_ms:
        return {
            "label": label,
            "count": 0,
            "p50_ms": 0.0,
            "p90_ms": 0.0,
            "p99_ms": 0.0,
        }

    return {
        "label": label,
        "count": len(latencies_ms),
        "p50_ms": percentile(latencies_ms, 50),
        "p90_ms": percentile(latencies_ms, 90),
        "p99_ms": percentile(latencies_ms, 99),
    }

def main():
    # 1) Prefetch random PKs and accountids
    pks = fetch_random_pks(100)
    accountids = fetch_random_accountids(100)

    print(f"Fetched {len(pks)} random PKs for testing.")
    print(f"Fetched {len(accountids)} random accountids for testing.")

    # 2) Run timed PK lookups
    pk_latencies_ms: List[float] = []
    print("\n=== Timed PK lookups ===")
    for i, pk in enumerate(pks, start=1):
        elapsed_ms = timed_get_order_by_pk(pk)
        pk_latencies_ms.append(elapsed_ms)
        print(f"PK query {i:3d} (pk={pk}): {elapsed_ms:.3f} ms")

    # 3) Run timed line_items count by accountid
    acct_latencies_ms: List[float] = []
    print("\n=== Timed line_items count by accountid ===")
    for i, accountid in enumerate(accountids, start=1):
        elapsed_ms = timed_get_line_item_count_for_account(accountid)
        acct_latencies_ms.append(elapsed_ms)
        print(f"Account query {i:3d} (accountid={accountid}): {elapsed_ms:.3f} ms")

    # 4) Summaries
    print("\n=== Summary Latencies (ms) ===")

    pk_summary = summarize_latencies("get_order_by_pk", pk_latencies_ms)
    acct_summary = summarize_latencies(
        "get_line_item_count_for_account", acct_latencies_ms
    )

    for summary in [pk_summary, acct_summary]:
        print(
            f"{summary['label']}: "
            f"count={summary['count']}, "
            f"P50={summary['p50_ms']:.3f} ms, "
            f"P90={summary['p90_ms']:.3f} ms, "
            f"P99={summary['p99_ms']:.3f} ms"
        )

if __name__ == "__main__":
    main()

