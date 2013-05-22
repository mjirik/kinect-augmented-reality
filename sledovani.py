'''
Created on 14.3.2013

@author: misa
'''
import pickle
import math
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
import kalibrace2

#Window_height = 700
#Window_width = 1300

Window_height = 550
Window_width = 1100



LOOP_TIME = 0.1

host = "ws://147.228.47.141:9002" 

data={}

Hkos="kos.png"
bod2="green_dot.png"
bg="black.png"

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
        self.kos = pygame.image.load(Hkos).convert_alpha()
        pygame.display.update()
        
        with open('matice_kal2','rb') as f:
            self.kalib_params = pickle.load(f)
        
    def sledovani_run(self):
        print('sledovani')
        try: 
            torso = self.body["Torso"]
            neck = self.body["Neck"]
            head = self.body["Head"]
            #import pdb; pdb.set_trace()
            krk = [neck["X"],neck["Y"], neck["Z"]]
            telo = [torso["X"],torso["Y"],torso["Z"]]
            hlava = [head["X"],head["Y"],head["Z"]]
            
            
    
            print telo
            telotr = kalibrace2.projekce(telo, self.kalib_params)
            krktr = kalibrace2.projekce(krk, self.kalib_params)
            hlavatr = kalibrace2.projekce(hlava, self.kalib_params)
            
            print "po kalibraci ", telotr
            self.xt = int(telotr[0])
            self.yt = int(telotr[1])
            
            #pridani bodu
            self.xk = int(krktr[0])
            self.yk = int(krktr[1])
            
            self.xh = int(hlavatr[0])
            self.yh = int(hlavatr[1])
            
        except Exception as e:
            print "problem v prijate zprave" 
            print e
        
        
        
        
        
       # zmena velikosti obrazku podle vzdalenosti
#        vzdalenost = [1,1,torso["Z"]]
#        self.vz = int(vzdalenost[2]/500)
#        
#        print vzdalenost[2]
#        self.width = 600/self.vz
#        self.height = 800/self.vz
        
        
        
#        self.width = abs(krk[1]-telo[1])*2
#        self.height = abs(krk[1]-telo[1])*2
        
        
#        self.point2 = pygame.transform.scale(self.point2, (int(self.width), int(self.height)))
        
        self.xt -= self.point2.get_width()/2
        self.yt -= self.point2.get_height()/2
        
        self.xk -= self.point2.get_width()/2
        self.yk -= self.point2.get_height()/2
        
#        self.xh -= self.point2.get_width()/2
#        self.yh -= self.point2.get_height()/2
#        
        self.xObr = (self.xt - self.xk)/2 + self.xk
        self.yObr = (self.yt - self.yk)/2 + self.yk
        
        self.xObr -= self.kos.get_width()/2
        self.yObr -= self.kos.get_height()/2
                
             
        
        
        self.height = self.yt - self.yk 
        self.width = self.kos.get_height()/1.3
        self.kos = pygame.image.load(Hkos).convert_alpha()
        
        prepona = (math.sqrt(math.pow((self.xt-self.xk), 2)+math.pow((self.yt-self.yk),2))/2)
        prilehla = (self.yt - self.yk)/2
        cosinus = (prilehla/prepona)
        angle = math.pow(-cosinus,-1)*(180/math.pi)+45
        
#        u1 = math.fabs(self.xt-self.xk)
#        u2 = math.fabs(self.yt-self.yk)  
#        v1 = math.fabs(self.xObr-self.xk)
#        v2 = math.fabs(self.yObr-self.yk)
#        cosinus = (u1*v1+u2*v2)/((math.sqrt(math.pow(u1,2)+math.pow(u2,2)))*(math.sqrt(math.pow(v1,2)+math.pow(v2,2))))
#        angle = math.pow(-cosinus,-1)*(180/math.pi)+45
#        print "uhel",angle
         
           
        self.kos = pygame.transform.scale(self.kos, (int(self.width), int(self.height)))       
        self.kos = pygame.transform.rotate(self.kos, angle)  
                
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.point2, (self.xt,self.yt))
        self.screen.blit(self.point2, (self.xk,self.yk))
        #self.screen.blit(self.point2, (self.xh,self.yh))
        self.screen.blit(self.kos, (self.xObr,self.yObr))
        
        print "y body"
        print self.yk
        print self.yt
        print self.yObr
        
        
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