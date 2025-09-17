import pickle
import pandas as pd
import os
from datetime import timedelta
from puti import Person
from statistics import median
from Route import Route
import plotly.express as px


def hist_freq(route):
    df = pd.DataFrame(dict(
        time = route.opr_time[route.max_fraction_opr]
    ))
    bins = 20
    intervals = pd.cut(df['time'], bins)
    result = df.groupby(intervals).size().reset_index(name='counts')
    fig = px.histogram(result, x='time')
    fig.show()


def hist_opr_aver(route):

    df = pd.DataFrame(dict(
        operation = route.opr_time.keys(),
        fraction = route.fraction.values()
    ))
    fig = px.histogram(df, x="operation", y="fraction")

    fig.write_image(f"out/{route.route}.png")


CACHE_FILE = 'cache2.pkl'
raw_data = pd.read_csv('case_championship_last.csv')
events = raw_data['Событие'].drop_duplicates().to_list()

routes = {}
if os.path.getsize(CACHE_FILE) > 0:
    with open(CACHE_FILE, 'rb') as f:
        routes = pickle.load(f)

def hist_freq(route):
    df = pd.DataFrame(dict(
        # time = route.opr_time[route.max_fraction_opr]
        time = route['0']

    ))
    # bins = 20
    # intervals = pd.cut(df['time'], bins)
    # result = df.groupby(intervals).size().reset_index(name='counts')
    # print(result)
    fig = px.histogram(df, x='time', nbins=40)
    fig.show()


org_routes = []
long_opr = []

time_4 = []
sobitia = {v:str(k) for k, v in raw_data['Событие'].drop_duplicates().to_dict().items()}
print(routes.keys())

for name, persons in routes.items() :
    r = Route(name, persons)
    print(r)

