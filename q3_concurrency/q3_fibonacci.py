"""Q3 - Fibonacci with and without multithreading (10 rounds each).

Time_Elapsed = End_Time_Of_Thread_Finished_Last - Start_Time_Of_Thread_That_Started_First
All times use time.perf_counter_ns() (nanoseconds).
"""

import sys
import threading
import time

NUMBERS = (35, 38, 40)
ROUNDS = 10


def fibonacci(n: int) -> int:
    """Naive recursive Fibonacci.

    Primitive operation count: T(n) = T(n-1) + T(n-2) + c, T(0)=T(1)=c'
    -> T(n) grows like phi^n, so the function is O(2^n) (tight bound O(phi^n),
    phi ~ 1.618).
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ---------------------------------------------------------------- threaded
def worker(n: int, results: dict, times: dict) -> None:
    """Thread body: compute fib(n) and record its own start / end time."""
    times[n] = {"start": time.perf_counter_ns()}
    results[n] = fibonacci(n)
    times[n]["end"] = time.perf_counter_ns()


def run_threaded() -> tuple[dict, int]:
    results: dict = {}
    times: dict = {}
    threads = [threading.Thread(target=worker, args=(n, results, times))
               for n in NUMBERS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    first_start = min(v["start"] for v in times.values())
    last_end = max(v["end"] for v in times.values())
    return results, last_end - first_start


# -------------------------------------------------------------- sequential
def run_sequential() -> tuple[dict, int]:
    results = {}
    start = time.perf_counter_ns()
    for n in NUMBERS:
        results[n] = fibonacci(n)
    end = time.perf_counter_ns()
    return results, end - start


# ------------------------------------------------------------------ driver
def experiment(title: str, runner) -> float:
    print(f"\n=== Fibonacci Computation ({title}) ===")
    totals = []
    for r in range(1, ROUNDS + 1):
        results, elapsed = runner()
        totals.append(elapsed)
        fibs = ", ".join(f"Fib({n})={results[n]}" for n in NUMBERS)
        print(f"Round {r:>2}: {fibs} | T = {elapsed:,} ns")
    avg = sum(totals) / len(totals)
    print(f"Average T ({title}): {avg:,.0f} ns")
    return avg


def main() -> None:
    print(f"Python {sys.version.split()[0]} | GIL enabled: "
          f"{getattr(sys, '_is_gil_enabled', lambda: True)()}")
    avg_thr = experiment("With Multithreading", run_threaded)
    avg_seq = experiment("Without Multithreading", run_sequential)

    change = (avg_seq - avg_thr) / avg_seq * 100
    print("\n=== Summary ===")
    print(f"Average with multithreading    : {avg_thr:,.0f} ns")
    print(f"Average without multithreading : {avg_seq:,.0f} ns")
    if change >= 0:
        print(f"Observation: Multithreading reduced the average time by "
              f"{change:.1f}%.")
    else:
        print(f"Observation: Multithreading did NOT help; it was "
              f"{-change:.1f}% slower than the sequential version.")


if __name__ == "__main__":
    main()
