import pandas as pd
import re

df = pd.read_csv('day1input.txt',header=None)

def find_all_digits(df,column_name):
    df['numbers'] = df[column_name].str.findall('\d+')
    df['concatenated'] = df['numbers'].apply(lambda x: ' '.join(x))
    df['concatenated'] = df['concatenated'].str.replace(r'\s+', '', regex=True)
    df['first_last'] = df['concatenated'].apply(
        lambda x: x[0] + x[-1]
        if len (x) >= 2 else x + x)
    df['first_last'] = df['first_last'].astype(int)
    df.drop(columns=['numbers','concatenated'])
    return df


def answerone(df,column_name):
    df_one = find_all_digits(df,column_name)
    answer = df_one['first_last'].sum()
    return print(f'Answer one is {answer}')


def convert(df):

    df['new'] = df[0].apply(lambda x: re.sub('eightwo', '82', x))
    df['new'] = df['new'].apply(lambda x: re.sub('oneight', '18', x))
    df['new'] = df['new'].apply(lambda x: re.sub('threeight', '38', x))
    df['new'] = df['new'].apply(lambda x: re.sub('fiveight', '58', x))
    df['new'] = df['new'].apply(lambda x: re.sub('senvenine', '79', x))
    df['new'] = df['new'].apply(lambda x: re.sub('twone', '21', x))

    df['new'] = df['new'].apply(lambda x: re.sub('one', '1', x))
    df['new'] = df['new'].apply(lambda x: re.sub('two', '2', x))
    df['new'] = df['new'].apply(lambda x: re.sub('three', '3', x))
    df['new'] = df['new'].apply(lambda x: re.sub('four', '4', x))
    df['new'] = df['new'].apply(lambda x: re.sub('five', '5', x))
    df['new'] = df['new'].apply(lambda x: re.sub('six', '6', x))
    df['new'] = df['new'].apply(lambda x: re.sub('seven', '7', x))
    df['new'] = df['new'].apply(lambda x: re.sub('eight', '8', x))
    df['new'] = df['new'].apply(lambda x: re.sub('nine', '9', x))
    return df

def answertwo(df,column_name):
    df_two = convert(df)
    df_two = find_all_digits(df_two,column_name)

    answer = df_two['first_last'].sum()
    return print(f'Answer two is {answer}')

answerone(df,0)
answertwo(df,'new')
