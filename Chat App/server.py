from twisted.internet.protocol import Protocol,Factory
from twisted.internet import reactor

transports=set()

class Chat(Protocol):
    def dataReceived(self,data):
        transports.add(self.transport)

        if ':' not in data.decode():
            return
        
        user , msg=data.decode().split(":",1)
        for t in transports:
            if t is not self.transport:
                t.write(('{0} says : {1}'.format(user,msg)).encode())

class ChatFactory(Factory):
    def buildProtocol(self,addr):
        return Chat()

reactor.listenTCP(9096,ChatFactory())
reactor.run()
