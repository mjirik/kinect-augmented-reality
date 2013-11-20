import sys
import json
from twisted.internet import reactor
from twisted.python import log

from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS
                               
Window_height = 700
Window_width = 1300                               


#  body = {'Torso':{'X':300,'Y':50,'Z':50},
#         'Neck':{'X':100,'Y':100,'Z':50},
#         'Head':{'X':400,'Y':50,'Z':100}}
body = {'Torso':{'X':(Window_width/2),'Y':(Window_height-300),'Z':50},
        'Neck':{'X':(Window_width/2),'Y':(Window_height-500),'Z':50},
        'Head':{'X':(Window_width/2),'Y':(Window_height-600),'Z':50}}

bodys=[body]
         
class EchoServerProtocol(WebSocketServerProtocol):

   def onMessage(self, msg, binary):
      print "sending echo:", msg
      sendMsg = json.dumps(bodys)
      self.sendMessage(sendMsg, binary)


def main():

   log.startLogging(sys.stdout)

   factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
   factory.protocol = EchoServerProtocol
   listenWS(factory)

   reactor.run()
   
if __name__ == '__main__':
    main()