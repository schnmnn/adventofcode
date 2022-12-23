import pandas as pd

input = pd.read_fwf('day5_input.txt',colspecs=[(0,4),(4,8),(8,12),(12,16),(16,20),(20,24),(24,28),(28,32),(32,36)],names=['stack1','stack2','stack3','stack4','stack5','stack6','stack7','stack8','stack9'])
stacks = input.loc[:7]

moves = pd.read_csv('day5_input.txt',header=None,names=['moves'])
moves = moves.loc[9:]
moves = moves['moves'].str.split(' ',5,expand=True)
moves = moves.rename(columns={0:'move',1:'count_moves',2:'from',3:'from_stack',4:'to',5:'to_stack'})

stacks = stacks.transpose()
stack_list = stacks.values.tolist()

for i in range(len(stack_list)):
    stack_list[i] = stack_list[i][::-1]
    stack_list[i] = [x for x in stack_list[i] if str(x) != 'nan']
    
for i in moves.values:
    for count in range(int(i[1])):
        to_stack = i[5]
        to_stack = int(to_stack)-1
        from_stack = i[3]
        from_stack = int(from_stack)-1
        stack_list[to_stack].append(stack_list[from_stack][-1])
        stack_list[to_stack] = [x for x in stack_list[to_stack] if str(x) != 'nan']
        stack_list[from_stack] = stack_list[from_stack][:-1]
        
answer_1 = []
for i in stack_list:
    answer_1.extend(i[-1][1])
    
print('The answer two part one is ' + str(answer_1))

### Part Two ###

# hier werden nun listen verschoben und damit neue listen erstellt

stack_list_2 = stacks.values.tolist()

for i in range(len(stack_list_2)):
    stack_list_2[i] = stack_list_2[i][::-1]
    stack_list_2[i] = [x for x in stack_list_2[i] if str(x) != 'nan']


for i in moves.values:
    to_stack = i[5]
    to_stack = int(to_stack)-1
    from_stack = i[3]
    from_stack = int(from_stack)-1
    count_crates = int((i[1]))
    stack_list_2[to_stack].extend(stack_list_2[from_stack][-count_crates:])
    stack_list_2[from_stack] = stack_list_2[from_stack][:-count_crates]
    
answer_2 = []
for i in stack_list_2:
    answer_2.extend(i[-1][1])
    
print('The answer two part two is ' + str(answer_2))
