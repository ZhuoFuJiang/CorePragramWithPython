import socket
from threading import Thread
from utils import read, write


HOST = ''
PORT = 50007
BUF_SIZE = 1024
address = (HOST, PORT)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(address)
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        print('\nConnected by', addr)
        # 如果有客户端连接了服务器端，则分配两个线程，一个负责读，一个负责写
        read_thread = Thread(target=read, args=(conn, addr))
        write_thread = Thread(target=write, args=(conn, addr))
        read_thread.start()
        write_thread.start()
        # read_thread.join()
        # write_thread.join()
