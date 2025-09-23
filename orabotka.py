from tqdm import tqdm
import pickle
import pandas as pd
from Operation import Operation, OprName
from datetime import datetime as dt

from Person import Person

CACHE_FILE = 'cache3.pkl'

raw_data = pd.read_csv('case_championship_last.csv')
sobitia = {v:str(k) for k, v in raw_data['Событие'].drop_duplicates().to_dict().items()}
raw_data = raw_data.replace(sobitia)
putis = {}

for j in tqdm(raw_data['ID'].drop_duplicates()):
    filtered_df = raw_data[raw_data['ID'] == j]
    filtered_df = filtered_df.sort_values(by=['Время'])

    route = filtered_df['Событие'].to_list()
    puti = '_'.join(route)

    operations = {}
    for i in range(len(route) - 1):
        operations[OprName(route[i]).name] = Operation(
            id=OprName(route[i]).name,
            time_start=dt.fromisoformat(filtered_df.iloc[i]['Время']) ,
            time_end=dt.fromisoformat(filtered_df.iloc[i+1]['Время']),
            employee="",
            grade=""
        )

    person = Person(time_start=dt.fromisoformat(filtered_df.iloc[0]['Время']),
                    time_end=dt.fromisoformat(filtered_df.iloc[-1]['Время']),
                    operations=operations,
                    chanel=filtered_df.iloc[0]['Канал'],
                    type_strah=filtered_df.iloc[0]['Тип страхового случая'],
                    damage=filtered_df.iloc[0]['Тип повреждения'],
                    place=filtered_df.iloc[0]['Место происшествия'],
                    summ=filtered_df.iloc[0]['Сумма ущерба'],
                    grade=filtered_df.iloc[0]['Оценка удовлетворённости клиента']
                    )

    if puti in putis:
        putis[puti].append(person)
    else:
        putis[puti] = [person]

with open(CACHE_FILE, 'wb') as f:
    pickle.dump(putis, f)
