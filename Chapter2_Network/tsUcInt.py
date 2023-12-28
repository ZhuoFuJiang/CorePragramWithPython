from socket import *


host = '127.0.0.1'
port = 21567
buf_size = 1024
address = (host, port)

udp_client_socket = socket(AF_INET, SOCK_DGRAM)

while True:
    data = input('> ')
    if not data:
        break
    udp_client_socket.sendto(bytes(data, 'utf-8'), address)
    data, address = udp_client_socket.recvfrom(buf_size)
    if not data:
        break
    print(data.decode('utf-8'))

udp_client_socket.close()
