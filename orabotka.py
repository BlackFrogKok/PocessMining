from tqdm import tqdm
import pickle
import pandas as pd
from datetime import datetime as dt

from puti import Person

CACHE_FILE = 'cache2.pkl'

raw_data = pd.read_csv('case_championship_last.csv')
sobitia = {v:str(k) for k, v in raw_data['Событие'].drop_duplicates().to_dict().items()}
raw_data = raw_data.replace(sobitia)
putis = {}

for j in tqdm(raw_data['ID'].drop_duplicates()):
    filtered_df = raw_data[raw_data['ID'] == j]
    filtered_df = filtered_df.sort_values(by=['Время'])

    route = filtered_df['Событие'].to_list()
    puti = '_'.join(route)

    opr_time = {}
    opr_start_date= {}
    for i in range(len(route) - 1):
        if route[i] in opr_time:
            opr_time[route[i]].append(dt.fromisoformat(filtered_df.iloc[i+1]['Время']) - dt.fromisoformat(filtered_df.iloc[i]['Время']))
            opr_start_date[route[i]].append(dt.fromisoformat(filtered_df.iloc[i]['Время']))

        else:
            opr_time[route[i]] = [dt.fromisoformat(filtered_df.iloc[i+1]['Время']) - dt.fromisoformat(filtered_df.iloc[i]['Время'])]
            opr_start_date[route[i]] = [dt.fromisoformat(filtered_df.iloc[i]['Время'])]


    person = Person(route,
                    dt.fromisoformat(filtered_df.iloc[0]['Время']),
                    dt.fromisoformat(filtered_df.iloc[-1]['Время']),
                    opr_time,
                    opr_start_date,
                    filtered_df.iloc[0]['Канал'],
                    filtered_df.iloc[0]['Тип страхового случая'],
                    filtered_df.iloc[0]['Тип повреждения'],
                    filtered_df.iloc[0]['Место происшествия'],
                    filtered_df.iloc[0]['Сумма ущерба'],
                    filtered_df.iloc[0]['Оценка удовлетворённости клиента']
                    )

    if puti in putis:
        putis[puti].append(person)
    else:
        putis[puti] = [person]

with open(CACHE_FILE, 'wb') as f:
    pickle.dump(putis, f)
