"""Q1 #4 - compare searching a hash table with a one-dimensional array.

Same data goes into both structures; we time many searches and average them.
"""

import random
import time

from hash_table import HashTable
from product import Product

SIZES = [100, 1_000, 10_000, 50_000]
SEARCHES = 200          # searches per size (random existing keys)
REPEATS = 3             # repeat and take the best to reduce noise


def build(n: int):
    ids = random.sample(range(1, n * 10), n)
    table = HashTable(int(n * 1.5) | 1)       # load factor ~0.67
    array = []
    for pid in ids:
        p = Product(pid, f"Item-{pid}", 10.0, 50)
        table.insert(pid, p)
        array.append(p)
    return table, array, ids


def array_search(array, pid):
    for p in array:
        if p.product_id == pid:
            return p
    return None


def time_searches(fn, keys) -> float:
    best = float("inf")
    for _ in range(REPEATS):
        t0 = time.perf_counter_ns()
        for k in keys:
            fn(k)
        best = min(best, time.perf_counter_ns() - t0)
    return best / len(keys)           # average ns per search


def run() -> None:
    random.seed(42)
    print("\n=== Search benchmark: Hash Table vs Array (average ns / search) ===")
    print(f"{'Records':>9} | {'Hash Table (ns)':>16} | {'Array (ns)':>14} | {'Speed-up':>9}")
    print("-" * 58)
    for n in SIZES:
        table, array, ids = build(n)
        keys = random.sample(ids, min(SEARCHES, n))
        t_hash = time_searches(table.search, keys)
        t_arr = time_searches(lambda k: array_search(array, k), keys)
        print(f"{n:>9,} | {t_hash:>16,.0f} | {t_arr:>14,.0f} | {t_arr / t_hash:>8.1f}x")


if __name__ == "__main__":
    run()
