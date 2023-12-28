from socket import *
from time import ctime


host = ''
port = 21567
buf_size = 1024
address = (host, port)

tcp_server_sock = socket(AF_INET, SOCK_STREAM)
tcp_server_sock.bind(address)
tcp_server_sock.listen(5)

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

tcp_server_sock.close()

