with open('input.txt') as file:
    lines = [line.strip() for line in file]

# Split each line into characters to form a 2D array
grid = [list(line) for line in lines]

def get_character_positions():
    symbol_positions = []   # To store the positions of non-dot characters
    number_positions = []   # To store the positions of number characters
    asterisk_positions = [] # To store the positions of asterisk characters

    # Iterate through each row
    for i in range(len(grid)):
        # Iterate through each column in the row
        for j in range(len(grid[i])):
            char = grid[i][j]
            #print(char)
            # Check if the current character is a number
            if char.isdigit():
                #print(char)
                number_positions.append((i, j))
            # Check if the current character is not a dot and not a digit
            elif char != '.':
                symbol_positions.append((i, j))
                if char == '*':
                    asterisk_positions.append((i,j))
                else:
                    continue
    return symbol_positions, number_positions, asterisk_positions


# Function to get neighbors of a given cell
def get_neighbors(row, col, max_row, max_col):
    # Positions relative to the current cell
    neighbor_positions = [
        (-1, -1), (-1, 0), (-1, 1),  # Upper row
        (0, -1),           (0, 1),    # Left and right
        (1, -1), (1, 0), (1, 1)       # Lower row
    ]
    neighbors = []
    for dr, dc in neighbor_positions:
        r, c = row + dr, col + dc
        # Check if the position is within the grid boundaries
        if 0 <= r < max_row and 0 <= c < max_col:
            neighbors.append((r, c))
    return neighbors

def get_numbers_and_positions():
    # Set to store unique adjacent numbers
    adjacent_numbers = set()
    adjacent_number_positions = set()

    # Iterate over each non-dot character
    for row, col in get_character_positions()[0]:
        # Get all valid neighbors
        neighbors = get_neighbors(row, col, len(grid), len(grid[0]))
        # Check each neighbor
        for nr, nc in neighbors:
            if grid[nr][nc].isdigit():
                adjacent_numbers.add(grid[nr][nc])
                adjacent_number_positions.add((grid[nr][nc], (nr, nc)))
    return adjacent_numbers, adjacent_number_positions


def get_full_number_horizontal(grid, start_row, start_col):
    number = grid[start_row][start_col]

    # Initialize start and end positions
    start_pos = end_pos = start_col

    # Check to the left
    col = start_col - 1
    while col >= 0 and grid[start_row][col].isdigit():
        number = grid[start_row][col] + number
        start_pos = col
        col -= 1

    # Check to the right
    col = start_col + 1
    while col < len(grid[0]) and grid[start_row][col].isdigit():
        number += grid[start_row][col]
        end_pos = col
        col += 1

    return number, (start_row, start_pos), (start_row, end_pos)

def get_full_number_with_position():
    # Using the adjacent_number_positions from earlier
    full_numbers_with_positions = set()

    for _, pos in get_numbers_and_positions()[1]:
        full_number, start_pos, end_pos = get_full_number_horizontal(grid, pos[0], pos[1])
        full_numbers_with_positions.add((full_number, start_pos, end_pos))

    return full_numbers_with_positions

def sum_up_numbers():
    sum = 0
    for i in get_full_number_with_position():
        sum = sum + int(i[0])
    return sum

print(f'Answer one is {sum_up_numbers()}')