BUF_SIZE = 1024


# 如果要全双工聊天，就必须要用两个线程啊，一个读一个写
def read(s):
    while True:
        data = s.recv(BUF_SIZE)
        if not data:
            print("No reply")
        else:
            print("\nReceived message> {}".format(data.decode("utf-8")))


def write(s):
    while True:
        data = input("Your messages > ")
        s.sendall(bytes(data, 'utf-8'))
