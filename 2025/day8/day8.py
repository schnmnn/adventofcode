from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable, Sequence, Tuple

Point = Tuple[float, float, float]

CONNECTION_ATTEMPT_LIMIT = 1000
INPUT_PATH = Path(__file__).resolve().parent / "input.txt"


def read_points(path: Path) -> list[Point]:
    text = path.read_text()
    lines = (line.strip() for line in text.splitlines())
    points: list[Point] = []
    for line in lines:
        if not line or line.startswith("#"):
            continue
        try:
            coords = tuple(float(value) for value in line.split(","))
        except ValueError as err:
            raise ValueError(f"invalid line in {path.name}: {line}\n{err}")
        if len(coords) != 3:
            raise ValueError(f"expected 3 coordinates, got {len(coords)} in {path.name}: {line}")
        points.append(coords)
    return points


def squared_distance(a: Point, b: Point) -> float:
    return sum((u - v) ** 2 for u, v in zip(a, b))


def generate_edges(points: Sequence[Point]) -> Iterable[tuple[float, int, int]]:
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            yield squared_distance(points[i], points[j]), i, j


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.size = [1] * size

    def find(self, index: int) -> int:
        if self.parent[index] != index:
            self.parent[index] = self.find(self.parent[index])
        return self.parent[index]

    def union(self, a: int, b: int) -> tuple[bool, int]:
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False, self.size[root_a]
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        return True, self.size[root_a]


def build_circuits(points: Sequence[Point], limit: int | None = None) -> tuple[list[tuple[int, int, float, bool, int]], UnionFind]:
    if len(points) < 2:
        raise ValueError("need at least two points to establish connections")

    edges = sorted(generate_edges(points), key=lambda item: item[0])
    uf = UnionFind(len(points))
    connections: list[tuple[int, int, float, bool, int]] = []

    if limit == 0:
        return connections, uf

    for distance_sq, i, j in edges:
        merged, component_size = uf.union(i, j)
        connections.append((i, j, math.sqrt(distance_sq), merged, component_size))
        if limit is not None and len(connections) == limit:
            break

    return connections, uf


def circuit_sizes(uf: UnionFind, total: int) -> list[int]:
    sizes: dict[int, int] = {}
    for index in range(total):
        root = uf.find(index)
        sizes[root] = uf.size[root]
    return list(sizes.values())


def find_last_connection(points: Sequence[Point]) -> tuple[int, int, float]:
    if len(points) < 2:
        raise ValueError("need at least two points to establish a connection")

    edges = sorted(generate_edges(points), key=lambda item: item[0])
    uf = UnionFind(len(points))
    merges = 0
    last_connection: tuple[int, int, float] | None = None

    for distance_sq, i, j in edges:
        merged, _ = uf.union(i, j)
        if merged:
            merges += 1
            last_connection = (i, j, math.sqrt(distance_sq))
            if merges == len(points) - 1:
                break

    if last_connection is None:
        raise ValueError("no connections could be formed")
    return last_connection


def main() -> None:
    if not INPUT_PATH.exists():
        raise SystemExit(f"{INPUT_PATH} not found")
    points = read_points(INPUT_PATH)
    if len(points) < 2:
        raise SystemExit("at least two coordinates are required to find the closest pair")

    _, uf = build_circuits(points, CONNECTION_ATTEMPT_LIMIT)
    sizes = circuit_sizes(uf, len(points))
    top_sizes = sorted(sizes, reverse=True)[:3]
    largest_product = math.prod(top_sizes) if len(top_sizes) == 3 else 0
    print(f"Answer1: {largest_product}")

    i, j, _ = find_last_connection(points)
    x_product = points[i][0] * points[j][0]
    print(f"Answer2: {int(x_product)}")


if __name__ == "__main__":
    main()
