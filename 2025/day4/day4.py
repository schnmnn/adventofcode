file_path = "input.txt"
with open(file_path, 'r', encoding='utf-8') as f:
    grid = [list(line.rstrip('\n')) for line in f.readlines()]

def count_adjacent_rolls(grid, row, col):
    """Count the number of @ symbols in the 8 adjacent positions."""
    count = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            if grid[new_row][new_col] == '@':
                count += 1
    
    return count

# ANSWER 1: Count accessible rolls (fewer than 4 adjacent rolls)
def count_accessible_rolls(grid):
    """Count all rolls that can be accessed."""
    accessible = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '@':
                adjacent_count = count_adjacent_rolls(grid, row, col)
                if adjacent_count < 4:
                    accessible += 1
    return accessible

answer1 = count_accessible_rolls(grid)

# ANSWER 2: Simulate removal process until no more rolls can be removed
def simulate_removal(grid):
    """Iteratively remove accessible rolls until none remain."""
    grid = [row.copy() for row in grid]
    removed_count = 0
    
    while True:
        # find all accessible rolls in current state
        accessible = []
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == '@':
                    adjacent_count = count_adjacent_rolls(grid, row, col)
                    if adjacent_count < 4:
                        accessible.append((row, col))
        
        if not accessible:
            break  # no more accessible rolls
        
        # remove all accessible rolls
        for row, col in accessible:
            grid[row][col] = '.'
            removed_count += 1
    
    return removed_count

answer2 = simulate_removal(grid)

print(f"answer1: {answer1}")
print(f"answer2: {answer2}")