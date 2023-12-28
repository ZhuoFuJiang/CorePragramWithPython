from socket import *

host = '127.0.0.1'
port = 21567
buf_size = 1024
address = (host, port)

while True:
    tcp_client_socket = socket(AF_INET, SOCK_STREAM)
    tcp_client_socket.connect(address)
    data = input('> ')
    if not data:
        break
    tcp_client_socket.send(bytes('{} \r\n'.format(data), 'utf-8'))
    data = tcp_client_socket.recv(buf_size)
    if not data:
        break
    print(data.strip())
    tcp_client_socket.close()
