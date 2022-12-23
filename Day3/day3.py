import pandas as pd

input = pd.read_csv('day3_input.txt',header=None)
input = input.set_axis(['rucksack'],axis='columns')
prio_matching = pd.read_csv('prio_matching.csv')

input['half_of_rucksack'] = input['rucksack'].str.len()/2
input['half_of_rucksack'] = input['half_of_rucksack'].astype(int)

input['rucksack_compartment_1'] = input.apply(
    lambda row: row['rucksack'][:row['half_of_rucksack']], 
    axis=1
)

input['rucksack_compartment_2'] = input.apply(
    lambda row: row['rucksack'][row['half_of_rucksack']:], 
    axis=1
)

rucksack_compartment_1_list = input['rucksack_compartment_1'].to_list()
rucksack_compartment_2_list = input['rucksack_compartment_2'].to_list()

len_rucksack = len(rucksack_compartment_1_list)
list_of_wrong_items = []

for count_item_rucksack in range(len_rucksack):
    for list_objekt in rucksack_compartment_1_list[count_item_rucksack]:
        if list_objekt in rucksack_compartment_2_list[count_item_rucksack]:
            a = list_objekt
    list_of_wrong_items.append(a)
            
wrong_items = pd.DataFrame(list_of_wrong_items)
wrong_items = wrong_items.set_axis(['item'],axis='columns')
wrong_items = pd.merge(wrong_items,prio_matching,on='item')
print('The answer to part one is ' + str(wrong_items['priorities'].sum()))


### Part two ###
prio_matching = pd.read_csv('prio_matching.csv')
len_input = len(input)
count1=0
count2=2
all_rucksacks = []
for i in range(0,len_input,3):
    group_of_3 = []
    a = input['rucksack'].loc[count1:count2].astype(str)
    b = a.values.tolist()
    group_of_3.append(b)
    all_rucksacks.append(b)
    count1=count1+3
    count2=count2+3
    
len_all_rucksacks = len(all_rucksacks)

badge=[]
for rucksack in range(len_all_rucksacks):
    one_and_two = []
    one_and_two_and_three=[]
    for i in all_rucksacks[rucksack][0]:
        if i in all_rucksacks[rucksack][1] and i not in one_and_two:
            one_and_two.append(i)
    for i in one_and_two:
        if i in all_rucksacks[rucksack][2] and i not in one_and_two_and_three:
            one_and_two_and_three.append(i)
    badge.append(one_and_two_and_three)

df = pd.DataFrame(badge,columns=['item'])
df_points = pd.merge(df,prio_matching,on='item')
answer_2 = df_points['priorities'].sum()

print('The answer to part two is '+str(answer_2))