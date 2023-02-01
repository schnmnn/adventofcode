import pandas as pd

values_of_choice = pd.read_csv('values_of_choice.txt')
values_of_result = pd.read_csv('values_of_result.txt')
all_possible_results = pd.read_csv('all_possible_results.txt')
input = pd.read_csv('day2_input.txt',header=None,sep=' ')
input = input.set_axis(['opponent','you'],axis='columns')

values_of_choice = values_of_choice[['your_choice_letter','Value_of_letter']]
values_of_choice = values_of_choice.rename(columns={'your_choice_letter':'you'})
your_values_of_choices = pd.merge(input['you'],values_of_choice, on='you')

sum_value_of_choices = your_values_of_choices['Value_of_letter'].sum()
all_possible_results['combined']= all_possible_results['opponent_letter'] + all_possible_results['your_choice_letter']
all_possible_results = pd.merge(all_possible_results,values_of_result,on='Result')
input['combined'] = input['opponent'] + input['you']
sum_result_points = pd.merge(input,all_possible_results,on='combined')
sum_result_points = sum_result_points['Points'].sum()
total_points = sum_value_of_choices + sum_result_points

print('The answer to part on is '+str(total_points))

### Part two ###


meaning_of_letter_part2 = pd.read_csv('meaning_of_letter_part2.txt')
values_of_choicepart2 = pd.read_csv('values_of_choice.txt')
input_part2 = pd.read_csv('day2_input.txt',header=None,sep=' ')
all_possible_results_part2 = pd.read_csv('all_possible_results.txt')
values_of_result_part2 = pd.read_csv('values_of_result.txt')
input_part2 = input_part2.set_axis(['opponents_choice','game_result_letter'],axis='columns')
input_part2 = pd.merge(input_part2,meaning_of_letter_part2,on='game_result_letter')
all_possible_results_part2 = all_possible_results_part2.drop(columns=['opponent_name','your_name'])
all_possible_results_part2 = all_possible_results_part2.rename(columns={'opponent_letter':'opponents_choice','your_choice_letter':'your_choice','Result':'result_name'})
input_part2 = input_part2.drop(columns=('game_result_letter'))
input_join = pd.merge(input_part2,all_possible_results_part2, on= ('opponents_choice','result_name'))
values_of_choicepart2 = values_of_choicepart2[['your_choice_letter','Value_of_letter']]
values_of_choicepart2 = values_of_choicepart2.rename(columns={'your_choice_letter':'your_choice'})
input_join = pd.merge(input_join,values_of_choicepart2,on='your_choice')
values_of_result_part2 = values_of_result_part2.rename(columns={'Result':'result_name'})
input_final = pd.merge(input_join,values_of_result_part2,on='result_name')
answer_2 = input_final['Value_of_letter'].sum() + input_final['Points'].sum()

print('The answer to part two is ' +str(answer_2))