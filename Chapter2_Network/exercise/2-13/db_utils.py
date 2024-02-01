import logging
logging.basicConfig(level=logging.INFO)


"""
数据库操作封装
"""


class MysqlDb:
    @staticmethod
    def connect(host, db_name, user, passwd):
        try:
            import MySQLdb
            try:
                cxn = MySQLdb.connect(host=host, db=db_name, user=user, passwd=passwd)
            except Exception as e:
                logging.warning("mysql connect fail: {}".format(e))
                return None
        except ImportError:
            return None
        cur = cxn.cursor()
        return cxn, cur

    @staticmethod
    def get_rc(cur):
        return cur.rowcount if hasattr(cur, 'rowcount') else -1


class RedisDb:
    @staticmethod
    def connect(host, port):
        try:
            import redis
            try:
                cxn = redis.Redis(host=host, port=port)
            except Exception as e:
                logging.warning("redis connect fail: {}".format(e))
                return None
        except ImportError:
            return None
        return cxn
