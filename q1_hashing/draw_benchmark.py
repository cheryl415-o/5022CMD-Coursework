"""Draw the speed test chart from your own computer's results.
Put this file in the q1_hashing folder and run it (it takes about 1 to 2 minutes).
It runs the benchmark 5 times, averages the results and saves benchmark_chart.png.
Needs matplotlib:  pip install matplotlib
"""
import random

import matplotlib.pyplot as plt

import benchmark   # your benchmark.py

RUNS = 5
hash_times = {n: [] for n in benchmark.SIZES}
array_times = {n: [] for n in benchmark.SIZES}

for run in range(RUNS):
    random.seed(42)
    print(f"run {run + 1} of {RUNS}")
    for n in benchmark.SIZES:
        table, array, ids = benchmark.build(n)
        keys = random.sample(ids, min(benchmark.SEARCHES, n))
        hash_times[n].append(benchmark.time_searches(table.search, keys))
        array_times[n].append(benchmark.time_searches(lambda k: benchmark.array_search(array, k), keys))

sizes = benchmark.SIZES
avg_hash = [sum(hash_times[n]) / RUNS for n in sizes]
avg_array = [sum(array_times[n]) / RUNS for n in sizes]

for n, h, a in zip(sizes, avg_hash, avg_array):
    print(f"{n:>7} records: hash {h:,.0f} ns, array {a:,.0f} ns, array is {a / h:,.0f}x slower")

plt.figure(figsize=(7, 3.5))
plt.plot(sizes, avg_array, marker="o", color="#eb6834", label="Array (linear search)")
plt.plot(sizes, avg_hash, marker="o", color="#2a78d6", label="Hash table")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("number of records")
plt.ylabel("time per search (ns, log scale)")
plt.title("Average time per search over 5 runs")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("benchmark_chart.png", dpi=200)
print("saved benchmark_chart.png")
