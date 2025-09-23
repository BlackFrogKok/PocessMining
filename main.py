import pickle
import pandas as pd
import os
import numpy as np
from scipy.stats import norm
from datetime import timedelta
from puti import Person
from statistics import median
from Route import Route
import plotly.express as px
from Route import hours

abc = 'ABCDEFGHIJKLMNOP'
OPRS = {'Регистрация претензии': '0',
        'Проверка документов': '1',
        'Поиск потерянной документации': '2',
        'Урегулирование претензии': '4',
        'Утверждение претензии': '5',
        'Ремонт автомобиля': '6',
        'Подготовка итоговой документации': '7',
        'Закрытие страхового случая': '8',
        'Обзор произошедшего случая': '9',
        'Проверка на мошенничество': '12',
        'Урегулирование объёма убытков': '58',
        'Получение страховых резервов': '60',
        'Отправка платежа': '61',
        'Получение права на предъявление претензий от страхователя': '111',
        'Отклонение претензии': '300',
        'Предъявление апелляции по претензии': '343'}
OPRS_LETTERS = {}
for i in zip(OPRS.values(), list(abc)):
    OPRS_LETTERS[i[0]] = i[1]


def num_to_let(route_name):
    return '_'.join([OPRS_LETTERS[i] for i in route_name.split('_')])

def my_norm(mu, sigma1, sigma2):
    x_range1 = np.linspace(-20 * sigma1 ** 0.5, 20 * sigma1 ** 0.5, 3000)
    y_pdf1 = norm.pdf(x_range1, mu, sigma1)

    df1 = pd.DataFrame({'x': x_range1, 'y': y_pdf1, 'distribution': 'all'})

    x_range2 = np.linspace(-20 * sigma2 ** 0.5, 20 * sigma2 ** 0.5, 3000)
    y_pdf2 = norm.pdf(x_range2, mu, sigma2)

    df2 = pd.DataFrame({'x': x_range2, 'y': y_pdf2, 'distribution': 'ABD'})
    df = pd.concat([df1, df2], ignore_index=True)

    fig = px.line(
        df,
        x='x',
        y='y',
        color='distribution',
        title='Кластер операций ABD классифицируется как ручная работа',
        labels={'x': 'Значение', 'y': 'Плотность вероятности'}
    )
    fig.update_yaxes(range=[0, 0.02])

    fig.write_image('Распределение времени выполнения.png')
    fig.show()

def hist_opr_prob(org_routes):
    prob = {}
    all_pers = sum([len(i.persons) for i in org_routes])
    for opr in OPRS.values():
        amount_cur_opr = 0
        for route in org_routes:
            if opr in route.route:
                amount_cur_opr += len(route.persons)
        prob[opr] = amount_cur_opr / all_pers


    df = pd.DataFrame(dict(
        operation=[num_to_let(i) for i in prob.keys()],
        probability=[i for i in prob.values()]
    ))
    fig = px.histogram(df, x="operation", y="probability", title='Вероятность возникновения операции в экземпляре процесса')
    fig.update_layout(
        yaxis=dict(
            tickformat=".0%",  # Формат процентов
        ),
        showlegend=False
    )
    fig.show()
    fig.write_image('Вероятность возникновения операции в экземпляре процесса.png')


def hist_freq(route, opr):
    df = pd.DataFrame(dict(
        hours = route.opr_time[opr]
        # time = route.fraction

    ))

    fig = px.histogram(df, x='hours', nbins=40, title=f'Время операции {OPRS_LETTERS[opr]} непостоянно')
    fig.show()
    fig.write_image(f'Время операции {OPRS_LETTERS[opr]} непостоянно.png')


def hist_opr_aver(route):

    df = pd.DataFrame(dict(
        operation = route.opr_time.keys(),
        fraction = route.fraction.values()
    ))
    fig = px.histogram(df, x="operation", y="fraction")

    fig.show()



CACHE_FILE = 'cache.pkl'
raw_data = pd.read_csv('case_championship_last.csv')
events = raw_data['Событие'].drop_duplicates().to_dict()
events['4+1'] = 'Ебаная хуйня'
events_list = (raw_data['Событие'].drop_duplicates().to_list())
mests = raw_data['Место происшествия'].drop_duplicates().to_list()


routes = {}
if os.path.getsize(CACHE_FILE) > 0:
    with open(CACHE_FILE, 'rb') as f:
        routes = pickle.load(f)



org_routes = []
long_opr = []

all_pers = []

for i in routes.values():
    all_pers += i

for name, persons in routes.items() :
    r = Route(name, persons)
    org_routes.append(r)


# ofice = Route('ofice', all_pers.copy(), lambda x: x.chanel == 'Офис')
# online = Route('online', all_pers.copy(), lambda x: x.chanel == 'Сайт')
# telephone = Route('telephone', all_pers.copy(), lambda x: x.chanel == 'Телефон')
# email = Route('email', all_pers.copy(), lambda x: x.chanel == 'Электронная почта')
all_routes = Route('all', all_pers.copy())

correct_routes = Route('correct', all_pers.copy(), lambda x: '_'.join(x.route_names) == '0_1_4_5_6_7_8_9' or '_'.join(x.route_names) == '0_1_4_5_111_6_7_8_9' or '_'.join(x.route_names) == '0_1_4_58_5_60_61_8_9' or '_'.join(x.route_names) == '0_1_4_300_343_5_8_9' or '_'.join(x.route_names) == '0_1_12_4_5_6_7_8_9', obedinenie=True)

r1 = Route('correct', all_pers.copy(), lambda x: '_'.join(x.route_names) == '0_1_4_5_6_7_8_9')
r2 = Route('correct', all_pers.copy(), lambda x: '_'.join(x.route_names) == '0_1_4_5_111_6_7_8_9')
r3 = Route('correct', all_pers.copy(), lambda x: '_'.join(x.route_names) == '0_1_4_58_5_60_61_8_9')
r4 = Route('correct', all_pers.copy(), lambda x: '_'.join(x.route_names) == '0_1_4_300_343_5_8_9')
r5 = Route('correct', all_pers.copy(), lambda x: '_'.join(x.route_names) == '0_1_12_4_5_6_7_8_9')

huiny = 0

for i in [r1, r2, r3, r4, r5]:
    summ_2 = 0
    for j in i.persons[0].route_names:
        if j == '0' or j == '1' or j == '4' or j == '5' or j == '9':
            continue

        summ_5 = 0
        for l in i.dev_opr[j]:
            summ_5 += (l/i.avr_opr[j])**2
        summ_2 += (summ_5/(len(i.dev_opr[j]) - 1))
    huiny += (summ_2 / (len(i.persons[0].route_names) - 5))

ll = (huiny/5)




#hist_opr_prob(org_routes)
summ=0
for i in correct_routes.dev_opr['4+1']:
    summ += (i/correct_routes.avr_opr['4+1'])**2

kkk = (summ / (len(correct_routes.dev_opr['4+1'])-1))



print((kkk + ll) / 2)
print(kkk)



# 0 1 6 10
cycle_routes = [org_routes[0], org_routes[1], org_routes[6], org_routes[10]]




# fig = px.histogram(x=all_routes.opr_time['4'], histnorm='probability density')
#
# fig.show()
example_route = Route(org_routes[2].route, org_routes[2].persons, obedinenie=True)
print(example_route)


sigma14 = sum(list(map(abs, example_route.dev_opr['4+1']))) / len(list(map(abs, example_route.dev_opr['4+1'])))
not_41 = []

for k, v in example_route.dev_opr.items():
    if k != '4+1':
        not_41 += v
sigma_other = sum(map(abs, not_41)) / len(not_41)

print(sigma14)
print(sigma_other)
my_norm(0,sigma14 ** 2, ((sigma14 + sigma_other) / 2) ** 2)
print(num_to_let('0_1_4'))








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


# df = pd.DataFrame(dict(
#     routes = [num_to_let(i.route) for i in org_routes],
#     count = [len(i.persons) for i in org_routes]
# ))
# fig = px.histogram(df, x="routes", y="count", title='Распределение клиентов по путям')
# fig.write_image('Распределение клиентов по путям.png')

# hist_freq(all_routes, '4')
# hist_freq(all_routes, '1')
# hist_freq(all_routes, '0')
# hist_freq(all_routes, '5')


# my_norm(0, 0.042, 0.14)

# 4 1 0 5

