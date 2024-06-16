import pandas as pd


def get_priority(unom_list):
    df = pd.read_csv(r'C:\Users\Степан\Documents\хакатон\data\merged_priority_data.csv')
    filtered_df = df[df['UNOM'].isin(unom_list)]

    unom_type_dict = dict(zip(filtered_df['UNOM'], filtered_df['Тип Назначение']))

    return unom_type_dict


print(get_priority([18777, 2105327]))