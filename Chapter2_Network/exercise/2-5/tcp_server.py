# Echo server program
import os
import socket

# 服务器新增功能：1、返回date 2、获取操作系统信息 3、接收ls dir命令，列出文件清单
import time

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    data = data.decode('utf-8')
                    print("Received: {}".format(data))
                    res_data = ''
                    if data.startswith('execute command'):
                        command = data.split(":")[1].lstrip().split(" ")[0].strip()
                        print("command: {}".format(command))
                        if command == 'date':
                            res_data += "服务器日期: %s" % time.ctime()
                        elif command == 'os':
                            res_data += "服务器操作系统: %s" % os.name
                        elif command == 'ls':
                            dir_param = data.split(":")[1].lstrip().split(" ")[1].strip()
                            res_data += "服务器当前目录为: %s" % ",".join(os.listdir(dir_param))
                        else:
                            res_data += "Invalid command"
                    else:
                        res_data += data
                conn.sendall(bytes(res_data, 'utf-8'))
