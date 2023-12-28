import socket
from threading import Thread
from utils import read, write

HOST = 'localhost'                 # The remote host
PORT = 50007              # The same port as used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    read_thread = Thread(target=read, args=(s,))
    write_thread = Thread(target=write, args=(s,))
    read_thread.start()
    write_thread.start()
    read_thread.join()
    write_thread.join()
