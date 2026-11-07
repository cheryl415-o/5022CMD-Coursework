"""Q3 iv - a situation where multithreading DOES help: I/O-bound work.

Each task 'waits' 1 second (simulating a network request / disk read). While
a thread waits, it releases the GIL, so the other threads can run.
"""

import threading
import time

TASKS = 3
WAIT_SECONDS = 1.0


def fake_download(i: int) -> None:
    time.sleep(WAIT_SECONDS)          # stands in for a network call


def sequential() -> int:
    t0 = time.perf_counter_ns()
    for i in range(TASKS):
        fake_download(i)
    return time.perf_counter_ns() - t0


def threaded() -> int:
    t0 = time.perf_counter_ns()
    threads = [threading.Thread(target=fake_download, args=(i,))
               for i in range(TASKS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter_ns() - t0


if __name__ == "__main__":
    seq, thr = sequential(), threaded()
    print(f"=== I/O-bound demo: {TASKS} tasks x {WAIT_SECONDS}s wait ===")
    print(f"Sequential : {seq:,} ns")
    print(f"Threaded   : {thr:,} ns")
    print(f"Observation: threading was {seq / thr:.1f}x faster for I/O-bound work.")
