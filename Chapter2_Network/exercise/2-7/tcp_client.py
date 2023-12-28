import socket


HOST = 'localhost'                 # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = input("Your message > ")
        s.sendall(bytes(data, "utf_8"))
        data = s.recv(1024)
        print('Received', repr(data.decode('utf-8')))
