# Echo client program
import socket


HOST = ''                 # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # s.sendall(bytes('Hello, world', 'utf-8'))
    while True:
        data = input("> ")
        s.sendall(bytes(data, "utf_8"))
        data = s.recv(1024)
        print('Received', repr(data.decode('utf-8')))
