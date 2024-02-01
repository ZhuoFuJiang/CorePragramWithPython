import socket
from threading import Thread
import logging
import time
logging.basicConfig(level=logging.INFO)


"""
服务器1: 提供搜索引擎服务
"""

HOST = 'localhost'
PORT = 50005
BUF_SIZE = 1024
ADDRESS = (HOST, PORT)


# 注册线程，向名称服务器注册服务
def submit():
    # 名称服务器的默认配置
    name_server_host = 'localhost'
    name_server_port = 50003
    address = (name_server_host, name_server_port)
    submit_msg = "submit: chat box: {}_{}".format(HOST, PORT)
    success = 0
    while not success:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(address)
                s.sendall(bytes(submit_msg, 'utf-8'))
                res = s.recv(BUF_SIZE).decode("utf-8")
                status = res.split(":")[0]
                if status == "success":
                    s.sendall(bytes('', 'utf-8'))
                    success = 1
        except socket.error as e:
            logging.warning("connect name server failed: {}".format(e))
            s.close()
            time.sleep(60)


# 处理客户端/名称服务器请求的线程
def handle_request(conn):
    try:
        while True:
            msg = conn.recv(BUF_SIZE).decode('utf-8')
            if not msg:
                conn.close()
                break
            command = msg.split(":")[0].lstrip().rstrip()
            content = msg.split(":")[1].lstrip().rstrip()
            status = 'fail'
            if command == 'ping':
                res = "I'm alive"
                status = 'success'
            elif command == 'chat':
                res = "this is {}'s response...".format(content)
                status = 'success'
            else:
                res = "I can't support the command"
            conn.sendall(bytes(status + ":" + res, 'utf-8'))
    except Exception as e:
        conn.close()


def serve():
    submit_thread = Thread(target=submit)
    submit_thread.start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(ADDRESS)
            s.listen(10)
            while True:
                conn, address = s.accept()
                logging.info('Connected by: {}'.format(address))
                handle_thread = Thread(target=handle_request, args=(conn, ))
                handle_thread.start()
        except Exception as e:
            s.close()


if __name__ == "__main__":
    serve()
