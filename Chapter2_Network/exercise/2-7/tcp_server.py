import socket


HOST = ''
PORT = 50007
BUF_SIZE = 1024
address = (HOST, PORT)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(address)
    sock.listen(1)

    conn, addr = sock.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(BUF_SIZE)
            if not data:
                break
            print("Received message > : {}".format(data.decode("utf-8")))
            res_data = input("your reply > ")
            conn.sendall(bytes(res_data, 'utf-8'))
