import pandas as pd
import pickle
import os
from Route import Route
from pprint import pprint
import plotly.express as px


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
               8: [3, 4],
               10: [3, 4, 5]
               }



ineff = {}
for k, v in inef_routes.items():
    times = org_routes[k].calc_cycle_ineff_time_route(v)

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

# pprint(cost_by_month)
# cycle_inef_cost = [0, 0, 0]
# print('                      минуты    с учётом инфляции  алтернативные издержки')
# for k, v in cost_by_month.items():
#     cycle_inef_cost[0] += sum([i[0] for i in v.values()]) * 60
#     cycle_inef_cost[1] += sum([i[1] for i in v.values()]) * 60
#     cycle_inef_cost[2] += cost_by_month[k]['2025.02'][2] * 60
#
#     print(f'{k}: {sum([i[0] for i in v.values()]) * 60} {sum([i[1] for i in v.values()]) * 60} {cost_by_month[k]['2025.02'][2] * 60}')
# # print(*cycle_inef_cost)


#график фин неэфф для циклических маршрутов
# for i in cost_by_month.keys():
#     df = pd.DataFrame(dict(
#         months=cost_by_month[i].keys(),
#         cost=[v[0] for v in cost_by_month[i].values()],
#         cost_infl=[v[1] for v in cost_by_month[i].values()]
#     ))
#     fig = px.line(df, x='months', y=['cost', 'cost_infl'], title=f'Стоимость работника индексируется на ИПЦ',)
#     fig.update_layout(font=dict(size=15), title_font=dict(size=17))
#     fig.show()
#     fig.write_image(f'Стоимость работника по месяцам будет больше с учётом инфляции {i}.png', scale=4)


# 0_1_4_300_343_5_8_9

inef_rare = org_routes[8].calc_cycle_ineff_time_route([4])
# pprint(inef_rare)
cost_by_month_rare = calc_empl_cost(inef_rare, infl=True)
# pprint(cost_by_month_rare)

