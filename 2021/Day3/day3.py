import csv
list = []
with open('input.txt',newline='') as f:
    input = csv.reader(f)
    for row in input:
        list.append(row)

lists = [[]for i in range(0,len(list[0][0]))]

for enum, i in enumerate(lists):
    for x in list:
        lists[enum].append(x[0][enum])

list_new_binary_number_most_common = []
list_new_binary_number_least_common = []

for enum, i in enumerate(lists):
    counter_1 = 0
    counter_0 = 0
    for x in i:
        if x == '1':
            counter_1 +=1
        elif x == '0':
            counter_0 += 1
    if counter_1 > counter_0:
        list_new_binary_number_most_common.append(1)
        list_new_binary_number_least_common.append(0)
    elif counter_1 < counter_0:
        list_new_binary_number_most_common.append(0)
        list_new_binary_number_least_common.append(1)

gamma_rate = ''
epsilon_rate = ''
for i in list_new_binary_number_most_common:
    gamma_rate += ''+ str(i)

for i in list_new_binary_number_least_common:
    epsilon_rate += ''+ str(i)


print('The answer to part one is ' + str(int(gamma_rate,2) * int(epsilon_rate,2)))