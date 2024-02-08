from distutils.log import warn as printf
import os
from random import randrange as rand


COLSIZ = 10
FIELDS = ('login', 'userid', 'projid')
RDBMSs = {'s': 'sqlite', 'm': 'mysql'}
DBNAME = 'test'
DBUSER = 'root'
PASSWD = '19961001qqasd'
HOST = 'localhost'
DB_EXC = None
NAMELEN = 16


tformat = lambda s: str(s).title().ljust(COLSIZ)
cformat = lambda s: s.upper().ljust(COLSIZ)


def setup():
    return RDBMSs[input('''
    Choose a database system:
    
    (M)ySQL
    (S)QLite
    
    Enter choice: ''').strip().lower()[0]]


def connect(db, DBNAME):
    global DB_EXC
    dbDir = '%s_%s' % (db, DBNAME)
    if db == 'sqlite':
        try:
            import sqlite3
        except ImportError:
            return None

        DB_EXC = sqlite3
        if not os.path.isdir(dbDir):
            os.mkdir(dbDir)
        cxn = sqlite3.connect(os.path.join(dbDir, DBNAME))
    elif db == 'mysql':
        try:
            import MySQLdb
            try:
                cxn = MySQLdb.connect(host=HOST, db=DBNAME, user=DBUSER, passwd=PASSWD)
            except Exception:
                return None
        except ImportError:
            return None
    else:
        return None
    return cxn


def create(cur):
    try:
        cur.execute('''CREATE TABLE users (
        login VARCHAR(%d),
        userid INTEGER,
        projid INTEGER)''' % NAMELEN)
    except Exception as e:
        drop(cur)
        create(cur)


drop = lambda cur: cur.execute('DROP TABLE users')

NAMES = (('aaron', 8312), ('angela', 7603), ('dave', 7306), ('davina', 7902),
         ('elliot', 7911), ('ernie', 7410), ('jess', 7912), ('jim', 7512), ('larry', 7311))


def randName():
    pick = set(NAMES)
    while pick:
        yield pick.pop()


def insert(cur, db):
    if db == 'sqlite':
        cur.executemany("INSERT INTO users VALUES(?,?,?)",
                        [(who, uid, rand(1, 5)) for who, uid in randName()])
    elif db == 'mysql':
        cur.executemany("INSERT INTO users VALUES(%s, %s, %s)",
                        [(who, uid, rand(1, 5)) for who, uid in randName()])


getRC = lambda cur: cur.rowcount if hasattr(cur, 'rowcount') else -1


def update(cur):
    fr = rand(1, 5)
    to = rand(1, 5)
    cur.execute("UPDATE users SET projid=%d WHERE projid=%d" % (to, fr))
    return fr, to, getRC(cur)


def delete(cur):
    rm = rand(1, 5)
    cur.execute("DELETE FROM users WHERE projid=%d" % rm)
    return rm, getRC(cur)


def dbDump(cur):
    cur.execute('SELECT * FROM users')
    printf("\n%s" % ''.join(map(cformat, FIELDS)))
    for data in cur.fetchall():
        printf("".join(map(tformat, data)))


def main():
    db = setup()
    printf("*** Connect to %r database" % db)
    cxn = connect(db, DBNAME)
    if not cxn:
        printf('ERROR %r not supported or unreachable, exit' % db)
        return
    cur = cxn.cursor()
    printf("\n*** Creating users table")
    create(cur)

    printf("\n*** Inserting names into table")
    insert(cur, db)
    dbDump(cur)

    printf("\n*** Randomly moving folks")
    fr, to, num = update(cur)
    printf("\t(%d users moved) from (%d) to (%d)" % (num, fr, to))
    dbDump(cur)

    printf("\n*** Randomly choosing group")
    rm, num = delete(cur)
    printf("\t(group #%d; %d users removed)" % (rm, num))
    dbDump(cur)

    printf("\n*** Dropping users table")
    drop(cur)
    printf("\n*** Close cxns")
    cur.close()
    cxn.commit()
    cxn.close()


if __name__ == "__main__":
    main()
