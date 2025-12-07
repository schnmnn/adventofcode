import re
import os
import sys
from collections import Counter

def read_lines():
    # read only input.txt (ignore test.txt)
    file_path = "input.txt"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Eingabefile '{file_path}' nicht gefunden.")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()

lines = read_lines()

def largest_2digit_from_line(line: str) -> str | None:
    """Find the largest 2-digit number preserving digit order per notebook logic."""
    digits = re.findall(r"\d", line)
    if len(digits) < 2:
        return None
    largest = max(digits)
    largest_idx = digits.index(largest)
    after = digits[largest_idx + 1 :]
    if after:
        second = max(after)
        return largest + second
    # no digit after the first largest -> pick second largest overall and keep order
    remaining = digits.copy()
    remaining.remove(largest)
    second_largest = max(remaining)
    second_idx = digits.index(second_largest)
    if second_idx < largest_idx:
        return second_largest + largest
    return largest + second_largest

def largest_k_subsequence(digits: list, k: int) -> str:
    """Greedy: lexicographically largest subsequence of length k preserving order."""
    n = len(digits)
    if k <= 0:
        return ""
    if k >= n:
        return "".join(digits)
    res = []
    start = 0
    for remaining in range(k, 0, -1):
        end = n - remaining  # last index allowed to pick for this position
        best = None
        best_idx = start
        for i in range(start, end + 1):
            d = digits[i]
            if best is None or d > best:
                best = d
                best_idx = i
                if best == "9":  # early exit
                    break
        res.append(best)
        start = best_idx + 1
    return "".join(res)

# PART 1: sum of largest 2-digit numbers per line
answer1 = 0
for line in lines:
    val = largest_2digit_from_line(line)
    if val and val.isdigit():
        answer1 += int(val)

# PART 2: sum of largest 12-digit numbers (selecting lexicographically largest subsequence length 12)
answer2 = 0
for line in lines:
    digits = re.findall(r"\d", line)
    if len(digits) >= 12:
        largest12 = largest_k_subsequence(digits, 12)
        if largest12 and largest12.isdigit():
            answer2 += int(largest12)

print(f"answer1: {answer1}")
print(f"answer2: {answer2}")