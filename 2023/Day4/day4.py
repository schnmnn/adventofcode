import re

with open('input.txt') as file:
    lines = [line.strip() for line in file]

def create_dict():
    game_dict = {}
    for i in lines:
        # Search for the pattern
            match = re.search(r'Card\D*(\d+):', i)
            if match:
                # Extract the digit
                game = match.group(1)
                game_dict[game] = {'winning_number':0,'numbers':0}
    return game_dict

def assign_values():
    game_dict = create_dict()
    for i in lines:
    # Search for the pattern
        match = re.search(r'Card\D*(\d+):', i)
        if match:
            # Extract the digit
            game = match.group(1)
        # Search for the pattern
        match = re.search(r':([^|]+)\|', i)
        if match:
            # Extract the text
            winning_numbers = match.group(1)
            game_dict[game]['winning_number'] = winning_numbers.strip().split(' ')
        # Search for the pattern
        match = re.search(r'\|(.*?)$', i)
        if match:
            # Extract the text
            numbers = match.group(1)
            game_dict[game]['numbers'] = numbers.strip().split(' ')
    return game_dict

def delete_empty_strings():
    game_dict = assign_values() 
    for k,v in game_dict.items():
        v['winning_number'] = [i for i in v['winning_number'] if i != '']
        v['numbers'] = [i for i in v['numbers'] if i != '']
    return game_dict


def calc_correct_numbers():
    correct_numbers = []
    for k,v in delete_empty_strings().items():
        set_winning_number = set(v['winning_number'])
        set_number = set(v['numbers'])
        # Find common elements
        common_elements = set_winning_number.intersection(set_number)
        correct_numbers.append(len(common_elements)) 
    return correct_numbers

def calc_points():
    sum_points = []
    for i in calc_correct_numbers():
        counter = 1
        if i > 0:
            point = 1
            #print(i)
            while  counter < i:
                counter = counter + 1
                point = point + point
            sum_points.append(point)
    return sum_points

print(f'Answer one is {sum(calc_points())}')