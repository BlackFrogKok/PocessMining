import pandas as pd
import pickle
import os
from Route import Route


def sample_by_month(route):
    groups = {}
    for person in route.persons:
        time = person.time_start.month + person.time_start.year
        if time in groups:
            groups[time].append(person)
        else:
            groups[time] = [person]
    return groups


def clac_ineff_time_person(person, opers_to_calc):
    inefficiency = 0
    for i in opers_to_calc:
        inefficiency += person.operations[i].time
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


# Циклические пути:
# 0:
