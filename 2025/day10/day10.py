#!/usr/bin/env python3
"""Compute minimal presses for both indicator lights and joltage targets."""

from __future__ import annotations

import pathlib
import re
from fractions import Fraction
from typing import Sequence


def parse_row(line: str) -> tuple[int, Sequence[int], Sequence[Sequence[int]], Sequence[int]]:
    """Extract the indicator mask, button toggles, and joltage targets."""
    indicator_section = line[line.index("[") + 1 : line.index("]")]
    indicator_mask = 0
    for idx, char in enumerate(indicator_section):
        if char == "#":
            indicator_mask ^= 1 << idx

    button_masks = []
    button_indices: list[Sequence[int]] = []
    for button in re.findall(r"\(([^)]*)\)", line):
        indices: list[int] = []
        mask = 0
        for part in [p.strip() for p in button.split(",") if p.strip()]:
            idx = int(part)
            indices.append(idx)
            mask ^= 1 << idx
        button_masks.append(mask)
        button_indices.append(indices)

    jolt_section = line[line.index("{") + 1 : line.index("}")]
    jolt_targets = [int(part.strip()) for part in jolt_section.split(",") if part.strip()]
    return indicator_mask, button_masks, button_indices, tuple(jolt_targets)


def min_presses(target: int, buttons: Sequence[int]) -> int:
    """Brute force every subset of buttons to find the minimal presses."""
    best = None
    for subset in range(1 << len(buttons)):
        mask = 0
        for idx, button_mask in enumerate(buttons):
            if subset >> idx & 1:
                mask ^= button_mask
        if mask == target:
            presses = subset.bit_count()
            if best is None or presses < best:
                best = presses

    if best is None:
        raise ValueError("No combination of buttons reaches the target configuration.")
    return best


def min_presses_joltage(target: Sequence[int], button_indices: Sequence[Sequence[int]]) -> int:
    """Solve the integer system to cover each joltage counter with minimal presses."""
    if not target:
        return 0
    rows = len(target)
    cols = len(button_indices)
    matrix: list[list[Fraction]] = [
        [Fraction(0) for _ in range(cols)] for _ in range(rows)
    ]
    for col, indices in enumerate(button_indices):
        for idx in indices:
            matrix[idx][col] = Fraction(1)

    aug = [row[:] + [Fraction(target_val)] for row, target_val in zip(matrix, target)]
    pivot_cols: list[int] = []
    row = 0
    for col in range(cols):
        pivot_row = None
        for r in range(row, rows):
            if aug[r][col] != 0:
                pivot_row = r
                break
        if pivot_row is None:
            continue
        aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
        pivot_cols.append(col)
        pivot_val = aug[row][col]
        aug[row] = [val / pivot_val for val in aug[row]]
        for r in range(rows):
            if r != row and aug[r][col] != 0:
                factor = aug[r][col]
                aug[r] = [rv - factor * pv for rv, pv in zip(aug[r], aug[row])]
        row += 1
        if row == rows:
            break
    rank = row
    for r in range(rank, rows):
        if any(aug[r][c] != 0 for c in range(cols)) or aug[r][-1] != 0:
            raise ValueError("No combination of buttons reaches the joltage target.")

    free_cols = [col for col in range(cols) if col not in pivot_cols]
    particular: list[Fraction] = [Fraction(0) for _ in range(cols)]
    for r, col in enumerate(pivot_cols):
        particular[col] = aug[r][-1]

    null_vectors: dict[int, list[Fraction]] = {}
    for free in free_cols:
        vec = [Fraction(0) for _ in range(cols)]
        vec[free] = Fraction(1)
        for r, col in enumerate(pivot_cols):
            vec[col] = -aug[r][free]
        null_vectors[free] = vec

    if not free_cols:
        if any(
            value < 0 or value.denominator != 1 for value in particular
        ):
            raise ValueError("No combination of buttons reaches the joltage target.")
        return sum(int(value) for value in particular)

    upper_bounds = []
    for indices in button_indices:
        if not indices:
            upper_bounds.append(0)
        else:
            upper_bounds.append(min(target[idx] for idx in indices))

    free_cols.sort(key=lambda col: upper_bounds[col])
    free_vectors = [null_vectors[col] for col in free_cols]
    current = particular.copy()
    best: int | None = None

    def dfs(idx: int) -> None:
        nonlocal best
        if idx == len(free_cols):
            if any(val < 0 or val.denominator != 1 for val in current):
                return
            total = sum(int(val) for val in current)
            if best is None or total < best:
                best = total
            return

        free_col = free_cols[idx]
        vector = free_vectors[idx]
        max_value = upper_bounds[free_col]
        for value in range(max_value + 1):
            for j in range(cols):
                current[j] += vector[j] * value
            dfs(idx + 1)
            for j in range(cols):
                current[j] -= vector[j] * value

    dfs(0)
    if best is None:
        raise ValueError("No combination of buttons reaches the joltage target.")
    return best


def solve(path: pathlib.Path) -> tuple[int, int]:
    """Read the input file and accumulate the minimal presses for each machine."""
    total_indicator = 0
    total_joltage = 0
    for index, line in enumerate(path.read_text().strip().splitlines(), start=1):
        if not line.strip():
            continue
        indicator_mask, button_masks, button_indices, jolt_targets = parse_row(line)
        indicator_presses = min_presses(indicator_mask, button_masks)
        joltage_presses = min_presses_joltage(jolt_targets, button_indices)
        print(
            f"Machine {index}: indicator={indicator_presses} presses, joltage={joltage_presses} presses"
        )
        total_indicator += indicator_presses
        total_joltage += joltage_presses
    return total_indicator, total_joltage


def main() -> None:
    path = pathlib.Path(__file__).with_name("input.txt")
    total_indicator, total_joltage = solve(path)
    print(f"Answer1: {total_indicator}")
    print(f"Answer2: {total_joltage}")


if __name__ == "__main__":
    main()
