import socket
import select
import re

HOST = "localhost"
PORT = 9898
ADDR = (HOST, PORT)
BUFSIZE = 1024

CONFORM_MSG = re.compile(r'^<RID:(\d+)>([\s\S]*?)</RID:\1>')


_service_socket = socket.socket()
# 允许套接字在其关闭后立即重新使用其地址。
_service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
_service_socket.bind(ADDR)
_service_socket.listen(10)

_current_in_list = [_service_socket]
_room = dict()


def broadcast_message(room_id, sock, message):
    for member in _room[room_id]:
        if member is not sock:
            try:
                member.send(bytes(message, 'utf-8'))
            except socket.error:
                member.close()
                _current_in_list .remove(member)
                _room[room_id].remove(member)


def main():
    while True:
        # 如果有可读的套接字，则返回
        rlist, wlist, xlist = select.select(_current_in_list, [], [])

        for sock in rlist:
            if sock is _service_socket:
                client, addr = sock.accept()
                _current_in_list.append(client)
                print("Client (%s) connected." % repr(addr))
            else:
                try:
                    raw_message = sock.recv(BUFSIZE).decode('utf-8')
                    if raw_message:
                        rgx_message = CONFORM_MSG.match(raw_message)
                        if rgx_message:
                            room_id = rgx_message.group(1)
                            message = rgx_message.group(2)
                            if sock not in _room.setdefault(room_id, []):
                                _room[room_id].append(sock)
                                # getpeername 用于获取与套接字连接的远程（对等）主机的地址
                                broadcast_message(room_id, sock, '\n[%s:%s] entered room.\n'\
                                                                         % sock.getpeername())
                            else:
                                broadcast_message(room_id, sock, "\n<" + str(sock.getpeername()) + ">" + message)
                        else:
                            print("Invalid format message,", raw_message)
                except socket.error:
                    print("Client (%s, %s) is offline" % sock.getpeername())
                    sock.close()
                    _current_in_list.remove(sock)
                    for room_id, socks in _room.items():
                        for _ in socks:
                            if _ is sock:
                                _room[room_id].remove(_)
                                break
                        else:
                            continue
                        break


if __name__ == '__main__':
    main()