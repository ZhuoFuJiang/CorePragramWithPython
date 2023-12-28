import socket
from threading import Thread
from utils import read, write

HOST = 'localhost'                 # The remote host
PORT = 50007              # The same port as used by the server
ADDRESS = (HOST, PORT)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(ADDRESS)
    read_thread = Thread(target=read, args=(s, ADDRESS))
    write_thread = Thread(target=write, args=(s, ADDRESS))
    read_thread.start()
    write_thread.start()
    read_thread.join()
    write_thread.join()
