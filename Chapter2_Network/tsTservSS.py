from socketserver import TCPServer as tcp, StreamRequestHandler as srh
from time import ctime

host = ''
port = 21567
address = (host, port)


class MyRequestHandler(srh):
    def handle(self) -> None:
        print('...connected from: {}'.format(self.client_address))
        self.wfile.write(bytes(
            '[{}] {}'.format(ctime(), self.rfile.readline()), 'utf-8'))


tcp_server = tcp(address, MyRequestHandler)
print('waiting for connection...')
tcp_server.serve_forever()
