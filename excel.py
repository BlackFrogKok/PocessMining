import os
import pickle
from datetime import timedelta

from Route import Route, hours

CACHE_FILE = 'cache3.pkl'

routes = {}
if os.path.getsize(CACHE_FILE) > 0:
    with open(CACHE_FILE, 'rb') as f:
        routes = pickle.load(f)

all_pers = []

for i in routes.values():
    all_pers += i

for i in range(1,13):
    all_routes = Route('all', all_pers.copy(), lambda x: x.time_start.month == i)
    all_pers = [j.time_vipol for j in all_routes.persons]
    print(f'{i};{hours(sum(all_pers, timedelta()))}/{len(all_pers)}')


