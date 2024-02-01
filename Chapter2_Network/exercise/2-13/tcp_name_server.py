import socket
import time
from threading import Thread
import logging
from db_utils import MysqlDb, RedisDb
logging.basicConfig(level=logging.INFO)


"""
名称服务器
"""

# 名称服务器的地址，端口号
HOST = ''
PORT = 50003
BUF_SIZE = 1024
ADDRESS = (HOST, PORT)


# mysql的连接方式
HOST = 'localhost'
DBNAME = 'test'
USER = 'root'
PASSWD = '19961001qqasd'
mysql_db, cursor = MysqlDb().connect(HOST, DBNAME, USER, PASSWD)


# redis的连接方式
PORT = 6379
redis_db = RedisDb().connect(HOST, PORT)


# ping所有注册的服务器，如果多次尝试失败，则删除该服务器记录，包括mysql和redis
def ping():
    try:
        while True:
            logging.info("start scan all server")
            # 找到目前所有已经注册的服务器
            select_sql = "select * from server_list"
            logging.info("select sql:{}".format(select_sql))
            cursor.execute(select_sql)
            result = cursor.fetchall()
            if not result:
                logging.info("There is no available servers")
            else:
                for server in result:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        host, port, service = server
                        address = (host, port)
                        try:
                            s.connect(address)
                            status = 1
                        except socket.error as e:
                            logging.warning("connect address: {} failed! Occurred by {}".format(address, e))
                            status = 0
                        if not status:
                            # 删除redis相应数据
                            logging.info("address:{} connect fail, delete record".format(address))
                            redis_db.delete(service)
                            delete_sql = "delete from server_list where service_desc='{}'".format(service)
                            logging.info("delete sql:{}".format(delete_sql))
                            cursor.execute(delete_sql)
                            mysql_db.commit()
                        else:
                            logging.info("address:{} connect success".format(address))
            time.sleep(60)
    except Exception as e:
        s.close()


# 处理客户端/服务器请求的线程
def handle_request(conn, address):
    try:
        while True:
            msg = conn.recv(BUF_SIZE).decode('utf-8')
            if not msg:
                conn.close()
                break
            command = msg.split(":")[0].lstrip().rstrip()
            content = msg.split(":")[1].lstrip().rstrip()
            status = 'fail'
            res = ""
            if command == 'submit':
                # 连接数据库，写入主机名 端口号 服务描述
                try:
                    address = msg.split(":")[2].lstrip().rstrip()
                    host, port = address.split("_")
                    insert_sql = "insert into server_list values ('{}', {}, '{}')".format(host, port, content)
                    logging.info("address:{} service:{} insert sql:{}".format(address, content, insert_sql))
                    cursor.execute(insert_sql)
                    mysql_db.commit()
                    # 同时写入redis
                    logging.info("address:{} service:{} write to redis".format(address, content))
                    redis_db.set(content, "{}_{}".format(host, port))
                    res = "Your service has recorded"
                    status = 'success'
                except Exception as e:
                    res = "{} service:{} has not recorded, fail!".format(address, content)
                    logging.warning("{} service:{} has not recorded, fail! Occurred by {}".format(address, content, e))
            elif command == 'search':
                # 连接数据库，查询服务名对应的主机号 端口号
                try:
                    # 先查询redis，如果没有就查询mysql，然后把数据写入redis
                    result = redis_db.get(content)
                    logging.info("address:{} service:{} redis result:{}".format(address, content, result))
                    if not result:
                        logging.info("redis has no service:{}".format(content))
                        select_sql = "select * from server_list where service_desc='{}'".format(content)
                        logging.info("address:{} service:{} select sql:{}".format(address, content, select_sql))
                        cursor.execute(select_sql)
                        result = cursor.fetchall()
                        if not result:
                            res = "service:{} has not searched, fail!".format(content)
                        else:
                            host, port, _ = result[0]
                            res = "{}_{}".format(host, port)
                            redis_db.set(content, res)
                            status = 'success'
                    else:
                        logging.info("redis has service:{}".format(content))
                        res = bytes.decode(result, 'utf-8')
                        status = 'success'
                except Exception as e:
                    res = "service:{} has not searched, fail!".format(content)
                    logging.warning("service:{} has not searched, fail! Occurred by {}".format(content, e))
            else:
                res = "I can't support the command"
            conn.sendall(bytes(status + ":" + res, 'utf-8'))
    except Exception as e:
        conn.close()


def serve():
    # 创建相应的表
    cursor.execute("create table if not exists server_list "
                   "(host varchar(64),"
                   "port int,"
                   "service_desc varchar(256));")
    ping_thread = Thread(target=ping)
    ping_thread.start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(ADDRESS)
            s.listen(10)
            while True:
                conn, address = s.accept()
                logging.info('Connected by: {}'.format(address))
                handle_thread = Thread(target=handle_request, args=(conn, address, ))
                handle_thread.start()
        except Exception as e:
            s.close()


if __name__ == "__main__":
    serve()
