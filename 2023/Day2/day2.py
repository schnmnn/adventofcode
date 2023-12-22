import re
from functools import reduce

with open('input.txt') as file:
    lines = [line.strip() for line in file]


def create_dict_with_all_sets():
    # Initialize an empty dictionary to store color counts
    split_strings = [line.split(';') for line in lines]
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


def get_fewest_color():
    fewest_colors = {}
    nested_dict = create_dict_with_all_sets()[0]
    for items in nested_dict.items():
        for i in items:
            if type(i) != dict:
                id = i
                fewest_colors[id] = {'red':0,'blue':0,'green':0}
            elif type(i) == dict:
                for enum, _ in enumerate(range(len(i))):
                        set_number = f'set{enum+1}'
                        # fewest_colors[id]['red'] = 0
                        # fewest_colors[id]['blue'] = 0
                        # fewest_colors[id]['green'] = 0
                        for k,v in i[set_number].items():
                            if k == 'red' and int(v) > int(fewest_colors[id]['red']):
                                fewest_colors[id]['red'] = v
                            elif k == 'green' and int(v) > int(fewest_colors[id]['green']):
                                fewest_colors[id]['green'] = v
                            elif k == 'blue' and int(v) > int(fewest_colors[id]['blue']):
                                fewest_colors[id]['blue'] = v
    return fewest_colors


def get_multiplied_values():
    list_multiplied_values = []
    fewest_colors = get_fewest_color()
    for k,v in fewest_colors.items():
        counter = 0
        limit = 2
        multiply_list = []
        for k1, v1 in v.items():
            multiply_list.append(v1)
            if counter < limit:
                counter += 1
        result = reduce(lambda x, y: int(x) * int(y), multiply_list)
        list_multiplied_values.append(result)
    return list_multiplied_values

print(f'Answer two is {sum(get_multiplied_values())}')