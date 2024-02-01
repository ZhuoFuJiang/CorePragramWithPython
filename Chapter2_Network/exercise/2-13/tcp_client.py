import socket
import logging
logging.basicConfig(level=logging.INFO)


HOST = 'localhost'
PORT = 50003
BUF_SIZE = 1024
ADDRESS = (HOST, PORT)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(ADDRESS)
    s.sendall(bytes("search: shopping", 'utf-8'))
    res = s.recv(BUF_SIZE).decode('utf-8')
    status = res.split(":")[0]
    content = res.split(":")[1]
    if status == 'success':
        try:
            host, port = res.split(":")[1].split("_")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
                s1.connect((host, int(port)))
                s1.sendall(bytes("shopping: hi, how are you", 'utf-8'))
                res = s1.recv(BUF_SIZE).decode('utf-8')
                logging.info("service server res: {}".format(res))
        except Exception as e:
            logging.warning(e)
    else:
        logging.info("name server res: {}".format(content))
