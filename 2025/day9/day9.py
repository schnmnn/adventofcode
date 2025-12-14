from __future__ import annotations

from pathlib import Path
from typing import Sequence, Tuple, Optional, Iterable

Point = Tuple[int, int]
INPUT_PATH = Path(__file__).resolve().parent / "input.txt"


def read_points(path: Path) -> list[Point]:
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    points: list[Point] = []
    for line in path.read_text().splitlines():
        cleaned = line.strip()
        if not cleaned or cleaned.startswith("#"):
            continue
        parts = [token for token in cleaned.replace(",", " ").split() if token]
        if len(parts) != 2:
            raise ValueError(f"expected two values for a point, got: {cleaned}")
        row, col = int(parts[0]), int(parts[1])
        points.append((row, col))
    return points


def largest_rectangle_simple(points: Sequence[Point]) -> Optional[int]:
    if len(points) < 2:
        return None
    best_area: Optional[int] = None
    n = len(points)
    for i in range(n - 1):
        r1, c1 = points[i]
        for j in range(i + 1, n):
            r2, c2 = points[j]
            if r1 == r2 or c1 == c2:
                continue
            height = abs(r2 - r1) + 1
            width = abs(c2 - c1) + 1
            area = height * width
            if best_area is None or area > best_area:
                best_area = area
    return best_area


def vertical_edges(points: Sequence[Point]) -> Iterable[tuple[int, int, int]]:
    n = len(points)
    for i in range(n):
        r1, c1 = points[i]
        r2, c2 = points[(i + 1) % n]
        if c1 != c2:
            continue
        if r1 == r2:
            continue
        yield c1, min(r1, r2), max(r1, r2)


def build_slabs(points: Sequence[Point]) -> list[tuple[int, int, list[tuple[int, int]]]]:
    if len(points) < 2:
        return []
    edges = list(vertical_edges(points))
    unique_rows = sorted({row for row, _ in points})
    slabs: list[tuple[int, int, list[tuple[int, int]]]] = []
    for start, end in zip(unique_rows, unique_rows[1:]):
        if start == end:
            continue
        y_line = (start + end) / 2
        crossings = sorted(x for x, low, high in edges if low <= y_line < high)
        intervals: list[tuple[int, int]] = []
        for k in range(0, len(crossings), 2):
            if k + 1 >= len(crossings):
                break
            intervals.append((crossings[k], crossings[k + 1]))
        if intervals:
            slabs.append((start, end, intervals))
    return slabs


def rectangle_within_slabs(
    slabs: list[tuple[int, int, list[tuple[int, int]]]], top: int, bottom: int, left: int, right: int
) -> bool:
    relevant = False
    for start, end, intervals in slabs:
        if end <= top or start >= bottom:
            continue
        relevant = True
        if not any(start_x <= left and right <= end_x for start_x, end_x in intervals):
            return False
    return relevant


def largest_rectangle_constrained(points: Sequence[Point]) -> Optional[int]:
    if len(points) < 2:
        return None

    slabs = build_slabs(points)
    best_area: Optional[int] = None
    n = len(points)
    for i in range(n - 1):
        r1, c1 = points[i]
        for j in range(i + 1, n):
            r2, c2 = points[j]
            if r1 == r2 or c1 == c2:
                continue
            top, bottom = min(r1, r2), max(r1, r2)
            left, right = min(c1, c2), max(c1, c2)
            if not rectangle_within_slabs(slabs, top, bottom, left, right):
                continue
            area = (bottom - top + 1) * (right - left + 1)
            if best_area is None or area > best_area:
                best_area = area
    return best_area


def main() -> None:
    if not INPUT_PATH.exists():
        raise SystemExit(f"{INPUT_PATH} not found")
    points = read_points(INPUT_PATH)
    area1 = largest_rectangle_simple(points)
    area2 = largest_rectangle_constrained(points)
    print(f"Answer1: {area1 if area1 is not None else 0}")
    print(f"Answer2: {area2 if area2 is not None else 0}")


if __name__ == "__main__":
    main()
