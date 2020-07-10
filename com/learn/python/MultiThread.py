import threading
import time
from queue import Queue


class CustomThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.__queue = queue

    def run(self):
        while True:
            q_method = self.__queue.get()
            q_method()
            self.__queue.task_done()


def moyu():
    print(" 开始摸鱼 %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def queue_pool():
    queue = Queue(5)
    for i in range(queue.maxsize):
        t = CustomThread(queue)
        t.setDaemon(True)
        t.start()

    for i in range(20):
        queue.put(moyu)
    queue.join()


if __name__ == '__main__':
    queue_pool()

# # 创建一个线程子类
# class MyThread(threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#
#     def run(self):
#         print("开始线程：" + self.name)
#         moyu_time(self.name, self.counter, 10)
#         print("退出线程：" + self.name)



#
#
# # 创建新线程
# # 小帅b找了两个人来摸鱼
# # 让小明摸一次鱼休息1秒钟
# # 让小红摸一次鱼休息2秒钟
# thread1 = MyThread(1, "小明", 1)
# thread2 = MyThread(2, "小红", 2)
#
# # 开启新线程
# thread1.start()
# thread2.start()
# # 等待至线程中止
# thread1.join()
# thread2.join()
# print("退出主线程")
