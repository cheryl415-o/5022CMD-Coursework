# 5022CMD Advanced Algorithms - Coursework

**Student:** Teh Cheryl (P24016487)
**Institution:** INTI International College Penang
**Submission date:** 8 November 2026

## Contents

| Folder | Question | Main program |
| --- | --- | --- |
| `q1_hashing/` | Q1: Hash table for a pharmacy inventory, and hash table vs array benchmark | `q1_inventory.py` |
| `q2_graph/` | Q2: Generic directed graph for a course prerequisite system | `q2_course_system.py` |
| `q3_concurrency/` | Q3: Recursive Fibonacci with and without threads, plus an I/O demo | `q3_fibonacci.py`, `q3_io_demo.py` |

## Requirements

- Tested with Python 3.14.7
- Only the standard library is needed to run the programs.
- `matplotlib` is needed only to run the `draw_*.py` files.

## How to run
Open a terminal in the project folder (the folder that contains q1_hashing, q2_graph and q3_concurrency) and run the commands below one after another.

```
cd q1_hashing
python q1_inventory.py       # pharmacy menu (option 6 runs the benchmark)
python benchmark.py          # benchmark only

cd ../q2_graph
python q2_course_system.py   # course prerequisite menu

cd ../q3_concurrency
python q3_fibonacci.py       # takes about 15 minutes (10 rounds)
python q3_io_demo.py         # about 4 seconds
```

## Notes

- `draw_*.py` files and the `.png` files are only used to make the figures in the report. They are not part of the required programs.
- The Q3 Fibonacci program takes a long time because it uses the slow recursive method on purpose.
- Results (times) will be a little different on each computer.
