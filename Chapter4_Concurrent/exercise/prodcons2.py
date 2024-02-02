import threading
from random import randint
from time import sleep
from queue import Queue
from concurrent import futures


DEFAULT_THREAD_NUMS = 3
MAX_THREAD_NUMS = 3


lock = threading.Lock()


def writeQ(queue):
    lock.acquire()
    print("producing object for Q...")
    queue.put("xxx", 1)
    print("size now ", queue.qsize())
    lock.release()


def readQ(queue):
    lock.acquire()
    val = queue.get(1)
    print(threading.current_thread(), " consumed object from Q... size now", queue.qsize())
    lock.release()


def writer(queue, loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1, 3))


def reader(queue, loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(2, 5))


funcs = [writer, reader]
nfuncs = range(len(funcs))


def main():
    nloops = randint(2, 5)
    q = Queue(32)
    threads = []
    # for i in nfuncs:
    #     t = MyThread(funcs[i], (q, nloops), funcs[i].__name__)
    #     threads.append(t)
    # 建立一个生产者线程
    producer = threading.Thread(target=writer, args=(q, nloops))
    producer.start()
    # producer.join()
    # 建立多个消费者线程
    consumer = futures.ThreadPoolExecutor(MAX_THREAD_NUMS)
    with consumer:
        for future in consumer.map(reader, [q for _ in range(DEFAULT_THREAD_NUMS)],
                                   [nloops//DEFAULT_THREAD_NUMS for _ in range(DEFAULT_THREAD_NUMS)]):
            pass

    print("all DONE")


if __name__ == "__main__":
    main()



