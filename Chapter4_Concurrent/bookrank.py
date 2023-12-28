from atexit import register
from re import compile
from threading import Thread
from time import ctime
from urllib import request


REGEX = compile('#([\d,]) in Books ')
AMZN = 'http://amazon.com/dp/'
ISBNs = {'0132269937': 'Core Python Programming',
         '0132356139': 'Python Web Development with Django',
         '0137143419': 'Python Fundamentals'}


def getRanking(isbn):
    page = request.urlopen('%s%s' % (AMZN, isbn))
    data = page.read()
    page.close()
    return REGEX.findall(data)[0]


def _showRanking(isbn):
    print('- %r ranked %s' % (ISBNs[isbn], getRanking(isbn)))


def _main():
    print("At", ctime(), 'on Amazon...')
    for isbn in ISBNs:
        # _showRanking(isbn)
        Thread(target=_showRanking, args=(isbn, )).start()


# 脚本退出时执行该函数
@register
def _atexit():
    print("all DONE at:", ctime())


if __name__ == "__main__":
    _main()