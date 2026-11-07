"""Draw the call tree of fibonacci(5) by recording the REAL calls of the Q3 function.
Put this file in the q3_concurrency folder and run it. It saves call_tree.png.
Needs matplotlib:  pip install matplotlib
"""
import sys
from collections import Counter

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from q3_fibonacci import fibonacci

N = 5
calls = []          # each call: {"n": ..., "depth": ..., "kids": [...]}
stack = []

def tracer(frame, event, arg):
    """Called by Python on every function call and return."""
    if frame.f_code.co_name != "fibonacci":
        return
    if event == "call":
        node = {"n": frame.f_locals["n"], "depth": len(stack), "kids": []}
        if stack:
            stack[-1]["kids"].append(node)
        calls.append(node)
        stack.append(node)
    elif event == "return":
        stack.pop()

sys.setprofile(tracer)
result = fibonacci(N)
sys.setprofile(None)
root = calls[0]
print(f"fibonacci({N}) = {result}, number of calls = {len(calls)}")
count = Counter(c["n"] for c in calls)
print("calls per n:", dict(sorted(count.items(), reverse=True)))

# place the nodes: leaves from left to right, parents centred above their children
leaf = [0]
def place(node):
    if node["kids"]:
        for k in node["kids"]:
            place(k)
        node["x"] = sum(k["x"] for k in node["kids"]) / len(node["kids"])
    else:
        node["x"] = leaf[0] * 0.72
        leaf[0] += 1
place(root)

fig, ax = plt.subplots(figsize=(8, 4))
ax.axis("off")
for c in calls:
    for k in c["kids"]:
        ax.plot([c["x"], k["x"]], [-c["depth"] - 0.17, -k["depth"] + 0.17], color="#999999", lw=1, zorder=1)
for c in calls:
    n = c["n"]
    base, repeated = n <= 1, count[n] > 1 and n >= 2
    colour = "#e8833a" if repeated else ("#e0e0e0" if base else "#2a78d6")
    ax.add_patch(FancyBboxPatch((c["x"] - 0.3, -c["depth"] - 0.17), 0.6, 0.34,
                                boxstyle="round,pad=0,rounding_size=0.08", color=colour, zorder=2))
    ax.text(c["x"], -c["depth"], f"F({n})", ha="center", va="center", fontsize=7, zorder=3,
            color="black" if base else "white", fontweight="bold")
xs = [c["x"] for c in calls]
ax.set_xlim(min(xs) - 0.5, max(xs) + 0.5)
ax.set_ylim(-5.2, 0.7)
ax.set_title(f"Recorded calls of fibonacci({N}): {len(calls)} calls. Orange = same sub-problem repeated", fontsize=9)
fig.tight_layout()
fig.savefig("call_tree.png", dpi=200)
print("saved call_tree.png")
