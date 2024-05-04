# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 22:25:48 2022

@author: nicho
"""
import cv2
import numpy as np
import imutils

def getAngleFromobject(x, WMiddle):
    HFOV = 130
    if x != -1:
        return ((x - WMiddle) / WMiddle) * (HFOV/2)
    else:
        return 0

def __calculateDistance(x1, y1, x2, y2):
    dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def getDistance(fittedHeight, knownHeight, focalLength):
    if(fittedHeight > 0):
        return round(((knownHeight * focalLength) / fittedHeight), 2)
    else:
        return 0

def getAngle(knownWidth, knownHeight, fittedHeight, fittedWidth):
    ratio = (knownWidth / knownHeight)
    w2 = fittedHeight * ratio
    if(knownWidth != 0 and w2 > fittedWidth):
        angle = (1 - (fittedWidth/w2)) * 90
    else:
        angle = 0
    return angle

def find_lines_yellow(filtered_image, image, name):
    gray = cv2.cvtColor(filtered_image,cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,10)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
    thresh = cv2.morphologyEx(th,cv2.MORPH_OPEN,kernel)
    row, col = thresh.shape[:2]
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE , cv2.CHAIN_APPROX_NONE)
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    
    rect = 0
    fittedHeight = 0
    fittedWidth = 0
    if len(sorted_contours) > 1:
        for pic, contour in enumerate(sorted_contours):
            area = cv2.contourArea(contour)
            if(area > 700 and area < ((image.shape[0] * image.shape[1])/1.5)):
                epsilon = 0.04*cv2.arcLength(contour,True)
                approx = cv2.approxPolyDP(contour,epsilon,True)
                if (len(approx)>4 and len(approx)<8) and len(contour) > 150:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    if any(box[i][1] > 100 for i in range(4)):
                        if name == "yellow":
                            cv2.drawContours(image,[box],0,(0,255,255),2)
                        elif name == "red":
                            cv2.drawContours(image,[box],0,(0,0,255),2)
                        else:
                            cv2.drawContours(image,[box],0,(255,0,0),2)
                        fittedHeight = __calculateDistance(box[0][0], box[0][1], box[1][0], box[1][1])
                        fittedWidth = __calculateDistance(box[2][0], box[2][1], box[1][0], box[1][1])
                        return fittedHeight, fittedWidth, rect[0][0]
    return fittedHeight, fittedWidth, -1

def find_lines_red(filtered_image, image, name):
    gray = cv2.cvtColor(filtered_image,cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(13,13))
    thresh = cv2.morphologyEx(th,cv2.MORPH_OPEN,kernel)
    row, col = thresh.shape[:2]
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE , cv2.CHAIN_APPROX_NONE)
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    
    rect = 0
    fittedHeight = 0
    fittedWidth = 0
    if len(sorted_contours) > 1:
        for pic, contour in enumerate(sorted_contours):
            contour = sorted_contours[1]
            area = cv2.contourArea(contour)
            if(area > 1000 and area < ((image.shape[0] * image.shape[1])/1.5)):
                epsilon = 0.04*cv2.arcLength(contour,True)
                approx = cv2.approxPolyDP(contour,epsilon,True)
                if (len(approx)>=4 and len(approx)<8) and len(contour) > 150:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    if any(box[i][1] > 100 for i in range(4)):
                        if name == "yellow":
                            cv2.drawContours(image,[box],0,(0,255,255),2)
                        elif name == "red":
                            cv2.drawContours(image,[box],0,(0,0,255),2)
                        else:
                            cv2.drawContours(image,[box],0,(255,0,0),2)
                        fittedHeight = __calculateDistance(box[0][0], box[0][1], box[1][0], box[1][1])
                        fittedWidth = __calculateDistance(box[2][0], box[2][1], box[1][0], box[1][1])
                        return fittedHeight, fittedWidth, rect[0][0]
    return fittedHeight, fittedWidth, -1

def find_lines_blue(filtered_image, image, name):
    box_list = []
    gray = cv2.cvtColor(filtered_image,cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(8,8))
    thresh = cv2.morphologyEx(th,cv2.MORPH_OPEN,kernel)
    row, col = thresh.shape[:2]
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE , cv2.CHAIN_APPROX_NONE)
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    
    rect = 0
    fittedHeight = 0
    fittedWidth = 0
    if len(sorted_contours) > 1:
        for pic, contour in enumerate(sorted_contours):
            area = cv2.contourArea(contour)
            if(area > 1000 and area < ((image.shape[0] * image.shape[1])/1.5)):
                approx = cv2.approxPolyDP(contour,0.04*cv2.arcLength(contour,True),True)
                if (len(approx)>4 and len(approx)<8) and len(contour) > 150:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    box_list.append(box)
                    if any(box[i][1] > 100 for i in range(4)): #and abs(box[0][1] - box[1][1]) < 25 and abs(box[2][1] - box[3][1]) < 25:
                    #if abs(box[0][0] - box[1][0]) < abs(box[1][1] - box[2][1])*1.5:
                        if name == "yellow":
                            cv2.drawContours(image,[box],0,(0,255,255),2)
                        elif name == "red":
                            cv2.drawContours(image,[box],0,(0,0,255),2)
                        else:
                            cv2.drawContours(image,[box],0,(255,0,0),2)
                        fittedHeight = __calculateDistance(box[0][0], box[0][1], box[1][0], box[1][1])
                        fittedWidth = __calculateDistance(box[2][0], box[2][1], box[1][0], box[1][1])
                        return fittedHeight, fittedWidth, rect[0][0]
    return fittedHeight, fittedWidth, -1

## For Distance Calculation :
knownHeight = 44
knownWidth = 55
ball_knownHeight = 6.5
ball_radius = 161.46
ball_diameter = ball_radius*2
known_distance = 10
focalLength = (ball_diameter * known_distance) / ball_knownHeight

def getObjectsInImage(img):
    #img = cv2.imread(i, cv2.IMREAD_COLOR)

    ## For angle calculation
    img = imutils.resize(img, width=640)
    MiddleOfImage = img.shape[1]/2
    
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    waitTime = 33
    while(1):
        img_detected = img.copy()
        a,b,r = 0,0,0
        distance = 0
        angle = 0
        DistanceFrom_Center = 0
        
        # BLUE GOALS : 
        lower = np.array([80, 45, 110])
        upper = np.array([100, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, np.ones((2, 2), np.uint8)) 
        mask = cv2.dilate(mask, np.ones((1, 1), np.uint8))
        img1 = cv2.bitwise_and(img,img, mask=mask)
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("blueGoalFilter", imutils.resize(img1, width=1000))
        fittedHeight, fittedWidth, center = find_lines_blue(img1, img_detected, "blue")
        
        DistanceFrom_Center = center - MiddleOfImage
        distanceGoalBlue = getDistance(fittedHeight, knownHeight, focalLength)
        angle = getAngle(knownWidth, knownHeight, fittedHeight,fittedWidth)
        angleGoalBlue = getAngleFromobject(center, MiddleOfImage)
        
        objectAngle = 0
        DistanceFrom_Center = 0
        distance = 0
        angle = 0

        #RED GOALS : 
        Y_goal_lower = np.array([170, 89, 0])
        Y_goal_upper = np.array([179, 255, 255])
        Y_goal_mask = cv2.inRange(hsv, Y_goal_lower, Y_goal_upper)
        Y_goal_mask = cv2.erode(Y_goal_mask, np.ones((2, 2), np.uint8)) 
        Y_goal_mask = cv2.dilate(Y_goal_mask, np.ones((20, 20), np.uint8))
        img1 = cv2.bitwise_and(img,img, mask=Y_goal_mask)
        Y_goal_lower = np.array([150, 130, 83])
        Y_goal_upper = np.array([179, 255, 255])
        Y_goal_mask = cv2.inRange(hsv, Y_goal_lower, Y_goal_upper)
        img1 = cv2.bitwise_and(img1,img1, mask=Y_goal_mask)
        #cv2.imshow("redGoalFilter1", imutils.resize(img1, width=1000))
        img1 = cv2.erode(img1, np.ones((2, 2), np.uint8)) 
        img1 = cv2.dilate(img1, np.ones((1, 1), np.uint8))
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("redGoalFilter2", imutils.resize(img1, width=1000))
        fittedHeight, fittedWidth, center = find_lines_red(img1, img_detected, "red")
        
        DistanceFrom_Center = center - MiddleOfImage
        distanceGoalRed = getDistance(fittedHeight, knownHeight, focalLength)
        angle = getAngle(knownWidth, knownHeight, fittedHeight,fittedWidth)
        angleGoalRed = getAngleFromobject(center, MiddleOfImage)
        
        objectAngle = 0
        DistanceFrom_Center = 0
        distance = 0
        angle = 0

        # YELLOW GOALS : 
        Y_goal_lower = np.array([16, 130, 100])
        Y_goal_upper = np.array([30, 255, 255])
        Y_goal_mask = cv2.inRange(hsv, Y_goal_lower, Y_goal_upper)
        Y_goal_mask = cv2.erode(Y_goal_mask, np.ones((2, 2), np.uint8)) 
        Y_goal_mask = cv2.dilate(Y_goal_mask, np.ones((1, 1), np.uint8))
        img1 = cv2.bitwise_and(img,img, mask=Y_goal_mask)
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("yellowGoalFilter", imutils.resize(img1, width=1000))
        fittedHeight, fittedWidth, center = find_lines_yellow(img1, img_detected, "yellow")
        
        DistanceFrom_Center = center - MiddleOfImage
        distanceGoalYellow = getDistance(fittedHeight, knownHeight, focalLength)
        angle = getAngle(knownWidth, knownHeight, fittedHeight,fittedWidth)
        angleGoalYellow = getAngleFromobject(center, MiddleOfImage)
        
        objectAngle = 0
        DistanceFrom_Center = 0
        distance = 0
        angle = 0
        a,b,r = -1,0,0
        
        # BLUE BALLS : 
        Y_goal_lower = np.array([90, 60, 60])
        Y_goal_upper = np.array([115, 255, 225])
        Y_goal_mask = cv2.inRange(hsv, Y_goal_lower, Y_goal_upper)
        Y_goal_mask = cv2.erode(Y_goal_mask, np.ones((6, 6), np.uint8)) 
        Y_goal_mask = cv2.dilate(Y_goal_mask, np.ones((40, 40), np.uint8))
        img1 = cv2.bitwise_and(img,img, mask=Y_goal_mask)
        Y_goal_lower = np.array([90, 61, 61])
        Y_goal_upper = np.array([115, 255, 255])
        Y_goal_mask = cv2.inRange(hsv, Y_goal_lower, Y_goal_upper)
        img1 = cv2.bitwise_and(img1,img1, mask=Y_goal_mask)
        img1 = cv2.erode(img1, np.ones((2, 2), np.uint8)) 
        img1 = cv2.dilate(img1, np.ones((4, 4), np.uint8))
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("blueAfterFilter", imutils.resize(img1, width=1000))
        
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        color = (255,0,0)
        sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
        for pic, contour in enumerate(sorted_contours):
            area = cv2.contourArea(contour)
            if(area > 80):
                epsilon = 0.04*cv2.arcLength(contour,True)
                approx = cv2.approxPolyDP(contour,epsilon,True)
                if len(approx)>=5 and len(approx)<=8:
                    k=cv2.isContourConvex(approx)
                    if k:
                        ((x, y), radius) = cv2.minEnclosingCircle(contour)
                        if (y > 100):
                            cv2.circle(img_detected, (int(x), int(y)), int(radius), color, 2)
                            x, y, w, h = cv2.boundingRect(contour)
                            a,b,r = x,y,radius
                            break
                        
        DistanceFrom_Center = a - MiddleOfImage
        distanceBallBlue = getDistance(r*2, ball_knownHeight, focalLength)
        angleBallBlue = getAngleFromobject(a, MiddleOfImage)
        #print(distance, objectAngle)
        
        objectAngle = 0
        DistanceFrom_Center = 0
        distance = 0
        a,b,r = -1,0,0
        
        # RED BALLS : 
        Y_goal_lower = np.array([154, 178, 80])
        Y_goal_upper = np.array([179, 247, 255])
        Y_goal_mask = cv2.inRange(hsv, Y_goal_lower, Y_goal_upper)
        Y_goal_mask = cv2.erode(Y_goal_mask, np.ones((1, 1), np.uint8)) 
        Y_goal_mask = cv2.dilate(Y_goal_mask, np.ones((20, 20), np.uint8))
        img1 = cv2.bitwise_and(img,img, mask=Y_goal_mask)
        Y_goal_lower = np.array([0, 100, 61])
        Y_goal_upper = np.array([179, 254, 255])
        Y_goal_mask = cv2.inRange(hsv, Y_goal_lower, Y_goal_upper)
        img1 = cv2.bitwise_and(img1,img1, mask=Y_goal_mask)
        img1 = cv2.erode(img1, np.ones((2, 2), np.uint8)) 
        img1 = cv2.dilate(img1, np.ones((3, 3), np.uint8))
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("redAfterFilter", imutils.resize(img1, width=1000))
        
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        color = (0,0,255)
        sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
        for pic, contour in enumerate(sorted_contours):
            area = cv2.contourArea(contour)
            if(area > 80):
                epsilon = 0.04*cv2.arcLength(contour,True)
                approx = cv2.approxPolyDP(contour,epsilon,True)
                if len(approx)>=5 and len(approx)<=8:
                    k=cv2.isContourConvex(approx)
                    if k:
                        ((x, y), radius) = cv2.minEnclosingCircle(contour)
                        if (y > 100):
                            cv2.circle(img_detected, (int(x), int(y)), int(radius), color, 2)
                            x, y, w, h = cv2.boundingRect(contour)
                            a,b,r = x,y,radius
                            break
                        
        DistanceFrom_Center = a - MiddleOfImage
        distanceBallRed = getDistance(r*2, ball_knownHeight, focalLength)
        angleBallRed = getAngleFromobject(a, MiddleOfImage)
        
        objectAngle = 0
        DistanceFrom_Center = 0
        distance = 0
        a,b,r = -1,0,0
        
        # YELLOW BALLS : 
        Y_goal_lower = np.array([19, 101, 111])
        Y_goal_upper = np.array([28, 255, 255])
        Y_goal_mask = cv2.inRange(hsv, Y_goal_lower, Y_goal_upper)
        Y_goal_mask = cv2.erode(Y_goal_mask, np.ones((2, 2), np.uint8)) 
        Y_goal_mask = cv2.dilate(Y_goal_mask, np.ones((3, 3), np.uint8))
        img1 = cv2.bitwise_and(img,img, mask=Y_goal_mask)
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("yellowAfterFilter", imutils.resize(img1, width=1000))
        
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        color = (0,255,255)
        sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
        for pic, contour in enumerate(sorted_contours):
            area = cv2.contourArea(contour)
            if(area > 80):
                epsilon = 0.04*cv2.arcLength(contour,True)
                approx = cv2.approxPolyDP(contour,epsilon,True)
                if len(approx)>=5 and len(approx)<=8:
                    k=cv2.isContourConvex(approx)
                    if k:
                        ((x, y), radius) = cv2.minEnclosingCircle(contour)
                        if (y > 100):
                            cv2.circle(img_detected, (int(x), int(y)), int(radius), color, 2)
                            x, y, w, h = cv2.boundingRect(contour)
                            a,b,r = x,y,radius
                            break
                        
        DistanceFrom_Center = a - MiddleOfImage
        distanceBallYellow = getDistance(r*2, ball_knownHeight, focalLength)
        angleBallYellow = getAngleFromobject(a, MiddleOfImage)
        
        objectAngle = 0
        DistanceFrom_Center = 0
        distance = 0
        return [img_detected, distanceBallYellow, distanceBallRed, distanceBallBlue, distanceGoalYellow, distanceGoalRed, distanceGoalBlue, angleGoalYellow, angleGoalRed, angleGoalBlue, angleBallYellow, angleBallRed, angleBallBlue]
