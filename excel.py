import os
import pickle
import plotly.express as px
import plotly.graph_objs as go

import pandas as pd
from plotly.graph_objs import Layout

from Route import Route, hours

CACHE_FILE = 'cache3.pkl'

routes = {}
if os.path.getsize(CACHE_FILE) > 0:
    with open(CACHE_FILE, 'rb') as f:
        routes = pickle.load(f)

all_pers = []

for i in routes.values():
    all_pers += i


fig_list = []

for num, year in enumerate([2023, 2024, 2025]):
    x = []
    y = []
    text = []
    count = []
    peoples = []
    for i in range(1, 13):
        all_routes = Route('all', all_pers.copy(), lambda x: x.time_start.month == i
                                                             and "_".join(x.operations.keys()) == 'A_B_D_E_F_G_H'
                                                             and x.time_start.year == year)
        pers_vipol = [hours(person.time_vipol) for person in all_routes.persons]
        people = set([person.operations['E'].employee for person in all_routes.persons])
        peoples += people
        x.append(i)
        try:
            y.append(sum(pers_vipol)/len(pers_vipol))
        except Exception:
            y.append(None)
        count.append(len(pers_vipol))
        text.append(len(pers_vipol))
    print(f'{year}: {len(set(peoples))}')

    fig_list.append(pd.DataFrame(dict(
        x=x,
        y=y,
        text=text,
        year=str(year)
    )))

df = pd.concat(fig_list, ignore_index=True)
fig = px.line(df, x="x", y="y", color='year', text="text" ).update_xaxes(dtick=dict(tick0=1))
fig.show()

# for i in range(len(x)):
#     print(f'{x[i]};{y[i]}'.replace('.', ','))

