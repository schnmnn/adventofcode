import csv
list = []
with open('input.txt',newline='') as f:
    input = csv.reader(f)
    for row in input:
        list.append(row)

direction_list = []
move_value_list = []
for i in list:
    split_text = i[0].split(" ")
    direction_list.append(split_text[0])
    move_value_list.append(split_text[1])

horizontal_value = 0
depth = 0

for enum,i in enumerate(direction_list):
    if i == 'forward':
        forward_value = int(move_value_list[enum])
        horizontal_value += forward_value
    elif i == 'up':
        depth_value = int(move_value_list[enum])
        depth -= depth_value
    elif i == 'down':
        depth_value = int(move_value_list[enum])
        depth += depth_value

print("The answer the part one is " + str(horizontal_value * depth)) 

horizontal_value = 0
depth = 0
aim = 0

for enum,i in enumerate(direction_list):
    if i == 'forward':
        forward_value = int(move_value_list[enum])
        horizontal_value += forward_value
        depth = depth + (aim * forward_value)
        if aim ==0:
            continue
        else:
            depth_value = aim * forward_value
    elif i == 'up':
        value = int(move_value_list[enum])
        aim -= value
    elif i == 'down':
        value = int(move_value_list[enum])
        aim += value

print("The answer the part two is " + str(horizontal_value * depth)) 
