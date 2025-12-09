from pathlib import Path
from functools import reduce
from typing import List


def compute_column(values: List[int], op: str):
    if op == "+":
        return sum(values)
    if op == "*":
        return reduce(lambda acc, x: acc * x, values, 1)
    if op == "-":
        if not values:
            return 0
        head, *tail = values
        return reduce(lambda acc, x: acc - x, tail, head)
    if op == "/":
        if not values:
            return 0
        head, *tail = values
        return reduce(lambda acc, x: acc / x, tail, float(head))
    raise ValueError(f"Unsupported operator: {op}")


def main() -> None:
    data_path = Path(__file__).with_name("input.txt")
    raw_lines = data_path.read_text().splitlines()
    if len(raw_lines) < 2:
        raise ValueError("Input must contain at least one row of numbers and one row of operators.")

    operators = raw_lines[-1].split()
    number_lines = raw_lines[:-1]

    width = len(operators)
    number_rows = [line.split() for line in number_lines]
    if any(len(row) != width for row in number_rows):
        raise ValueError("All rows must have the same number of columns.")

    columns: List[List[int]] = [[] for _ in range(width)]
    for row in number_rows:
        for idx, token in enumerate(row):
            columns[idx].append(int(token))

    column_results = [
        compute_column(col_values, op)
        for col_values, op in zip(columns, operators)
    ]

    answer1 = sum(column_results)
    print(f"Answer1: {answer1}")

    # Answer2: Cephalopod math (right-to-left, digit columns with blanks).
    padded_numbers = number_lines
    max_len = max(len(line) for line in padded_numbers)
    padded_numbers = [line.ljust(max_len) for line in padded_numbers]
    operator_line = raw_lines[-1].ljust(max_len)

    digit_results: List[int] = []
    current_positions: List[int] = []

    def flush_block():
        if not current_positions:
            return
        # positions are collected right-to-left; process left-to-right within block for readability
        positions = sorted(current_positions)
        numbers: List[int] = []
        for pos in positions:
            digits = "".join(
                row[pos] for row in padded_numbers if row[pos] != " "
            )
            if digits:
                numbers.append(int(digits))
        op_chars = [operator_line[pos] for pos in positions if operator_line[pos].strip()]
        if not op_chars:
            raise ValueError(f"No operator found for block at positions {positions}")
        op_char = op_chars[0]
        digit_results.append(compute_column(numbers, op_char))

    for pos in range(max_len - 1, -1, -1):
        column_chars = [row[pos] for row in padded_numbers]
        op_char = operator_line[pos]
        if all(ch == " " for ch in column_chars) and op_char == " ":
            flush_block()
            current_positions = []
            continue
        current_positions.append(pos)
    flush_block()

    answer2 = sum(digit_results)
    print(f"Answer2: {answer2}")


if __name__ == "__main__":
    main()
