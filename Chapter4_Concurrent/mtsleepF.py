from threading import Thread, currentThread, Lock
from time import sleep, ctime
import random
import contextlib
from atexit import register


lock = Lock()


class ClearOutputSet(set):
    def __str__(self):
        return ', '.join(x for x in self)


loops = (random.randint(2, 5) for x in range(random.randint(3, 7)))
remaining = ClearOutputSet()


# 将加锁和释放锁变成上下文管理形式
# 实现方式1
class Locking:
    def __enter__(self):
        lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        lock.release()


# 实现方式2
@contextlib.contextmanager
def locking():
    lock.acquire()
    yield 1
    lock.release()


def loop(nesc):
    myname = currentThread().name
    # with Locking():
    with locking() as t:
        # lock.acquire()
        remaining.add(myname)
        print("[%s] Started %s" % (ctime(), myname))
        # lock.release()
    sleep(nesc)
    # with Locking():
    with locking() as t:
        # lock.acquire()
        remaining.remove(myname)
        print("[%s] Comleted %s (%d secs)" % (ctime(), myname, nesc))
        print("      (remaining: %s)" % (remaining or 'NONE'))
        # lock.release()


def _main():
    for pause in loops:
        Thread(target=loop, args=(pause, )).start()


@register
def _atexit():
    print("all DONE at:", ctime())


if __name__ == "__main__":
    _main()
