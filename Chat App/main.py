from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor,protocol

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

class ChatClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write('CONNECT'.encode())
        self.factory.app.on_connect(self.transport)
    def dataReceived(self,data):
        self.factory.app.on_message(data)

class ChatClientFactory(protocol.ClientFactory):
    protocol=ChatClient

    def __init__(self,app):
        self.app=app


class ChatApp(App):
    def connect(self):
        host=self.root.ids.server.text
        self.username=self.root.ids.username.text
        reactor.connectTCP(host,9096,ChatClientFactory(self))

    def disconnect(self):
        if self.conn:
            self.conn.loseConnection()
            del self.conn
        self.root.current='login'
        self.root.ids.chat_logs.text=""

    def send_msg(self):
        msg=self.root.ids.message.text
        self.conn.write(('%s:%s' % (self.username,msg)).encode())
        self.root.ids.chat_logs.text +='%s:%s' % (self.username,msg) + '\n'
        self.root.ids.message.text=""

    def on_connect(self,conn):
        self.conn=conn
        self.root.current='chatroom'
    def on_message(self,msg):
        self.root.ids.chat_logs.text +=msg.decode() + '\n'
if __name__=="__main__":
    
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '900')
    Window.clearcolor=(0.75,0.27,0,0.8)
    ChatApp().run()