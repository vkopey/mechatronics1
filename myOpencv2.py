#-*- coding: utf-8 -*-
import numpy as np
import cv2
from skimage.feature import canny
from skimage.transform import hough_circle, hough_circle_peaks
from skimage import io
import pyfirmata

board=pyfirmata.Arduino('COM13')
#print board.get_firmata_version()
servo=board.get_pin('d:9:s')

def detObj(image):
    edges = canny(image, sigma=2, low_threshold=10, high_threshold=20)
    #io.imsave("edges.bmp", edges)
    hough_radii = [16]
    hough_res = hough_circle(edges, hough_radii)
    accums, cx, cy, r = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=1)
    return cx, cy, r
    
cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cx, cy, r=detObj(gray)
    print cx, cy, r
    #cv2.circle(gray, (cx, cy), r, 255, -1)
    
    servo.write(cx/20)
    
    #cv2.imshow('frame',gray)
    #if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
board.exit()