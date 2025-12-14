#!/usr/bin/env python3
"""Determine how many regions can fit a given set of presents."""

from __future__ import annotations

import pathlib
from collections import defaultdict
from collections import defaultdict
from typing import Iterable, Sequence


def normalize(cells: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    cells = tuple(cells)
    min_row = min(r for r, _ in cells)
    min_col = min(c for _, c in cells)
    return tuple(sorted((r - min_row, c - min_col) for r, c in cells))


def all_transformations(shape_lines: Sequence[str]) -> list[list[tuple[int, int]]]:
    cells = [(r, c) for r, row in enumerate(shape_lines) for c, ch in enumerate(row) if ch == "#"]
    transforms: set[tuple[tuple[int, int], ...]] = set()

    def rotate(cells_set: set[tuple[int, int]]) -> set[tuple[int, int]]:
        return {(c, -r) for r, c in cells_set}

    def flip(cells_set: set[tuple[int, int]]) -> set[tuple[int, int]]:
        return {(r, -c) for r, c in cells_set}

    base = set(cells)
    for flip_mode in (False, True):
        current = flip(base) if flip_mode else base
        for _ in range(4):
            transforms.add(normalize(current))
            current = rotate(current)

    return [list(transform) for transform in transforms]


def parse_shapes(lines: Sequence[str]) -> tuple[dict[int, list[str]], int]:
    shapes: dict[int, list[str]] = {}
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if not line:
            idx += 1
            continue
        if ":" in line:
            prefix = line.split(":", 1)[0].strip()
            if "x" in prefix:
                break
        else:
            idx += 1
            continue
        if ":" not in line:
            idx += 1
            continue
        key = int(line.split(":", 1)[0])
        idx += 1
        shape_lines: list[str] = []
        while idx < len(lines) and lines[idx].strip() and ":" not in lines[idx]:
            shape_lines.append(lines[idx].rstrip())
            idx += 1
        shapes[key] = shape_lines
    return shapes, idx


def parse_regions(lines: Sequence[str], start_idx: int) -> list[tuple[int, int, list[int]]]:
    regions = []
    for line in lines[start_idx:]:
        stripped = line.strip()
        if not stripped:
            continue
        if ":" not in stripped:
            continue
        dims, counts = stripped.split(":", 1)
        width_str, height_str = dims.strip().split("x")
        counts_list = [int(token) for token in counts.strip().split()]
        regions.append((int(width_str), int(height_str), counts_list))
    return regions


def can_fit_region(
    width: int,
    height: int,
    counts: Sequence[int],
    shape_transforms: Sequence[list[list[tuple[int, int]]]],
    shape_area: Sequence[int],
) -> bool:
    if len(counts) != len(shape_transforms):
        return False
    total_cells = sum(counts[i] * shape_area[i] for i in range(len(counts)))
    if total_cells > width * height:
        return False

    placements_by_shape: list[
        list[tuple[tuple[int, int], ..., int]]
    ] = []
    for transforms in shape_transforms:
        placements: list[tuple[tuple[int, int], ...]] = []
        seen: set[tuple[tuple[int, int], ...]] = set()
        for transform in transforms:
            max_row = max(r for r, _ in transform)
            max_col = max(c for _, c in transform)
            if max_row >= height or max_col >= width:
                continue
            for base_row in range(0, height - max_row):
                for base_col in range(0, width - max_col):
                    row_masks: dict[int, int] = {}
                    for dr, dc in transform:
                        row = base_row + dr
                        col = base_col + dc
                        row_masks[row] = row_masks.get(row, 0) | (1 << col)
                    placement = tuple(sorted(row_masks.items()))
                    placement_size = sum(mask.bit_count() for _, mask in placement)
                    if placement in seen:
                        continue
                    seen.add(placement)
                    placements.append((placement, placement_size))
        placements_by_shape.append(placements)

    counts_list = list(counts)
    for idx in range(len(counts_list)):
        if counts_list[idx] > 0 and not placements_by_shape[idx]:
            return False

    grid = [0] * height
    memo: dict[tuple[int, tuple[tuple[int, ...], ...]], bool] = {}
    occupied = 0
    remaining_needed = sum(counts_list[i] * shape_area[i] for i in range(len(counts_list)))

    shape_sequence = sorted(
        range(len(counts_list)),
        key=lambda idx: (-counts_list[idx], len(placements_by_shape[idx]) or float("inf")),
    )

    def dfs(order_idx: int) -> bool:
        nonlocal occupied, remaining_needed
        if order_idx == len(shape_sequence):
            return True
        if remaining_needed > width * height - occupied:
            return False
        key = (order_idx, tuple(counts_list), tuple(grid))
        if key in memo:
            return memo[key]
        shape_idx = shape_sequence[order_idx]
        if counts_list[shape_idx] == 0:
            result = dfs(order_idx + 1)
            memo[key] = result
            return result
        for placement_mask, placement_size in placements_by_shape[shape_idx]:
            if any(grid[row] & mask for row, mask in placement_mask):
                continue
            for row, mask in placement_mask:
                grid[row] |= mask
            counts_list[shape_idx] -= 1
            remaining_needed -= shape_area[shape_idx]
            occupied += placement_size
            next_idx = order_idx + (0 if counts_list[shape_idx] > 0 else 1)
            if dfs(next_idx):
                memo[key] = True
                return True
            occupied -= placement_size
            remaining_needed += shape_area[shape_idx]
            counts_list[shape_idx] += 1
            for row, mask in placement:
                grid[row] ^= mask
        memo[key] = False
        return False

    return dfs(0)


def solve(path: pathlib.Path) -> int:
    lines = path.read_text().splitlines()
    shapes, region_start = parse_shapes(lines)
    regions = parse_regions(lines, region_start)

    shape_keys = sorted(shapes.keys())
    shape_transforms = []
    shape_area = []
    for key in shape_keys:
        transforms = all_transformations(shapes[key])
        shape_transforms.append(transforms)
        shape_area.append(len(transforms[0]))

    fit_count = 0
    for width, height, counts in regions:
        if can_fit_region(width, height, counts, shape_transforms, shape_area):
            fit_count += 1
    return fit_count


def main() -> None:
    path = pathlib.Path(__file__).with_name("input.txt")
    result = solve(path)
    print(f"Answer1: {result}")


if __name__ == "__main__":
    main()
