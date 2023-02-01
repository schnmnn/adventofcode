import pandas as pd
import numpy as np

input = pd.read_csv('day1input.txt',skip_blank_lines=False,header=None)
input["elf"] = input.isnull().all(axis=1).cumsum()
input = input.set_axis(['calories','group'], axis='columns')
input = input.dropna(0)
input_group = input.groupby(by=['group']).sum()
input_group = input_group.sort_values(by='group')
input_group.insert(loc=0,column='elf',value=(input_group.reset_index().index)+1)
input_group = input_group.sort_values(by='calories',ascending=False,ignore_index=True)
answer_1 = input_group['calories'][0]
print('The answer to part one is ' + str(int(answer_1)))

### part two ###
top_3_elf = input_group[:3]
answer_2 = top_3_elf['calories'].sum()
print('The answer to part two is ' + str(int(answer_2)))
