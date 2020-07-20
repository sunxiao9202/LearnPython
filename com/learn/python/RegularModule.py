import hashlib
import itertools
from collections import namedtuple, defaultdict

from contextlib import contextmanager

import requests

r = requests.get(
    'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=json')

print(r.json())

@contextmanager
def tag(name):
    print("<%s>" % name)
    yield
    print("</%s>" % name)


with tag("h1"):
    print("hello")
    print("world")


class Query(object):

    def __init__(self, name):
        self.name = name

    def query(self):
        print('Query info about %s...' % self.name)


@contextmanager
def create_query(name):
    print('Begin')
    q = Query(name)
    yield q
    print('End')


with create_query('Bob') as q:
    q.query()

md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())

Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x)

dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'

print(dd['key2'])

foo = [2, 18, 9, 22, 17, 24, 8, 12, 27]
print([x for x in foo if x % 3 == 0])
