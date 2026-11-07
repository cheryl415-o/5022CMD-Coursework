"""Draw the bar chart of T in each round (Figure 6 in the report).
How to use:
  1. Run q3_fibonacci.py in PyCharm until it finishes.
  2. Copy the whole Run window text into a new file called q3_output.txt (same folder as this file).
  3. Run this file. It reads the T values from q3_output.txt and saves rounds_chart.png.
Needs matplotlib:  pip install matplotlib
"""
import re

import matplotlib.pyplot as plt

text = open("q3_output.txt", encoding="utf-8").read()
with_part, without_part = text.split("=== Fibonacci Computation (Without Multithreading) ===")
find_t = lambda part: [int(x.replace(",", "")) / 1e9 for x in re.findall(r"T = ([\d,]+) ns", part)][:10]
thr, seq = find_t(with_part), find_t(without_part)      # seconds, 10 rounds each
avg_t, avg_s = sum(thr) / len(thr), sum(seq) / len(seq)
print(f"with threads: average {avg_t:.2f} s   without threads: average {avg_s:.2f} s")

fig, ax = plt.subplots(figsize=(8, 3.6))
rounds = list(range(1, len(thr) + 1))
bw = 0.38
ax.bar([r - bw / 2 for r in rounds], thr, bw, color="#2a78d6", label=f"With multithreading (average {avg_t:.2f} s)")
ax.bar([r + bw / 2 for r in rounds], seq, bw, color="#e8833a", label=f"Without multithreading (average {avg_s:.2f} s)")
ax.axhline(avg_t, color="#2a78d6", lw=1, ls="--")        # dashed lines = averages
ax.axhline(avg_s, color="#e8833a", lw=1, ls="--")
ax.set_ylim(0, max(thr + seq) * 1.25)                    # bars start at zero
ax.set_xticks(rounds)
ax.set_xlabel("Round")
ax.set_ylabel("Total time T (seconds)")
ax.legend(loc="upper left", frameon=False, ncol=2, fontsize=8)
ax.set_title("Ten rounds: T with and without threads (dashed lines = averages)", fontsize=9)
fig.tight_layout()
fig.savefig("rounds_chart.png", dpi=200)
print("saved rounds_chart.png")
