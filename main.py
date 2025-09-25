import pickle
import pandas as pd
import os
from Route import Route


CACHE_FILE = 'cache3.pkl'
routes = {}
if os.path.getsize(CACHE_FILE) > 0:
    with open(CACHE_FILE, 'rb') as f:
        routes = pickle.load(f)
org_routes = []
all_pers = []
for i in routes.values():
    all_pers += i
for name, persons in routes.items() :
    r = Route(name, persons)
    org_routes.append(r)



# индексы циклических путей: 0 1 6 10


# Количество нарушений SLA всего
all_routes = Route('all', all_pers.copy())
cycle_routes = [org_routes[0], org_routes[1], org_routes[6], org_routes[10]]

sla_fail = 0
for i in all_routes.persons:
    if i.is_over_limit():
        sla_fail += 1
print(f'Всего нарушений SLA: {sla_fail}')

# количество нарушений SLA в циклах
cycle_routes = Route('cycle', [i.persons for i in cycle_routes])
sla_fail_cycles = 0
for i in cycle_routes.persons:
    if i.is_over_limit():
        sla_fail_cycles += 1
print(f'Нарушений SLA в циклах: {sla_fail_cycles}')





# 0 1 6 10





#
# sigma14 = sum(list(map(abs, example_route.dev_opr['4+1']))) / len(list(map(abs, example_route.dev_opr['4+1'])))
# not_41 = []
#
# for k, v in example_route.dev_opr.items():
#     if k != '4+1':
#         not_41 += v
# sigma_other = sum(map(abs, not_41)) / len(not_41)

# print(sigma14)
# print(sigma_other)
# my_norm(0,sigma14 ** 2, ((sigma14 + sigma_other) / 2) ** 2)
# print(num_to_let('0_1_4'))
#
# for i in all_routes.persons:
#     print(i.time_vipol)






# for i in cycle_routes:
#     df = pd.DataFrame(dict(
#         routes = [num_to_let(i.route)],
#         count = [len(i.persons)]
#     ))
#
#     fig = px.histogram(df, x="routes", y="count", title=f'Количество клиентов в зацикленном пути {num_to_let(i.route)}')
#     fig.update_layout(bargap=0.95)
#     # fig.show()
#     fig.write_image(f'Количество клиентов в зацикленном пути {num_to_let(i.route)}.png')


# Совмещение двух графиков
# df = pd.DataFrame(dict(
#     routes = [num_to_let(cycle_routes[0].route), num_to_let(cycle_routes[2].route)],
#     count = [len(cycle_routes[0].persons), len(cycle_routes[2].persons)]
# ))
# fig = px.histogram(df, x="routes", y="count", title=f'Количество клиентов в зацикленном пути 1')
# fig.update_layout(bargap=0.7, font=dict(size=15), title_font=dict(size=14))
# # fig.show()
# fig.write_image(f'Количество клиентов в зацикленном пути 2.png')



# df = pd.DataFrame(dict(
#     routes = [num_to_let(org_routes[7].route), num_to_let(org_routes[9].route)],
#     fraction = [len(i.persons) / len(all_routes.persons) for i in [org_routes[7], org_routes[9]]]
# ))
# fig = px.histogram(df, x="routes", y="fraction", title='Отсутствие ключевой операции')
# fig.update_layout(
#     yaxis=dict(
#         tickformat=".0%",  # Формат процентов
#     ),
#     showlegend=False,
#     bargap=0.8
# )
# fig.show()
# fig.write_image('Отсутствие ключевой операции.png')


# my_norm(0, kkk, (kkk + ll) / 2)

# df = pd.DataFrame(dict(
#     days = [hours(i.time_vipol) / 24 for i in all_routes.persons]
#
# ))
#
# fig = px.histogram(df, x='days', nbins=100, title=f'Часть экземпляров процессов занимает больше двух дней')
# fig.write_image('Распределение экземпляров по времени выполнения.png')






# my_norm(0, 0.042, 0.14)

# 4 1 0 5
