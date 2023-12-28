from twisted.internet import protocol, reactor

host = 'localhost'
port = 21567


class TSClientProtocol(protocol.Protocol):
    def sendData(self):
        data = input('> ')
        if data:
            print('...sending {}...'.format(data))
            self.transport.write(data)
        else:
            self.transport.loseConnection()

    def connectionMade(self):
        self.sendData()

    def dataReceived(self, data: bytes):
        print(data)
        self.sendData()


class TSClientFactory(protocol.ClientFactory):
        protocol = TSClientProtocol
        clientConnectionLost = clientConnectionFailed = \
            lambda self, connector, reason: reactor.stop()

reactor.connectTCP(host, port, TSClientProtocol)
reactor.run()
