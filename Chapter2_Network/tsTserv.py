from socket import *
from time import ctime


host = ''
port = 21567
buf_size = 1024
address = (host, port)

tcp_server_sock = socket(AF_INET, SOCK_STREAM)
tcp_server_sock.bind(address)
tcp_server_sock.listen(5)
# 让已关闭的套接字能立即使用
tcp_server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
try:
    while True:
        print('waiting for connection...')
        tcp_client_sock, address = tcp_server_sock.accept()
        print('connected from: {}'.format(address))

        while True:
            data = tcp_client_sock.recv(buf_size)
            if not data:
                break
            tcp_client_sock.send(bytes('[{}] {}'.format(ctime(), data), 'utf-8'))

        tcp_client_sock.close()
except Exception as e:
    print("connection fail! occurred by {}".format(e))
finally:
    tcp_server_sock.close()

