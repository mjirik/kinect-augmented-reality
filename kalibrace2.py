# -*- coding: cp1250 -*-

'''
Created on 14.3.2013

@author: misa
'''

import pickle
import numpy as np
import os, sys, pygame
import autobahn
import twisted
import random
from pygame.locals import *
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, \
                               WebSocketClientProtocol, \
                               connectWS
import json


#Window_height = 700
#Window_width = 1300
Window_height = 500
Window_width = 1000
LOOP_TIME = 0.1

host = "ws://147.228.47.141:9002" 

data={}

bod1="red_dot.png"
bg="black.png"

print "neco"
def Haffine_from_points(fp,tp):
    """
    find H, affine transformation, such that 
        tp is affine transf of fp
    """
    if fp.shape != tp.shape:
        raise RuntimeError, 'number of points do not match'

    #condition points
    #-from points-
    m = np.mean(fp[:2], axis=1)
    maxstd = np.max(np.std(fp[:2], axis=1))
    C1 = np.diag([1/maxstd, 1/maxstd, 1]) 
    C1[0][2] = -m[0]/maxstd
    C1[1][2] = -m[1]/maxstd
    fp_cond = np.dot(C1,fp)

    #-to points-
    m = np.mean(tp[:2], axis=1)
    C2 = C1.copy() #must use same scaling for both point sets
    C2[0][2] = -m[0]/maxstd
    C2[1][2] = -m[1]/maxstd
    tp_cond = np.dot(C2,tp)

    #conditioned points have mean zero, so translation is zero
    A = np.concatenate((fp_cond[:2],tp_cond[:2]), axis=0)
    U,S,V = np.linalg.svd(A.T)

    #create B and C matrices as Hartley-Zisserman (2:nd ed) p 130.
    tmp = V[:2].T
    B = tmp[:2]
    C = tmp[2:4]

    tmp2 = np.concatenate((np.dot(C,np.linalg.pinv(B)),np.zeros((2,1))), axis=1) 
    H = np.vstack((tmp2,[0,0,1]))

    #decondition
    H = np.dot(np.linalg.inv(C2),np.dot(H,C1))
    return H / H[2][2]

class EchoClientProtocol(WebSocketClientProtocol):
    def sendHello(self):
        self.sendMessage("skeleton")
            
    def send_message(self):
        self.sendMessage("skeleton")
 
    def onOpen(self):
        self.kalibrace_init()
        self.sendHello()
        self.stav = 'kalibrace'
        self.msg = ''
        reactor.callLater(LOOP_TIME, self.tick)
    
    def update(self,body):
        
        self.body = body    
 
    
    def onMessage(self, msg, binary):
        
        print "Got echo: " + msg
        
        self.msg = msg
        
        if len(msg) > 2:
            data = json.loads( msg )
         
            self.body = data[0]
            
            if self.stav == 'kalibrace':
                self.kalibrace_run()
            
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
                reactor.stop()
                
        if self.stav == 'kalibrace':
            self.bod(x = self.kalibPtsX[self.actualPointInd], y = self.kalibPtsY[self.actualPointInd])
        
        pygame.display.flip()
        reactor.callLater(LOOP_TIME, self.tick)
        
    def bod(self, x=None, y=None):    
        
        if x == None:
            self.px = random.randint(Window_width*0.05,Window_width*0.9)
            self.py = random.randint(Window_height*0.05,Window_height*0.9)
        else:
            self.px = x
            self.py = y
            
        self.background=pygame.image.load(bg).convert()
        self.point=pygame.image.load(bod1).convert_alpha()
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.point, (x,y))
        pygame.display.update()           
        
        
    def kalibrace_init(self, new_kalib = False):
        pygame.init()
        pygame.display.set_caption('Vykresleni bodu')
        self.size = self.width, self.height = Window_width,Window_height
        self.screen=pygame.display.set_mode((self.size),0,32)
        self.background=pygame.image.load(bg).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.size)
        self.point=pygame.image.load(bod1).convert_alpha()
        
        r=self.background.get_size()
        print r
        if pygame.font:
            pismo = pygame.font.Font(None, 28)
            text = pismo.render(u"Lovou ruku přiložte na zobrazovaný bod a pravou zvedněte nad hlavu",1, (10, 10, 10))
            textPozice = text.get_rect()
            textPozice.centerx = self.screen.get_rect().centerx
            self.screen.blit(text, textPozice)
            
            
            
        self.povoleno = True
        
        
        
        if new_kalib:
            self.nPoints = 14
            self.kalibPtsX = [
                              50, 
                              Window_width - 50,
                              Window_width - 50,
                              80,
                              90,
                              Window_width - 80,
                              Window_width - 70,
                              60,
                              Window_width - 50,
                              80,
                              90,
                              Window_width - 80,
                              Window_width - 70,
                              60,
                              1
                              ]
            self.kalibPtsY = [
                              50,
                              50,
                              Window_height - 50,
                              Window_height - 50,
                              80,
                              50,
                              Window_height - 80,
                              Window_height - 50,
                              70,
                              80,
                              Window_height - 50,
                              Window_height - 90,
                              90,
                              40,
                              1
                              ]
            self.bod(x = self.kalibPtsX[0], y = self.kalibPtsY[0])
        else:
            self.nPoints = 4
            self.kalibPtsX = [50, Window_width - 50,  Window_width - 50, 50, 1]
            self.kalibPtsY = [50, 50, Window_height - 50, Window_height - 50, 1]
            self.bod(x = self.kalibPtsX[0], y = self.kalibPtsY[0])
        
        self.actualPointInd = 0
        self.projPts = [0]*self.nPoints
        self.kinectPts = [0]*self.nPoints
        
        self.new_kalib = new_kalib
        pass
    
    def kalibrace_run(self):
        head = self.body["Head"]
        rhand = self.body["RightHand"]
        lhand = self.body["LeftHand"]
        #lfoot = self.body["LeftFoot"]
        #rknee = self.body["RightKnee"]
          
        if int(rhand["Y"]) > int(head["Y"]) and self.povoleno:
            x1 = int(lhand["X"])
            y1 = int(lhand["Y"])
            z1 = int(lhand["Z"])
            
            self.projPts[self.actualPointInd] = [self.px, self.py]
            self.kinectPts[self.actualPointInd] = [x1, y1, z1]
            self.actualPointInd = self.actualPointInd + 1
            self.povoleno = False
            print "x1 =",  x1
            print "y1 =",  y1
                 
        if int(rhand["Y"]) < int(head["Y"]):
            self.povoleno = True     
            
        print self.projPts
        print self.kinectPts
        print self.actualPointInd
        print self.povoleno
        
        if self.new_kalib:
            import cv2
            from cv2 import cv
            # nova kalibrace pomoci opencv
            if self.actualPointInd == self.nPoints:
            
                obj_points = np.array(self.kinectPts,'float32')
                img_points = np.array(self.projPts,'float32')
            
                #w = 1680
                #h = 1050
                size = (self.width,self.height)
            
                w = 1680
                h = 1050
                size = (w,h)
                camera_matrix = np.zeros((3, 3),'float32')
                camera_matrix[0,0]= 2200.0
                camera_matrix[1,1]= 2200.0
                camera_matrix[2,2]=1.0
                camera_matrix[0,2]=750.0
                camera_matrix[1,2]=750.0 
            
                dist_coefs = np.zeros(4,'float32')
                
                #retval,camera_matrix,dist_coefs,rvecs,tvecs
                print obj_points
                print img_points
                print size
                retval,camera_matrix,dist_coefs,rvecs,tvecs = cv2.calibrateCamera([obj_points],[img_points],size,camera_matrix,dist_coefs,flags=cv.CV_CALIB_USE_INTRINSIC_GUESS)
                
                kalib_params = (retval,camera_matrix,dist_coefs,rvecs,tvecs)
                with open('matice_kal2', 'wb') as f:
                    pickle.dump(kalib_params,f)
                print "Kalibrace dokoncena"    
            pass
        else:
            
                
            
                
            if self.actualPointInd == 4:
                #self.stav = 'sledovani'       
                 
                #print self.projPts
                fp = np.array([[self.projPts[0][0],self.projPts[1][0],self.projPts[2][0 ],self.projPts[3][0]],[self.projPts[0][1],self.projPts[1][1],self.projPts[2][1],self.projPts[3][1]],[1,1,1,1]])
                tp = np.array([[self.kinectPts[0][0],self.kinectPts[1][0],self.kinectPts[2][0],self.kinectPts[3][0]],[self.kinectPts[0][1],self.kinectPts[1][1],self.kinectPts[2][1],self.kinectPts[3][1]],[1,1,1,1]])
                self.H=Haffine_from_points(fp, tp)
                print fp
                print self.H
                
                with open('matice_kal2', 'wb') as f:
                    pickle.dump(self.H,f)
                print "Kalibrace dokoncena" 
                
                
def projekce(point, kalib_params, new_kalib = False):
    
    if new_kalib:
        import cv2
        retval,camera_matrix,dist_coefs,rvecs,tvecs = kalib_params
        #point = [[280,-23.0,641]]
        point_np = np.array([point], dtype = np.float64)
        print point_np.dtype
        print point_np
        
        ip, jacob = cv2.projectPoints(point_np, 
            np.array(rvecs), 
            np.array(tvecs), 
            np.array(camera_matrix), 
            np.array(dist_coefs))
        
        proj_point = ip[0,0]
    else:
        point[2]=1
        proj_point = np.dot(kalib_params, point)
        
    return proj_point
    
                
if __name__ == '__main__':
    
    pygame.init() 
    factory = WebSocketClientFactory(host, debug = False)
    factory.protocol = EchoClientProtocol
    connectWS(factory)
    reactor.run()
            
