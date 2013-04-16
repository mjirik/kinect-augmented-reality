# -*- coding: utf-8 -*-

# Ukázka kalibrace kamery pomocí OpenCV
#https://github.com/abidrahmank/OpenCV-Python/blob/master/Other_Examples/camera_calibration.py

def kalibrace_opencv():
    import numpy as np
    import cv
    obj_pts = [[0,0,0],[1,0,0],[1,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]]
    img_pts = [[120,729],[434,980],[897,795],[88,210],[429,368],[938,237],[552,124]]
    #n_images=1#no of boards
    # board_w=int(sys.argv[1])# number of horizontal corners
    #board_h=int(sys.argv[2])# number of vertical corners
    n_pts = len(obj_pts)
    #board_n=board_w*board_h# no of total corners
    #board_sz=(board_w,board_h)#size of board


    image_points=cv.CreateMat(n_pts,2,cv.CV_32FC1)
    object_points=cv.CreateMat(n_pts,3,cv.CV_32FC1)
# počty bodů v jednotlivých obrazech, ( v našem případě máme obraz jen jeden)
    n_images = 1
    point_counts=cv.CreateMat(n_images,1,cv.CV_32SC1)
    intrinsic_matrix=cv.CreateMat(3,3,cv.CV_32FC1)
    #distortion_coefficient=cv.CreateMat(5,1,cv.CV_32FC1)
    distortion_coefficient=cv.CreateMat(4,1,cv.CV_32FC1)

    # only if n_images == 1
    cv.Set2D(point_counts,0,0, len(obj_pts))

    for j in range(n_pts):
        cv.Set2D(image_points,j,0,img_pts[j][0])
        cv.Set2D(image_points,j,1,img_pts[j][1])
        cv.Set2D(object_points,j,0,obj_pts[j][0])
        cv.Set2D(object_points,j,1,obj_pts[j][1])
        cv.Set2D(object_points,j,2,obj_pts[j][2])



#creation of memory stor        ages

    #obj_pts = np.zeros([n_pts,3])
    #img_pts = np.zeros([n_pts,2])


    #obj_pts = [[0,0,0],[1,0,0],[1,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]]
    #img_pts = [[120,729],[434,980],[897,795],[88,210],[429,368],[938,237],[552,124]]

    #obj_pts_np = np.array(obj_pts).astype(np.float)
    #img_pts_np = np.array(img_pts).astype(np.float)
    #

    #img_pts = cv.fromarray(img_pts_np, allowND = True)

    #obj_pts = cv.fromarray(obj_pts_np, True)

    #img_sz = cv.fromarray(np.array([[1000,1000]]).astype(np.int16))
    img_sz = (1000,1000)

    cv.Set2D(intrinsic_matrix,0,0,1.0)
    cv.Set2D(intrinsic_matrix,1,1,1.0)

    rcv = cv.CreateMat(n_images, 3, cv.CV_64FC1)
    tcv = cv.CreateMat(n_images, 3, cv.CV_64FC1)

    import pdb; pdb.set_trace()

    cv.CalibrateCamera2(object_points, image_points,point_counts,img_sz,intrinsic_matrix,distortion_coefficient,rcv,tcv,0 )
    #cv.InitIntrinsicParams2D(object_points, image_points,point_counts,img_sz,intrinsic_matrix,1)#,distortion_coefficient,rcv,tcv,0 )

    import pdb; pdb.set_trace()

    print "ahoj"


def kalibrace_cv2():
    # http://stackoverflow.com/questions/10022568/opencv-2-3-camera-calibration
    import cv2
    from cv2 import cv
    import numpy as np

    #obj_points = [[-9.7,3.0,4.5],[-11.1,0.5,3.1],[-8.5,0.9,2.4],[-5.8,4.4,2.7],[-4.8,1.5,0.2],[-6.7,-1.6,-0.4],[-8.7,-3.3,-0.6],[-4.3,-1.2,-2.4],[-12.4,-2.3,0.9],[-14.1,-3.8,-0.6],[-18.9,2.9,2.9],[-14.6,2.3,4.6],[-16.0,0.8,3.0],[-18.9,-0.1,0.3],[-16.3,-1.7,0.5],[-18.6,-2.7,-2.2]]
    #img_points = [[993.0,623.0],[942.0,705.0],[1023.0,720.0],[1116.0,645.0],[1136.0,764.0],[1071.0,847.0],[1003.0,885.0],[1142.0,887.0],[886.0,816.0],[827.0,883.0],[710.0,636.0],[837.0,621.0],[789.0,688.0],[699.0,759.0],[768.0,800.0],[697.0,873.0]]
# moje testovaci data pochazeji z obrazku, nula je vlevo dole
# http://upload.wikimedia.org/wikipedia/commons/0/02/Face_colored_cube.png
    obj_points = [[0,0,0],[1,0,0],[1,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]]
    img_points = [[120,729],[434,980],[897,795],[88,210],[429,368],[938,237],[552,124]]

    obj_points = np.array(obj_points,'float32')
    img_points = np.array(img_points,'float32')

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

    retval,camera_matrix,dist_coefs,rvecs,tvecs = cv2.calibrateCamera([obj_points],[img_points],size,camera_matrix,dist_coefs,flags=cv.CV_CALIB_USE_INTRINSIC_GUESS)
    #print retval
    #print camera_matrix
    #print dist_coefs

    #print rvecs
    #print tvecs
    #import pdb; pdb.set_trace()


    #pokusny_bod = [[-9.7,3.0,4.6]]
    pokusny_bod = [[1,0.5,0]]
    ip, jacob = cv2.projectPoints(np.array(pokusny_bod), 
            np.array(rvecs), 
            np.array(tvecs), 
            np.array(camera_matrix), 
            np.array(dist_coefs))
    print "bod by mel byt kolem 690, 860"
    print 'ip = ', ip
    #print 'jacob' , jacob


if __name__ == '__main__':
    kalibrace_cv2()
