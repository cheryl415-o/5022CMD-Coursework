"""Draw the hash table picture from the real Q1 program.
Put this file in the q1_hashing folder and run it. It saves hash_slots.png.
Needs matplotlib:  pip install matplotlib
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from q1_inventory import PharmacyInventory, load_seed

inv = PharmacyInventory()          # table with 101 slots
load_seed(inv)                     # the ten starting products
slots = inv.table._slots           # list of Slot objects

# slot number -> product id, for slots that are in use
used = {i: s.key for i, s in enumerate(slots) if s.state == 1}

fig, (top, bottom) = plt.subplots(2, 1, figsize=(7, 4.2), gridspec_kw={"height_ratios": [1, 2]})

# top: all 101 slots as thin boxes
for i in range(101):
    top.add_patch(Rectangle((i - 0.5, 0), 1, 1, color="#2a78d6" if i in used else "#e8e8e8", ec="white"))
top.set_xlim(-0.5, 100.5); top.set_ylim(0, 1); top.set_yticks([])
top.set_title(f"Whole table: 101 slots, {len(used)} used")

# bottom: zoom on slots 89 to 100
lo, hi = 89, 100
for i in range(lo, hi + 1):
    colour = "#2a78d6" if i in used else "#e8e8e8"
    bottom.add_patch(Rectangle((i - 0.45, 0.2), 0.9, 0.6, color=colour))
    label = str(used[i]) if i in used else "empty"
    bottom.text(i, 0.5, label, ha="center", va="center", fontsize=8, color="white" if i in used else "gray")
    bottom.text(i, 0.05, f"[{i}]", ha="center", fontsize=8)
bottom.annotate("", xy=(98, 0.82), xytext=(92, 0.82), arrowprops=dict(arrowstyle="->", color="#eb6834", connectionstyle="arc3,rad=-0.3"))
bottom.set_title("1203 belongs in slot 92, which is taken, so it is stored in slot 98 (7 checks)", fontsize=9)
bottom.set_xlim(lo - 0.6, hi + 0.6); bottom.set_ylim(0, 1.3); bottom.axis("off")

plt.tight_layout()
plt.savefig("hash_slots.png", dpi=200)
print("saved hash_slots.png")
