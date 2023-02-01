import csv
list = []
with open('input.txt',newline='') as f:
    input = csv.reader(f)
    for row in input:
        list.append(row)

input_list = []
for i in list:
    input_list.append(i[0])

counter = 0
for enum,i in enumerate(input_list):
    if enum == 0:
        last = 0
    else:
        last = input_list[enum-1]
        if int(i) > int(last) and  enum != 0:
            counter = counter + 1
        else:
            continue

print('The answer to part one is ' + str(counter))

counter = 0
for enum,i in enumerate(input_list): 
    if enum < 3:
        last = 0
    else:
        last = int(input_list[enum-3]) + int(input_list[enum-2]) + int(input_list[enum-1])
        current = int(input_list[enum-2]) + int(input_list[enum-1]) + int(input_list[enum-0])
        if current > last and  last != 0:
            counter = counter + 1
        else:
            continue

print('The answer to part two is ' + str(counter))
