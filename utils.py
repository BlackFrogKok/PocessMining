
import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import timedelta
import plotly.express as px




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

abc = 'ABCDEFGHIJKLMNOP'
OPRS_LETTERS = {}
for i in zip(OPRS.values(), list(abc)):
    OPRS_LETTERS[i[0]] = i[1]


def num_to_let(route_name):
    return '_'.join([OPRS_LETTERS[i] for i in route_name.split('_')])


def hist_pers_distrib_routes(routes, write=False):
    df = pd.DataFrame(dict(
        routes = [num_to_let(i.route) for i in routes],
        count = [len(i.persons) for i in routes]
    ))
    fig = px.histogram(df, x="routes", y="count", title='Распределение клиентов по путям')
    if write:
        fig.write_image('Распределение клиентов по путям.png')
    fig.show()

# def hist_opr_aver(route):
#     df = pd.DataFrame(dict(
#         operation = route.opr_time.keys(),
#         fraction = route.fraction.values()
#     ))
#     fig = px.histogram(df, x="operation", y="fraction")
#
#     fig.show()


def calc_sigma(route, opr):
    S_sq = sum([i ** 2 for i in route.dev_opr[opr]]) / (len(route.dev_opr[opr]) - 1)
    E = sum(route.avr_opr[opr]) / len(route.avr_opr[opr])
    return (S_sq ** 0.5) / E


def my_norm(sigma1, sigma2, opr, mu=0, write=False):
    x_range1 = np.linspace(-20 * sigma1 ** 0.5, 20 * sigma1 ** 0.5, 3000)
    y_pdf1 = norm.pdf(x_range1, mu, sigma1)

    df1 = pd.DataFrame({'x': x_range1, 'y': y_pdf1, 'distribution': 'all'})

    x_range2 = np.linspace(-20 * sigma2 ** 0.5, 20 * sigma2 ** 0.5, 3000)
    y_pdf2 = norm.pdf(x_range2, mu, sigma2)

    df2 = pd.DataFrame({'x': x_range2, 'y': y_pdf2, 'distribution': opr})
    df = pd.concat([df1, df2], ignore_index=True)

    fig = px.line(
        df,
        x='x',
        y='y',
        color='distribution',
        title=f'Кластер операций {opr} классифицируется как ручная работа',
        labels={'x': 'Значение', 'y': 'Плотность вероятности'}
    )
    fig.update_yaxes(range=[0, 0.02])
    fig.show()
    if write:
        fig.write_image('Распределение времени выполнения.png')
#
# def hist_opr_prob(org_routes):
#     prob = {}
#     all_pers = sum([len(i.persons) for i in org_routes])
#     for opr in OPRS.values():
#         amount_cur_opr = 0
#         for route in org_routes:
#             if opr in route.route:
#                 amount_cur_opr += len(route.persons)
#         prob[opr] = amount_cur_opr / all_pers
#
#
#     df = pd.DataFrame(dict(
#         operation=[num_to_let(i) for i in prob.keys()],
#         probability=[i for i in prob.values()]
#     ))
#     fig = px.histogram(df, x="operation", y="probability", title='Вероятность возникновения операции в экземпляре процесса')
#     fig.update_layout(
#         yaxis=dict(
#             tickformat=".0%",  # Формат процентов
#         ),
#         showlegend=False
#     )
#     fig.show()
#     fig.write_image('Вероятность возникновения операции в экземпляре процесса.png')

