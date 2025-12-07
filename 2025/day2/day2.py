file_path = "input.txt"
with open(file_path, 'r', encoding='utf-8') as f:
    data = f.read()

# each comma-separated item is a range (e.g. '11-22') or a single id
raw_ranges = [s.strip() for s in data.split(',') if s.strip()]

# expand ranges
expanded_ids = []
for item in raw_ranges:
    if '-' in item:
        a, b = [p.strip() for p in item.split('-', 1)]
        if a.isdigit() and b.isdigit():
            start, end = int(a), int(b)
            if start <= end:
                expanded_ids.extend([str(n) for n in range(start, end + 1)])
            else:
                expanded_ids.extend([str(n) for n in range(start, end - 1, -1)])
        else:
            parts = [p.strip() for p in item.split('-') if p.strip()]
            expanded_ids.extend(parts)
    else:
        expanded_ids.append(item)

# skip ids with leading zeros
valid_ids = [id_ for id_ in expanded_ids if not (len(id_) > 1 and id_.startswith('0'))]

# PART 1: check if id has repeating pattern (left half == right half)
def is_repeated(s: str) -> bool:
    if not s or len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    return s[:mid] == s[mid:]

invalid_ids_v1 = [id_ for id_ in valid_ids if is_repeated(id_)]
numeric_invalids_v1 = [int(x) for x in invalid_ids_v1 if x.isdigit()]
answer1 = sum(numeric_invalids_v1)

# PART 2: check how many times the shortest repeating pattern repeats
def get_repeat_count(s: str) -> int:
    """Return how many times the shortest repeating pattern repeats in s."""
    if not s:
        return 1
    n = len(s)
    for d in range(1, n // 2 + 1):
        if n % d == 0:
            pattern = s[:d]
            if s == pattern * (n // d):
                return n // d
    return 1

invalid_ids_v2 = [id_ for id_ in valid_ids if get_repeat_count(id_) >= 2]
numeric_invalids_v2 = [int(x) for x in invalid_ids_v2 if x.isdigit()]
answer2 = sum(numeric_invalids_v2)

print(f"Answer1: {answer1}")
print(f"Answer2: {answer2}")