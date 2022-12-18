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
print(wrong_items['priorities'].sum())