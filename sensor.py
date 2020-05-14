"""
Adapted from https://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
and https://thedatafrog.com/en/articles/human-detection-video/

Able to detect a person in front of the camera.
"""

import cv2 
import imutils 

   
# from datafrog, pyimagesearch
def detect():
    hog = cv2.HOGDescriptor() 
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
       
    cap = cv2.VideoCapture(0) 
       
    while cap.isOpened(): 
        
        ret, image = cap.read() 
        if ret: 
            image = imutils.resize(image,
                                   width=min(400, image.shape[1])) 
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            (regions, _) = hog.detectMultiScale(gray,
                                                winStride=(4, 4),
                                                padding=(4, 4),
                                                scale=1.05) 
           
            if len(regions) != 0: 
                return True
            
        else: 
            break
