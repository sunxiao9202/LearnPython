import multiprocessing
import time


def f(name):
    print('hello', name)


if __name__ == '__main__':
    with multiprocessing.Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
