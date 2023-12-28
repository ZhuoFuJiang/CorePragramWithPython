import socket


default_host = '127.0.0.1'
default_port = 21567
buf_size = 1024

# TODO 实质上一个好的程序应该检查一下二者的格式和范围
host = input("Please input host: ")
if host == '':
    print("Input is valid, will use default_host")
    host = default_host
port = input("Please input port: ")
if port == '':
    print("Input is valid, will use default_port")
    port = default_port
else:
    try:
        port = int(port)
    except ValueError as e:
        print("Valid port, can't transform to integer: {}".format(e))
        port = default_port
address = (host, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(address)

while True:
    data = input('> ')
    if not data:
        break
    sock.send(bytes(data, 'utf-8'))
    data = sock.recv(buf_size)
    if not data:
        break
    print(data.decode('utf-8'))

sock.close()
