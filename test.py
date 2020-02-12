import requests as r
import random as rand
import time
import os

os.environ['NO_PROXY'] = '127.0.0.1'
i = 0
while 1:
    time.sleep(1)
    data = {'time': i, 'command': rand.uniform(-1, 1)}
    r.post('http://127.0.0.1:5000/graph/plot', json=data)
    i += 1