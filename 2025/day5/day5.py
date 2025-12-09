from pathlib import Path
from typing import List, Tuple


def parse_input(path: Path) -> Tuple[List[Tuple[int, int]], List[int]]:
    """Parse range lines and number lines separated by a blank line."""
    ranges: List[Tuple[int, int]] = []
    numbers: List[int] = []
    in_second_section = False

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            in_second_section = True
            continue

        if not in_second_section:
            start_str, end_str = line.split("-")
            ranges.append((int(start_str), int(end_str)))
        else:
            numbers.append(int(line))

    return ranges, numbers


def count_numbers_in_ranges(
    ranges: List[Tuple[int, int]], numbers: List[int]
) -> int:
    """Return how many numbers fall in any range."""
    return sum(1 for number in numbers if any(start <= number <= end for start, end in ranges))


def count_ids_from_ranges(ranges: List[Tuple[int, int]]) -> int:
    """Count unique ids covered by the ranges, inclusive of endpoints.

    Overlapping ranges are merged so shared ids are only counted once.
    """
    if not ranges:
        return 0

    merged: List[Tuple[int, int]] = []
    for start, end in sorted(ranges):
        if not merged:
            merged.append((start, end))
            continue

        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return sum(end - start + 1 for start, end in merged)


def get_data_path() -> Path:
    """Prefer input.txt if it exists; otherwise use test.txt."""
    base = Path(__file__).resolve().parent
    input_path = base / "input.txt"
    return input_path if input_path.exists() else base / "test.txt"


def main() -> None:
    data_path = get_data_path()
    ranges, numbers = parse_input(data_path)

    answer1 = count_numbers_in_ranges(ranges, numbers)
    answer2 = count_ids_from_ranges(ranges)
    print(f"Answer1: {answer1}")
    print(f"Answer2: {answer2}")


if __name__ == "__main__":
    main()
