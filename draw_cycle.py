"""Draw the refused arrow CS401 -> CS201 using the real Q2 program.
Put this file in the q2_graph folder and run it. It saves cycle_graph.png.
Needs matplotlib:  pip install matplotlib
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from q2_course_system import build_sample_system

cs = build_sample_system()
g = cs.graph
a, b = cs.by_code["CS401"], cs.by_code["CS201"]      # we try to add the arrow CS401 -> CS201

# ask the real program (same call as the menu: CS201 requires CS401)
print("wouldCreateCycle(CS401, CS201) =", g.wouldCreateCycle(a, b))
print("program says:", cs.add_prerequisite(b, a))
print("edge was added?", g.hasEdge(a, b))

# find the path CS201 -> ... -> CS401 that already exists (breadth-first search)
parent, queue = {b: None}, [b]
while queue:
    cur = queue.pop(0)
    for nxt in g.listOutgoingAdjacentVertex(cur):
        if nxt not in parent:
            parent[nxt] = cur
            queue.append(nxt)
path, cur = [], a
while cur is not None:
    path.append(cur)
    cur = parent[cur]
path.reverse()
print("existing path:", " -> ".join(c.code for c in path))
path_edges = set(zip(path, path[1:]))

# same layout idea as draw_graph.py
level = {}
def depth(c):
    if c not in level:
        pre = g.listIncomingAdjacentVertex(c)
        level[c] = 0 if not pre else 1 + max(depth(p) for p in pre)
    return level[c]
for c in g.vertices():
    depth(c)
columns = {}
for c in sorted(g.vertices(), key=lambda c: c.code):
    columns.setdefault(level[c], []).append(c)
pos = {}
for col, items in columns.items():
    for i, c in enumerate(items):
        pos[c] = (col * 2.4, (len(items) - 1) / 2 * 1.5 - i * 1.5)

fig, ax = plt.subplots(figsize=(8, 4.3))
ax.axis("off")
w, h = 1.6, 0.9
for u in g.vertices():
    for v in g.listOutgoingAdjacentVertex(u):
        (x1, y1), (x2, y2) = pos[u], pos[v]
        on_path = (u, v) in path_edges
        ax.add_patch(FancyArrowPatch((x1 + w / 2, y1), (x2 - w / 2, y2), arrowstyle="-|>", mutation_scale=12,
                                     color="#e8833a" if on_path else "#aaaaaa", lw=2.4 if on_path else 1.1))
(x1, y1), (x2, y2) = pos[a], pos[b]                    # the refused arrow, drawn in red and curved
ax.add_patch(FancyArrowPatch((x1, y1 - h / 2), (x2, y2 - h / 2), arrowstyle="-|>", mutation_scale=14,
                             color="#d62728", lw=2.2, linestyle="--", connectionstyle="arc3,rad=-0.6"))
for c, (x, y) in pos.items():
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.1",
                                color="#2a78d6" if c.is_core() else "#e8833a", alpha=1 if c in path else 0.45))
    ax.text(x, y + 0.15, c.code, ha="center", va="center", color="white", fontweight="bold", fontsize=9)
    ax.text(x, y - 0.18, c.name, ha="center", va="center", color="white", fontsize=6)
ax.set_xlim(-1, max(p[0] for p in pos.values()) + 1.2)
ax.set_ylim(min(p[1] for p in pos.values()) - 2.4, max(p[1] for p in pos.values()) + 1)
ax.set_title("Red dashed: refused arrow CS401 -> CS201.  Thick orange: path that already exists", fontsize=9)
fig.tight_layout()
fig.savefig("cycle_graph.png", dpi=200)
print("saved cycle_graph.png")
