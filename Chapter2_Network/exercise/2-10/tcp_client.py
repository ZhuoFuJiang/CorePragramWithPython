import socket
from threading import Thread
import sys

HOST = "localhost"
PORT = 9898
ADDR = (HOST, PORT)
BUFSIZE = 1024


def read(s, addr, room_id):
    while True:
        data = s.recv(BUFSIZE)
        if not data:
            print("No reply")
        else:
            print("\nReceived message> {} from {} in room {}".format(data.decode("utf-8"), repr(addr), room_id))


def write(s, addr, room_id):
    while True:
        data = input("Your messages to {}> ".format(repr(addr)))
        data = gen_message(room_id, data)
        s.sendall(bytes(data, 'utf-8'))


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


def gen_message(room_id, raw_message):
    return '<RID:{}>{}</RID:{}>'.format(room_id, raw_message, room_id)


def main():
    room_id = input('<Room ID> ')

    client_socket = socket.socket()
    # client_socket.settimeout(2)

    try:
        client_socket.connect(ADDR)

        # notify all room's user that new client is entered
        client_socket.send(bytes(gen_message(room_id, ''), 'utf-8'))
    except socket.error:
        print("Unable to connect")
        sys.exit()

    print('Connected to remote host. Start sending messages')
    prompt()
    read_thread = Thread(target=read, args=(client_socket, ADDR, room_id))
    write_thread = Thread(target=write, args=(client_socket, ADDR, room_id))
    read_thread.start()
    write_thread.start()
    read_thread.join()
    write_thread.join()


if __name__ == '__main__':
    main()
