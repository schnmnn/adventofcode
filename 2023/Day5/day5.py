import pandas as pd

with open('input.txt') as file:
    lines = [line.strip() for line in file]

def create_input_list(lines):

    seeds = []
    for line in lines:
        if 'seeds:' in line:
            seeds.append(line.split(' '))

    for i in seeds:
        for a in i:
            if a.isdigit() != True:
                i.remove(a)

    input_list = [item for sublist in seeds for item in sublist]
    return input_list

input_list = create_input_list(lines)

def create_map_dict(lines):
    map_names = ['seed-to-soil map:','soil-to-fertilizer map:','fertilizer-to-water map:','water-to-light map:','light-to-temperature map:','temperature-to-humidity map:','humidity-to-location map:']
    maps = {}
    current_name = None

    for line in lines:
        line = line.strip()
        if line in map_names:
            current_name = line
            maps[current_name] = []  # Initialize an empty list for this name
        elif current_name is not None:
            # If a name has been encountered, start appending values
            if line == '':
                continue
            else:
                maps[current_name].append(line.split(' '))
    return maps

def get_map_result(input,df):
    df = df
    df['input'] = input

    # create a mapping number if the input is between the source_range_start + the range
    df['map_number'] = df.apply(
    lambda x:
    (int(x['dest_range_start']) - int(x['source_range_start']) ) if (int(x['input']) >= int(x['source_range_start']) ) & (int(x['input']) < (int(x['source_range_start']) + int(x['range'])))
    else 0, axis= 1
    )

    # create an output column according to the map number
    df['output'] = df.apply(
    lambda x:
    (int(x['input']) + int(x['map_number'])) if x['map_number'] != '0'
    else 0,axis = 1
    )

    # find the maximum absolute value of the map_number to extract the correct result
    result = df['output'][df['map_number'].abs() == df['map_number'].abs().max()].iloc[0]

    return result


def create_location_list():
    maps = create_map_dict(lines)
    location_list = []
    for i in input_list:
        current_input = i
        for map in maps:
            df = pd.DataFrame(maps[map],columns=['dest_range_start','source_range_start','range'])
            current_input = (get_map_result(current_input,df))
        location_list.append(current_input)
    return location_list

print(f'Answer on is {min(create_location_list())}')