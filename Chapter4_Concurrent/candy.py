from atexit import register
from random import randrange
from threading import BoundedSemaphore, Lock, Thread
from time import sleep, ctime
import random


lock = Lock()
MAX = 5
candystray = BoundedSemaphore(5)


def refill():
    lock.acquire()
    print("Refilling candy...")
    try:
        # release相当于加1
        candystray.release()
    except ValueError:
        # 超过初始值，报异常
        print("full, skipping")
    else:
        print("OK")
    lock.release()


def buy():
    lock.acquire()
    print("Buying candy...")
    # acquire释放初始值
    # 传入False表明非阻塞，如果值为0直接返回
    if candystray.acquire(False):
        print("OK")
    else:
        print("empty, skipping")
    lock.release()


def producer(loops):
    for i in range(loops):
        refill()
        sleep(randrange(3))


def consumer(loops):
    for i in range(loops):
        buy()
        sleep(randrange(3))


def _main():
    print("starting at:", ctime())
    nloops = randrange(2, 6)
    print("THE CANDY MACHINE (full with %d bars)!" % MAX)
    Thread(target=consumer, args=(randrange(nloops, nloops+MAX+2),)).start()
    Thread(target=producer, args=(nloops,)).start()


@register
def _atexit():
    print("all DONE at:", ctime())


if __name__ == "__main__":
    _main()

