import pandas as pd
import pickle
import os
from Route import Route
from pprint import pprint
import plotly.express as px
from pprint import pprint
from Route import hours
from utils import hist_opr_time
from main import num_to_let


CACHE_FILE = 'cache3.pkl'


routes = {}
if os.path.getsize(CACHE_FILE) > 0:
    with open(CACHE_FILE, 'rb') as f:
        routes = pickle.load(f)


org_routes = []
for name, persons in routes.items() :
    r = Route(name, persons)
    org_routes.append(r)
all_pers = sum([i.persons for i in org_routes], [])
all_route = Route('all', all_pers)







#
# df = pd.DataFrame(dict(
#     month = [i for i in all_route.persons],
#     hours = every_by_month.values()
# ))
# fig = px.scatter(df, x='month', y='hours', title='Среднее время выполнения процесса по месяцам', trendline='ols')
# fig.show()