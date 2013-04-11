'''
Created on 14.3.2013

@author: misa
'''
import pickle
import numpy as np
import sys, pygame
import autobahn
import twisted
import random
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, \
                               WebSocketClientProtocol, \
                               connectWS
import json

Window_height = 800
Window_width = 1500
LOOP_TIME = 0.1

host = "ws://147.228.47.141:9002" 

data={}

bod2="kos.png"
#bod2="green_dot.png"
bg="pozadiWhite.jpg"

class EchoClientProtocol(WebSocketClientProtocol):
    def sendHello(self):
        self.sendMessage("skeleton")
            
    def send_message(self):
        self.sendMessage("skeleton")
 
    def onOpen(self):
        self.sledovani_init()
        self.sendHello()
        self.stav = 'sledovani'
        self.msg = ''
        reactor.callLater(LOOP_TIME, self.tick)
    
    def update(self,body):
        
        self.body = body    
 
    
    def onMessage(self, msg, binary):
        
        print "Got echo: " + msg
        
        self.msg = msg
        #self.factory.app.reactor.callLater(LOOP_TIME, self.send_message)
        #import pdb; pdb.set_trace()
        
        
        if len(msg) > 2:
            data = json.loads( msg )
         
            self.body = data[0]
            if self.stav == 'sledovani':
                self.sledovani_run()
            
            pygame.display.update()
            
            
        reactor.callLater(LOOP_TIME, self.send_message)
        #self.send_message()

    def tick(self):
        #print 'tik'
        #self.screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop() # just stop somehow
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                reactor.stop() # just stop somehow
                
                
                
        pygame.display.flip()
        reactor.callLater(LOOP_TIME, self.tick)        
        
#    def bod(self, x=None, y=None):    
#        
#        if x == None:
#            self.px = random.randint(Window_width*0.05,Window_width*0.9)
#            self.py = random.randint(Window_height*0.05,Window_height*0.9)
#        else:
#            self.px = x
#            self.py = y
#            
#        self.background=pygame.image.load(bg).convert()
#        self.point2=pygame.image.load(bod2).convert_alpha()   
#        pygame.display.set_caption('Vykresleni bodu')
#        size = self.width, self.height = Window_width,Window_height
#        self.screen = pygame.display.set_mode(size, 0, 32)
#        self.screen.fill((255, 255, 255))
#
#        self.screen.blit(self.background,(0,0))
#        self.screen.blit(self.point, (x,y))
#        pygame.display.update()     
    def sledovani_init(self):
        pygame.init()
        pygame.display.set_caption('Vykresleni bodu')
        self.size = self.width, self.height = Window_width,Window_height
        self.screen = pygame.display.set_mode((self.size),0,32)
        self.background = pygame.image.load(bg).convert()
        self.point2 = pygame.image.load(bod2).convert_alpha()
        pygame.display.update()
        
    def sledovani_run(self):
        print('sledovani')
        torso = self.body["Torso"]
        neck = self.body["Neck"]
        #import pdb; pdb.set_trace()
        krk = [1,neck["Y"],1]
        telo = [torso["X"],torso["Y"],1]
        
        
        
        
        
        
        with open('matice_kal','rb') as f:
            self.matice = pickle.load(f)
        hlavatr = np.dot(self.matice,telo)
        print hlavatr
        self.x = int(hlavatr[0])
        self.y = int(hlavatr[1])
        
       
        vzdalenost = [1,1,torso["Z"]]
        self.vz = int(vzdalenost[2]/500)
        
        print vzdalenost[2]
        self.width = 340/self.vz
        self.height = 400/self.vz
        
#        self.width = abs(krk[1]-telo[1])*2
#        self.height = abs(krk[1]-telo[1])*2
        
        
        self.point2 = pygame.transform.scale(self.point2, (int(self.width), int(self.height)))
        
        self.x -= self.point2.get_width()/2
        self.y -= self.point2.get_height()/2
                
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.point2, (self.x,self.y))
        pygame.display.update()
        
        
        
#        x,y = pygame.mouse.get_pos()
#        x -= point.get_width()/2
#        y -= point.get_height()/2
#        screen.blit(point, (x,y))
        
        
            
if __name__ == '__main__':
    
    pygame.init() 
    factory = WebSocketClientFactory(host, debug = False)
    factory.protocol = EchoClientProtocol
    connectWS(factory)
    reactor.run()            