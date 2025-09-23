import os
import pickle

from Route import Route

CACHE_FILE = 'cache3.pkl'

routes = {}
if os.path.getsize(CACHE_FILE) > 0:
    with open(CACHE_FILE, 'rb') as f:
        routes = pickle.load(f)

all_pers = []

for i in routes.values():
    all_pers += i

for i in range(1,13):
    all_routes = Route('all', all_pers.copy())


