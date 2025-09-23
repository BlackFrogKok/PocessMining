import pandas as pd
import pickle
import os
from Route import Route
from pprint import pprint
import plotly.express as px



def sample_by_month(route):
    groups = {}
    for person in route.persons:
        # print(person.time_start.month)
        # print(person.time_start.year)
        # print('------------------')
        if person.time_start.month > 9:
            time = str(person.time_start.year)+ '.' + str(person.time_start.month)
        else:
            time = str(person.time_start.year) + '.0' + str(person.time_start.month)

        if time in groups:
            groups[time].append(person)
        else:
            groups[time] = [person]
    return groups


def clac_ineff_time_person(person, opers_to_calc):
    inefficiency = 0
    opers = list(person.operations.keys())

    for i in opers_to_calc:
        inefficiency += person.operations[opers[i]].time
    return inefficiency


def calc_ineff_time_route(route, opers_to_calc):
    inefficiency_by_month = {}
    groups = sample_by_month(route)
    for time, persons in groups.items():
        inefficiency = 0
        for person in persons:
            inefficiency += clac_ineff_time_person(person, opers_to_calc)
        inefficiency_by_month[time] = inefficiency
    return inefficiency_by_month


def calc_empl_cost(inefficiency_by_month, infl=False):
    start_cost = 1
    start_cost_infl = 1
    alter_cost = 0
    cost_by_month = {}
    for time, inefficiency in inefficiency_by_month.items():
        if infl:
            start_cost_infl = start_cost_infl * (1 + INFLATION[time] / 100)

            alter_cost = (alter_cost + inefficiency * start_cost_infl) * (1 + INTEREST_RATE[time] / 100)
            cost_by_month[time] = (start_cost * inefficiency, inefficiency * start_cost_infl, alter_cost)
        else:
            cost_by_month[time] = inefficiency * start_cost

    return cost_by_month


CACHE_FILE = 'cache3.pkl'
raw_data = pd.read_csv('case_championship_last.csv')
events = raw_data['Событие'].drop_duplicates().to_dict()
events_list = (raw_data['Событие'].drop_duplicates().to_list())
mests = raw_data['Место происшествия'].drop_duplicates().to_list()

routes = {}
if os.path.getsize(CACHE_FILE) > 0:
    with open(CACHE_FILE, 'rb') as f:
        routes = pickle.load(f)


org_routes = []
for name, persons in routes.items() :
    r = Route(name, persons)
    org_routes.append(r)


inef_routes = {0: [1],
               1: [3],
               6: [1, 2, 3],
               10: [3, 4, 5]}



ineff = {}
for k, v in inef_routes.items():
    times = calc_ineff_time_route(org_routes[k], v)

    ineff[org_routes[k].route] = dict(sorted(times.items(), key=lambda item: tuple(map(int, item[0].split('.')))))


# for k, v in ineff.items():
#     print(f'{k}: {sum(v.values())}')

inflation_sourse = {
    '2023': '0.84   0.46	0.37	0.38	0.31	0.37	0.63	0.28	0.87	0.83	1.11	0.73',
    '2024': '0.86	0.68	0.39	0.50	0.74	0.64	1.14	0.20	0.48	0.75	1.43	1.32',
    '2025': "1.23	0.81"
}
INFLATION = {}
for k, v in inflation_sourse.items():
    inflation_month = v.split()
    for i in range(12):
        if k == '2025' and i > 1:
            break
        INFLATION[k + '.' + str(i + 1).zfill(2)] = float(inflation_month[i])

mec_25 = {1-2:1.2887982604601167}
INTEREST_RATE = {
 '2023.02': 1.182828477493573,
 '2023.03': 1.182828477493573,
 '2023.04': 1.182828477493573,
 '2023.05': 1.182828477493573,
 '2023.06': 1.182828477493573,
 '2023.07': 1.182828477493573,
 '2023.08': 1.195230252761303,
 '2023.09': 1.2300755055779713,
 '2023.10': 1.2383078119015432,
 '2023.11': 1.2531631188616348,
 '2023.12': 1.2599210498948732,
 '2024.01': 1.2599210498948732,
 '2024.02': 1.2599210498948732,
 '2024.03': 1.2599210498948732,
 '2024.04': 1.2599210498948732,
 '2024.05': 1.2599210498948732,
 '2024.06': 1.2599210498948732,
 '2024.07': 1.2599210498948732,
 '2024.08': 1.272348382661198,
 '2024.09': 1.272348382661198,
 '2024.10': 1.272348382661198,
 '2024.11': 1.2887982604601167,
 '2024.12': 1.2887982604601167,
 '2025.01': 1.2887982604601167,
 '2025.02': 1.2887982604601167}



cost_by_month = {}


for k, v in ineff.items():
    cost_by_month[k] = calc_empl_cost(v, infl=True)

pprint(cost_by_month)
for k, v in cost_by_month.items():
    print(f'{k}: {sum([i[0] for i in v.values()])} {sum([i[1] for i in v.values()])} {cost_by_month[k]['2025.02'][2]}')



df = pd.DataFrame(dict(
    months=cost_by_month['0_1_2_1_4_5_6_7_8_9'].keys(),
    cost=[v[0] for v in cost_by_month['0_1_2_1_4_5_6_7_8_9'].values()],
    cost_infl=[v[1] for v in cost_by_month['0_1_2_1_4_5_6_7_8_9'].values()]
))
fig = px.line(df, x='months', y=['cost', 'cost_infl'], title='Стоимость работника по месяцам будет больше с учётом инфляции')
fig.update_layout(font=dict(size=15), title_font=dict(size=17))
# fig.show()
# fig.write_image('Стоимость работника по месяцам будет больше с учётом инфляции.png', scale=4)



