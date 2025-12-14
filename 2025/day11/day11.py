#!/usr/bin/env python3
"""Count all paths from "you" to "out" in the device graph."""

from __future__ import annotations

import pathlib
from collections import defaultdict
from typing import Iterable, Mapping, Sequence


def parse_graph(lines: Iterable[str]) -> Mapping[str, list[str]]:
    graph: dict[str, list[str]] = defaultdict(list)
    for line in lines:
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        node, targets = stripped.split(":", 1)
        children = [token for token in targets.strip().split() if token]
        graph[node.strip()].extend(children)
    return graph


def count_paths(graph: Mapping[str, Sequence[str]], start: str = "you", end: str = "out") -> int:
    """Return number of distinct simple paths from start to end."""
    memo: dict[str, int] = {}

    def dfs(node: str, visited: set[str]) -> int:
        if node == end:
            return 1
        if node in visited:
            return 0
        if node in memo:
            return memo[node]
        visited.add(node)
        total = 0
        for child in graph.get(node, []):
            total += dfs(child, visited)
        visited.remove(node)
        memo[node] = total
        return total

    return dfs(start, set())


def count_paths_with_requirements(
    graph: Mapping[str, Sequence[str]],
    start: str = "svr",
    end: str = "out",
    required: Sequence[str] = ("dac", "fft"),
) -> int:
    """Return number of paths from start to end that visit all required nodes."""
    required_index = {node: idx for idx, node in enumerate(required)}
    completed_mask = (1 << len(required)) - 1

    memo: dict[tuple[str, int], int] = {}

    def dfs(node: str, mask: int) -> int:
        if node == end:
            return 1 if mask == completed_mask else 0
        key = (node, mask)
        if key in memo:
            return memo[key]
        total = 0
        for child in graph.get(node, []):
            next_mask = mask
            if child in required_index:
                next_mask |= 1 << required_index[child]
            total += dfs(child, next_mask)
        memo[key] = total
        return total

    start_mask = 0
    if start in required_index:
        start_mask |= 1 << required_index[start]
    return dfs(start, start_mask)


def solve(path: pathlib.Path) -> tuple[int, int]:
    lines = path.read_text().splitlines()
    graph = parse_graph(lines)
    total_paths = count_paths(graph, start="you", end="out")
    constrained_paths = count_paths_with_requirements(graph)
    return total_paths, constrained_paths


def main() -> None:
    path = pathlib.Path(__file__).with_name("input.txt")
    answer1, answer2 = solve(path)
    print(f"Answer1: {answer1}")
    print(f"Answer2: {answer2}")


if __name__ == "__main__":
    main()
