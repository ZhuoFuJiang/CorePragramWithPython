import socket
from time import ctime

host = ''
port = 21567
buf_size = 1024
address = (host, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(address)
sock.listen(5)

while True:
    try:
        print('waiting for connection...')
        client_sock, address = sock.accept()
        print('connected from: {}'.format(address))

        chunk = client_sock.recv(buf_size)
        while chunk:
            client_sock.send(bytes('[{}] {}'.format(ctime(), chunk), 'utf-8'))
            chunk = client_sock.recv(buf_size)

        client_sock.close()
    except KeyboardInterrupt:
        print("Bye Bye")
        sock.close()
