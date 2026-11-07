"""Draw the course prerequisite graph from the real Q2 program.
Put this file in the q2_graph folder and run it. It saves course_graph.png.
Needs matplotlib:  pip install matplotlib
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from q2_course_system import build_sample_system

cs = build_sample_system()          # the 7 courses and 7 arrows from the program
g = cs.graph

# column of each course = length of its longest chain of prerequisites
level = {}
def depth(c):
    if c not in level:
        pre = g.listIncomingAdjacentVertex(c)
        level[c] = 0 if not pre else 1 + max(depth(p) for p in pre)
    return level[c]
for c in g.vertices():
    depth(c)

# row of each course inside its column
columns = {}
for c in sorted(g.vertices(), key=lambda c: c.code):
    columns.setdefault(level[c], []).append(c)
pos = {}
for col, items in columns.items():
    for i, c in enumerate(items):
        pos[c] = (col * 2.4, (len(items) - 1) / 2 * 1.5 - i * 1.5)

fig, ax = plt.subplots(figsize=(8, 4))
ax.axis("off")
w, h = 1.6, 0.9
for a in g.vertices():
    for b in g.listOutgoingAdjacentVertex(a):          # arrow a -> b: a is a prerequisite of b
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.add_patch(FancyArrowPatch((x1 + w / 2, y1), (x2 - w / 2, y2), arrowstyle="-|>",
                                     mutation_scale=12, color="#555555", lw=1.2))
for c, (x, y) in pos.items():
    colour = "#2a78d6" if c.is_core() else "#e8833a"   # blue = core, orange = elective
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.1",
                                color=colour))
    ax.text(x, y + 0.15, c.code, ha="center", va="center", color="white", fontweight="bold", fontsize=9)
    ax.text(x, y - 0.18, c.name, ha="center", va="center", color="white", fontsize=6)
ax.set_xlim(-1, max(p[0] for p in pos.values()) + 1.2)
ax.set_ylim(min(p[1] for p in pos.values()) - 1, max(p[1] for p in pos.values()) + 1)
ax.set_title("Arrow Y -> X means Y is a prerequisite of X (blue = core, orange = elective)", fontsize=9)
fig.tight_layout()
fig.savefig("course_graph.png", dpi=200)
print("saved course_graph.png")
