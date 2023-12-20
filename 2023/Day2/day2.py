import re

with open('input.txt') as file:
    lines = [line.strip() for line in file]


def create_dict_with_all_sets():
    # Initialize an empty dictionary to store color counts
    split_strings = [line.split(';') for line in lines]
    color_counts = {}
    game_ids = []
    pattern = r"Game (\d+):"
    nested_dict = {}
    # Process each sublist
    for sublist in split_strings:
        for enum,s in enumerate(sublist):
            set_number = enum+1
            if re.search(pattern, s) != None:
                id = re.search(pattern, s).group(1)
                game_ids.append(re.search(pattern, s).group(1))
                s = re.sub(pattern, '', s)
                nested_dict[id] = {}
                nested_dict[id][f'set{enum+1}'] = {}
            else:
                1==1
                #continue
                nested_dict[id][f'set{enum+1}'] = {}

            # Split by comma to get each color-number pair
            pairs = s.split(',')
            for enum,pair in  enumerate(pairs):
                # Split by space to separate number and color
                parts = pair.strip().split(' ')
                if parts[1] == 'red':
                    nested_dict[id][f'set{set_number}']['red'] = parts[0]
                elif parts[1] == 'green':
                    nested_dict[id][f'set{set_number}']['green'] = parts[0]
                elif parts[1] == 'blue':
                    nested_dict[id][f'set{set_number}']['blue'] = parts[0]
                else:
                    continue
    return nested_dict, game_ids

def get_games_not_possible():
    game_ids_not_possible = []
    nested_dict = create_dict_with_all_sets()[0]
    for items in nested_dict.items():
        for i in items:
            if type(i) != dict:
                id = i
                #print(id)
            elif type(i) == dict:
                for enum, _ in enumerate(range(len(i))):
                    set_number = f'set{enum+1}'
                    #print(i[set_number])
                    for k,v in i[set_number].items():
                        if k == 'red' and int(v) > 12:
                            if id not in game_ids_not_possible:
                                game_ids_not_possible.append(id)
                            else:
                                continue
                        elif k == 'green' and int(v) > 13:
                            if id not in game_ids_not_possible:
                                game_ids_not_possible.append(id)
                        elif k == 'blue' and int(v) > 14:
                            if id not in game_ids_not_possible:
                                game_ids_not_possible.append(id)
    return game_ids_not_possible


def calculate_possible_games():
    game_ids = create_dict_with_all_sets()[1]    
    no_games = get_games_not_possible()
    sum_all = 0
    sum_not_possible = 0

    for i in game_ids:
        sum_all += int(i)

    for i in no_games:
        sum_not_possible += int(i)

    return sum_all - sum_not_possible

print(f'Answer one is {calculate_possible_games()}')
