
import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import timedelta
import plotly.express as px






# def hist_opr_aver(route):
#     df = pd.DataFrame(dict(
#         operation = route.opr_time.keys(),
#         fraction = route.fraction.values()
#     ))
#     fig = px.histogram(df, x="operation", y="fraction")
#
#     fig.show()



# def my_norm(mu, sigma1, sigma2):
#     x_range1 = np.linspace(-20 * sigma1 ** 0.5, 20 * sigma1 ** 0.5, 3000)
#     y_pdf1 = norm.pdf(x_range1, mu, sigma1)
#
#     df1 = pd.DataFrame({'x': x_range1, 'y': y_pdf1, 'distribution': 'all'})
#
#     x_range2 = np.linspace(-20 * sigma2 ** 0.5, 20 * sigma2 ** 0.5, 3000)
#     y_pdf2 = norm.pdf(x_range2, mu, sigma2)
#
#     df2 = pd.DataFrame({'x': x_range2, 'y': y_pdf2, 'distribution': 'ABD'})
#     df = pd.concat([df1, df2], ignore_index=True)
#
#     fig = px.line(
#         df,
#         x='x',
#         y='y',
#         color='distribution',
#         title='Кластер операций ABD классифицируется как ручная работа',
#         labels={'x': 'Значение', 'y': 'Плотность вероятности'}
#     )
#     fig.update_yaxes(range=[0, 0.02])
#
#     fig.write_image('Распределение времени выполнения.png')
#     fig.show()
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

