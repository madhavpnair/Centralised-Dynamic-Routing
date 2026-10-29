import sys
from pathlib import Path

# add parent to module search path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from DynamicSWSF_FP import DynamicSWSF_FP

INF = float("inf")

def test(name, N, E, U, d, expected):
    result = DynamicSWSF_FP(N, E, U, d.copy())
    assert result == expected, f"{name}: expected {expected}, got {result}"
    print(f"PASS: {name}")

test(
    "Overestimated distance",
    [0, 1, 2],
    {0: [(1, 2), (2, 20)], 1: [(2, 3)], 2: []},
    {0},
    [13, 3, 0],
    [5, 3, 0],
)

test(
    "Underestimated distance",
    [0, 1],
    {0: [(1, 5)], 1: []},
    {0},
    [2, 0],
    [5, 0],
)

# overall decrease in path length
test(
    "Cheapest path",
    [0, 1, 2, 3],
    {0: [(1, 2), (2, 1)], 1: [(3, 8)], 2: [(3, 3)], 3: []},
    {0},
    [99, 8, 3, 0],
    [4, 8, 3, 0],
)

# no updates
test(
    "Empty update set",
    [0, 1, 2],
    {0: [(1, 1)], 1: [(2, 1)], 2: []},
    set(),
    [2, 1, 0],
    [2, 1, 0],
)

test(
    "Unreachable vertex",
    [0, 1],
    {0: [], 1: []},
    {0},
    [7, 0],
    [INF, 0],
)


