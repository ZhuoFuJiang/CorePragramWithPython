from socket import *
from time import ctime


host = ''
port = 21567
buf_size = 1024
address = (host, port)

udp_server_sock = socket(AF_INET, SOCK_DGRAM)
udp_server_sock.bind(address)

while True:
    print('waiting for connection...')
    data, address = udp_server_sock.recvfrom(buf_size)
    udp_server_sock.sendto(bytes('[{}] {}'.format(ctime(), data), 'utf-8'), address)
    print('...received from and returned to: {}'.format(address))

udp_server_sock.close()

