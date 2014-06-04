'''
Created on 14.3.2013

@author: misa
'''
import pickle
import math
import numpy as np
import sys, pygame
from pygame.locals import *
import autobahn
import twisted
import random
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, \
                               WebSocketClientProtocol, \
                               connectWS
import json
import threading
import os
import config

fileList2 = os.listdir(config.im_folder)
fileList3 = os.listdir(config.im_directory)
index = 0
a = 0
Window_height = config.window_height    
Window_width = config.window_width

mode = config.MODE

loop = config.LOOP_TIME

if mode == 'demo':

    host = "ws://localhost:9000"
    import fakeserver
    def vlakno():
        fakeserver.main()
    v1 = threading.Thread(target = vlakno)
    v1.start()    
    
else:
#     host = "ws://147.228.47.141:9002" 
    host = config.kinect_server_adress #"ws://192.168.1.100:9002"  

data={}



bod1 = config.red_dot
bod2= config.green_dot
bg = config.background

class KinectClientProtocol(WebSocketClientProtocol):
   
    def sendHello(self):
        self.sendMessage("skeleton")
            
    def send_message(self):
        self.sendMessage("skeleton")
 
    def onOpen(self):
        #print "op"
        self.sledovani_init()
        self.sendHello()
        self.stav = 'sledovani'
        self.msg = ''
        reactor.callLater(loop, self.tick)
    
    def update(self,body):
        self.body = body    
    
    def onMessage(self, msg, binary):
        print "Got echo: " + msg
        
        self.msg = msg
        
        if len(msg) > 2:
            data = json.loads( msg )
         
            self.body = data[0]    
            pygame.display.update()  
        reactor.callLater(loop, self.send_message)
   
    def tick(self):
        global a 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop() # just stop somehow
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if config.spacebar_to_toggle_images == "yes":  
                    a = self.changeOfIndex(a,fileList2)
                if config.spacebar_to_toggle_directory == "yes":
                    a = self.changeOfIndex(a,fileList3)
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                reactor.stop() # just stop somehow
         
        self.sledovani_run()  
        pygame.display.update()
        reactor.callLater(loop, self.tick)
        print fileList3[a]
            
    def sledovani_init(self):
        pygame.init()
        pygame.display.set_caption('Vykresleni bodu')
        self.size = self.width, self.height = Window_width,Window_height
        self.screen = pygame.display.set_mode((self.size),0,32)
        self.background = pygame.image.load(bg).convert()
        self.point1 = pygame.image.load(bod1).convert_alpha()
        self.point2 = pygame.image.load(bod2).convert_alpha()
        pygame.display.update()
        
        with open('matice_kal2','rb') as f:
            self.kalib_params = pickle.load(f)
       
    def sledovani_run(self):
        print('sledovani')
        try: 
            torso = self.body["Torso"]
            neck = self.body["Neck"]
            head = self.body["Head"]
            krk = [neck["X"],neck["Y"], neck["Z"]]
            telo = [torso["X"],torso["Y"],torso["Z"]]
            hlava = [head["X"],head["Y"],head["Z"]]
            
            print krk
# prevod z +/- 600 na 0 az 640
             
            krk = self.__getImageCoordinatesFromSkeletonCoordinates(-np.array(krk[:2]))
            telo = self.__getImageCoordinatesFromSkeletonCoordinates(-np.array(telo[:2]))
            hlava = self.__getImageCoordinatesFromSkeletonCoordinates(-np.array(hlava[:2]))
           
            print "po prepoctu do obazovych sour"
            #print krk
            print telo
            #print hlava
        
            kalib_mode = config.calibration_mode
            if mode == 'demo':
                kalib_mode = 'off'
                kalib_mode = config.calibration_mode
                import datetime
                t = datetime.datetime.now()
                t_us = t.second
                
                posunX = int(60*np.sin(3.14*t_us/60))
                posunY = int(60*np.cos(3.14*t_us/60))
                
                krktr = [neck["X"] + posunX ,neck["Y"] + posunY, neck["Z"]]
                telotr = [torso["X"] + posunX,torso["Y"] + posunY,torso["Z"]]
                hlavatr = [head["X"] + posunX,head["Y"] + posunY,head["Z"]]
            
            else:
                print "pred kalibraci "
                print "telo", telo
    #             telotr = kalibrace2.projekce(telo, self.kalib_params,mode = kalib_mode)
    #             krktr = kalibrace2.projekce(krk, self.kalib_params,mode = kalib_mode)
    #             hlavatr = kalibrace2.projekce(hlava, self.kalib_params,mode = kalib_mode)
    
                telotr = self.projekce(telo, self.kalib_params,mode = kalib_mode)
                krktr = self.projekce(krk, self.kalib_params,mode = kalib_mode)
                hlavatr = self.projekce(hlava, self.kalib_params,mode = kalib_mode)
            
                print "po kalibraci "
                print "telo", telotr
             #   print "neck", krktr
              #  print "head", hlavatr
#                    
            self.xt = int(telotr[0])
            self.yt = int(telotr[1])
            
            self.xk = int(krktr[0])
            self.yk = int(krktr[1])
            
            self.xh = int(hlavatr[0])
            self.yh = int(hlavatr[1])
            
        except Exception as e:
            print "problem v prijate zprave  ", e
            self.xt = int(0)
            self.yt = int(0)
            
            self.xk = int(0)
            self.yk = int(0)
            
            self.xh = int(0)
            self.yh = int(0)
              
        self.xt -= self.point2.get_width()/2
        self.yt -= self.point2.get_height()/2
        
        self.xh -= self.point2.get_width()/2
        self.yh -= self.point2.get_height()/2
        
        self.xk -= self.point2.get_width()/2
        self.yk -= self.point2.get_height()/2
        
        self.xh -= self.point2.get_width()/2
        self.yh -= self.point2.get_height()/2
        
        self.xObr = (self.xt - self.xk)/2 + self.xk
        self.yObr = (self.yt - self.yk)/2 + self.yk
        
        global index
        
        if config.spacebar_to_toggle_images == "yes": 
            Hkos = config.im_folder + fileList2[a]
        if config.spacebar_to_toggle_directory == "yes":    
            b = os.listdir(config.im_directory + fileList3[a])
            index = self.changeOfIndex(index,b)    
            Hkos = config.im_directory + fileList3[a]+"/" + b[index]  
                          
        self.kos = pygame.image.load(Hkos).convert_alpha()      
        self.xObr -= self.kos.get_width()/2
        self.yObr -= self.kos.get_height()/2
        
        self.height = self.yt - self.yk
        self.width = self.kos.get_height()/1.3
        
#         if config.rotate_and_scale_of_image == "yes": 
#             prepona = (math.sqrt(math.pow((self.xt-self.xk), 2)+math.pow((self.yt-self.yk),2))/2)
#             prilehla = (self.yt - self.yk)/2
#             cosinus = (prilehla/prepona)
#             angle = math.pow(-cosinus,-1)*(180/math.pi)+45 
#             self.kos = pygame.transform.scale(self.kos, (int(self.width), int(self.height)))       
#             self.kos = pygame.transform.rotate(self.kos, angle)  
                
        self.screen.blit(self.background,(0,0))
        if config.point_torso == "yes": 
            self.screen.blit(self.point2, (self.xt,self.yt))
        if config.point_neck == "yes":    
            self.screen.blit(self.point2, (self.xk,self.yk))
        if config.point_head == "yes":    
            self.screen.blit(self.point2, (self.xh,self.yh))
        if config.image == "yes":
            self.screen.blit(self.kos, (self.xObr,self.yObr))   
        pygame.display.flip()
        pygame.display.update()
        
    def __getImageCoordinatesFromSkeletonCoordinates(self, skcoor):
        sk_res = np.array([1280, 960])
        sk_res = np.array([1280, 960])
        im_res =  np.array([640, 480])
        sk_res = im_res*1.5
        skcoor = np.array(skcoor)
        
        scale =  im_res /sk_res
        
        a1 = np.array([378,320])
        a2 = np.array([0.37, 0.4])
        
        #a1 = sk_res*0.5
        #a2 = scale
        return (skcoor*a2) + a1
#         return np.array([10, 10])
        #return (skcoor + sk_res*0.5)/scale
    
    def projekce(self,point, kalib_params, mode):
    
        if mode=='ransac':
            import cv2
            pt = np.float32([ [point[0],point[1]]]).reshape(-1,1,2)
            ip = cv2.perspectiveTransform(pt, kalib_params)
            proj_point = ip[0,0]    
         
        return proj_point 
    
    def changeOfIndex(self,aglob,fileList):
        if aglob == 0:
            aglob += 1
        else:    
            if aglob >= (len(fileList)-1):
                aglob = 0       
            else:
                aglob += 1            
        return aglob 
    
   
       
if __name__ == '__main__':
    pygame.init() 
    factory = WebSocketClientFactory(host, debug = False)
    factory.protocol = KinectClientProtocol
    connectWS(factory)
    reactor.run()
    print "konec"            