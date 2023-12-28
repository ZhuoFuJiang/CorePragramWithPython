BUF_SIZE = 1024


# 如果要全双工聊天，就必须要用两个线程啊，一个读一个写
def read(s, addr):
    while True:
        data = s.recv(BUF_SIZE)
        if not data:
            print("No reply")
        else:
            print("\nReceived message> {} from {}".format(data.decode("utf-8"), repr(addr)))


def write(s, addr):
    while True:
        data = input("Your messages to {}> ".format(repr(addr)))
        s.sendall(bytes(data, 'utf-8'))
