from __future__ import annotations

from collections import deque
from functools import lru_cache
from pathlib import Path
from typing import List, Sequence


def read_grid(path: Path) -> List[List[str]]:
    data = path.read_text().splitlines()
    return [list(line) for line in data]


def find_source(grid: Sequence[Sequence[str]]) -> tuple[int, int]:
    for row_index, row in enumerate(grid):
        if "S" in row:
            return row_index, row.index("S")
    raise ValueError("Source marker 'S' not found in the grid.")


def trace_beams(grid: List[List[str]], start_row: int, start_col: int) -> int:
    beams = deque([(start_row + 1, start_col)])
    splits = 0
    seen: set[tuple[int, int]] = set()

    while beams:
        row, col = beams.popleft()
        if (row, col) in seen:
            continue
        seen.add((row, col))

        if row >= len(grid):
            continue

        if col < 0 or col >= len(grid[row]):
            continue

        cell = grid[row][col]
        if cell == "^":
            splits += 1
            beams.append((row + 1, col - 1))
            beams.append((row + 1, col + 1))
        elif cell == ".":
            beams.append((row + 1, col))

    return splits


def count_paths(grid: List[List[str]], start_row: int, start_col: int) -> int:
    @lru_cache(None)
    def helper(row: int, col: int) -> int:
        if row >= len(grid):
            return 1
        if col < 0 or col >= len(grid[row]):
            return 0
        cell = grid[row][col]
        if cell == "^":
            return helper(row + 1, col - 1) + helper(row + 1, col + 1)
        if cell == ".":
            return helper(row + 1, col)
        return 0

    return helper(start_row + 1, start_col)


def main(path: Path) -> None:
    grid = read_grid(path)
    start_row, start_col = find_source(grid)
    splits = trace_beams(grid, start_row, start_col)
    possibilities = count_paths(grid, start_row, start_col)
    print(f"answer1: {splits}")
    print(f"answer2: {possibilities}")


if __name__ == "__main__":
    input_path = Path("input.txt")
    if not input_path.exists():
        raise SystemExit("input.txt not found in current directory.")
    main(input_path)
