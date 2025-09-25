import pandas as pd
import pickle
import os
from Route import Route
from pprint import pprint
import plotly.express as px
from cycle_inefficency import clac_cycle_ineff_time_person, calc_cycle_ineff_time_route, calc_empl_cost
from pprint import pprint
from Route import hours



CACHE_FILE = 'cache3.pkl'


routes = {}
if os.path.getsize(CACHE_FILE) > 0:
    with open(CACHE_FILE, 'rb') as f:
        routes = pickle.load(f)


org_routes = []
for name, persons in routes.items() :
    r = Route(name, persons)
    org_routes.append(r)

ideal_route = org_routes[2]
f = open('dev_ideal_person.txt', 'r')
dev_ideal = [float(i.replace(',', '.')) for i in f.read().splitlines()]
ideal_route_pers = {}
i = 0
for k, v in ideal_route.sample_persons_by_month.items():
    ideal_route_pers[k] = len(v) * dev_ideal[i]
    i+=1

ideal_route_pers = dict(sorted(ideal_route_pers.items(), key=lambda item: tuple(map(int, item[0].split('.')))))

cost = calc_empl_cost(ideal_route_pers, infl=True)
# print(cost)
minutes, cost_empl, alter = 0, 0, cost['2025.02'][2]
for k, v in cost.items():
    minutes += v[0]
    cost_empl += v[1]
# print(minutes * 60, cost_empl * 60, alter * 60)











ideal_route_pers2 = ideal_route.sample_persons_by_month()
for k, v in ideal_route_pers2.items():
    ideal_route_pers2[k] = sum([hours(i.time_vipol) for i in v]) / len(v)

ideal_route_pers2 = dict(sorted(ideal_route_pers2.items(), key=lambda item: tuple(map(int, item[0].split('.')))))


every_by_month = {}
for k in ideal_route_pers2.keys():
    month = k.split('.')[1]
    if month not in every_by_month.keys():
        every_by_month[month] = []



for k, v in ideal_route_pers2.items():
    month = k.split('.')[1]
    every_by_month[month].append(v)

for k, v in every_by_month.items():
    every_by_month[k] = sum(v) / len(v)

# print(every_by_month)
every_by_month = dict(sorted(every_by_month.items(), key=lambda item: int(item[0])))
# for i in every_by_month:
#     print(str(every_by_month[i]).replace('.', ','))


ideal_route_pers_per_month = ideal_route.sample_persons_by_month()
for k, v in ideal_route_pers_per_month.items():
    ideal_route_pers_per_month[k] = len(v)

ideal_route_pers_per_month = dict(sorted(ideal_route_pers_per_month.items(), key=lambda item: tuple(map(int, item[0].split('.')))))
# pprint(ideal_route_pers_per_month)

every_by_month2 = {}
for k, v in ideal_route_pers_per_month.items():
    month = k.split('.')[1]
    if month not in every_by_month2.keys():
        every_by_month2[month] = 0
    else:
        every_by_month2[month] += v


dev = [0.163, 0.0505]
# pprint(ideal_route_pers_per_month)

#
print(f'02: {every_by_month2['02'] * dev[0] * 60}')
print(f'11: {every_by_month2['11'] * dev[1] * 60}')


# df = pd.DataFrame(dict(
#     month = every_by_month.keys(),
#     hours = every_by_month.values()
# ))
# fig = px.scatter(df, x='month', y='hours', title='Среднее время выполнения процесса по месяцам', trendline='ols')
# fig.show()



