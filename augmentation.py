import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import logging
#import datetime

def rotated_skewed_search(image, crop):
    """
    Matches features of rotated images with actual image

    Parameters
    ----------
    :param image : original image
    :param crop: cropped image
    :return: [coordinates] or None
    """

    sift = cv2.xfeatures2d.SIFT_create()

    timg = cv2.imread(image)
    timggray= cv2.cvtColor(timg,cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5,5), np.uint8)
    timggray = cv2.erode(timggray, kernel, iterations=1)
    tkp,tdes = sift.detectAndCompute(timggray,None)

    qimg = cv2.imread(crop)
    qimggray = cv2.cvtColor(qimg,cv2.COLOR_BGR2GRAY)
 
    qkp,qdes = sift.detectAndCompute(qimggray, None)
 
    FLANN_INDEX_KDITREE=0
    index_params=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
    search_params = dict(checks = 50)
    flann=cv2.FlannBasedMatcher(index_params,search_params)
    matches=flann.knnMatch(tdes,qdes,k=2)
    goodMatch=[]
    for m_n in matches:
        if len(m_n) != 2:
            continue
        m, n = m_n
        if(m.distance<0.75*n.distance):
            goodMatch.append(m)
    MIN_MATCH_COUNT = 30
    if (len(goodMatch) >= MIN_MATCH_COUNT):
        tp = []
        qp = []

        for m in goodMatch:
            tp.append(tkp[m.queryIdx].pt)
            qp.append(qkp[m.trainIdx].pt)
 
        tp, qp = np.float32((tp, qp))
        
        H, status = cv2.findHomography(tp, qp, cv2.RANSAC, 3.0)
        
        img_object = timg

        obj_corners = np.empty((4,1,2), dtype=np.float32)
        obj_corners[0,0,0] = 0
        obj_corners[0,0,1] = 0
        obj_corners[1,0,0] = qimg.shape[1]
        obj_corners[1,0,1] = 0
        obj_corners[2,0,0] = qimg.shape[1]
        obj_corners[2,0,1] = qimg.shape[0]
        obj_corners[3,0,0] = 0
        obj_corners[3,0,1] = qimg.shape[0]
        
        h = timg.shape[0]
        w = timg.shape[1]

        #trainBorder = np.float32([[[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]])
        #queryBorder = cv2.perspectiveTransform(trainBorder, H)
        #scene_corners = None
        
        print("------", H)
        if(H.size() != 0):
            if (H != 0).any():
                print("----------------------Test******************************")
                scene_corners = cv2.perspectiveTransform(obj_corners, H)
                print(scene_corners)
                return [scene_corners[0,0,0],scene_corners[0,0,1], scene_corners[3,0,0], scene_corners[3,0,1]]
            #  print(H)
        return None
              
        #print('corner 0: {}, {}'.format(scene_corners[0,0,0], scene_corners[0,0,1]))
        #print('corner 1: {}, {}'.format(scene_corners[1,0,0], scene_corners[1,0,1]))
        #print('corner 2: {}, {}'.format(scene_corners[2,0,0], scene_corners[2,0,1]))
        #print('corner 3: {}, {}'.format(scene_corners[3,0,0], scene_corners[3,0,1]))
        

        #cv2.polylines(qimg, [np.int32(queryBorder)], True, (0, 255, 0), 5)
        #cv2.imshow('result', qimg)

        #cv2.polylines(qimg, [np.int32(queryBorder)], True, (0, 255, 0), 5)
        #cv2.polylines(timg, [np.int32(queryBorder)], True, (0, 255, 0), 5)
        #cv2.imwrite("cropped_"+str(datetime.datetime.now())+".jpg", timg)

        #cv2.rectangle(timg, c, b, (0, 0, 255), 2)

        #cv2.imwrite('result2.png', timg)
        #plt.imshow(qimg, 'gray'), plt.show()
    else:
        logging.error('Augmentation: Coordinates not found')
        return None

#print(rotated_skewed_search('./data/images/d469bcc8-d501-5b75-81b0-00eabb7a2238.jpg', './data/crops/afb8cde2-0e4f-55d6-a1ae-5e65567ed1ab.jpg'))