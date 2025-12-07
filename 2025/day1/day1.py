with open('input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

def answer_one(filename):
    try:
        with open(filename, 'r') as f:
            # Read lines and remove any empty ones
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return "Error: File not found."

    position = 50
    zero_hits = 0

    # Process each instruction
    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        
        if direction == 'L':
            # Move left: subtract distance
            position = (position - distance) % 100
        elif direction == 'R':
            # Move right: add distance
            position = (position + distance) % 100
            
        # Check if we landed on 0
        if position == 0:
            zero_hits += 1

    return zero_hits


def answer_two(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return "Error: File not found."

    position = 50
    total_zero_touches = 0

    for line in lines:
        clean_line = line.strip()
        if not clean_line: continue
        
        direction = clean_line[0]
        try:
            distance = int(clean_line[1:].strip())
        except ValueError:
            continue

        # 1. Count full circles (every 100 steps touches 0 once)
        total_zero_touches += distance // 100
        
        # 2. Check the remaining steps for a 0 crossing
        remainder = distance % 100
        
        if direction == 'R':
            # Moving UP (e.g. 95 -> 0 -> 5)
            # If current pos + steps >= 100, we crossed 0
            if position + remainder >= 100:
                total_zero_touches += 1
            
            # Update position
            position = (position + distance) % 100
            
        elif direction == 'L':
            # Moving DOWN (e.g. 5 -> 0 -> 95)
            # We touch 0 if the remainder is greater than or equal to current position
            # UNLESS we are already at 0 (moving left from 0 doesn't touch 0 immediately, it goes to 99)
            if position != 0 and remainder >= position:
                total_zero_touches += 1
            
            # Update position
            position = (position - distance) % 100

    return total_zero_touches

# print(solve_safe_password_touches('yourfile.txt'))


print(f"The password is: {answer_one('input.txt')}")

print(f"The password is: {answer_two('input.txt')}")
