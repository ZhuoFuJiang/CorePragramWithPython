from socketserver import ThreadingTCPServer, StreamRequestHandler
import threading


ip = 'localhost'
port = 50003


client_connection = {}


class MyServer(StreamRequestHandler):
    def handle(self):
        while True:
            data = str(self.request.recv(1024), 'ascii')
            cur_thread = threading.current_thread()
            response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
            self.request.sendall(response)


server = ThreadingTCPServer((ip, port), MyServer)
server.serve_forever()
