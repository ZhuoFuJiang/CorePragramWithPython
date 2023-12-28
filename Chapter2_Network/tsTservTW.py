from twisted.internet import protocol, reactor
from time import ctime


port = 21567


class TsServerProtocol(protocol.Protocol):
    def connectionMade(self):
        self.client = self.transport.getPeer().host
        print('...connected from:{}'.format(self.client))

    def dataReceived(self, data: bytes):
        self.transport.write(bytes("[{}] {}".format(ctime(), data.decode('utf-8')),
                                   'utf-8'))


factory = protocol.Factory()
factory.protocol = TsServerProtocol
print('waiting for connection...')
reactor.listenTCP(port, factory)
reactor.run()
