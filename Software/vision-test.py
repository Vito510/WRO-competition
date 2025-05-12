import cv2
import numpy as np
from scipy.ndimage import label

cam = cv2.VideoCapture(2)

frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

def draw_contour(mask, color):
    threshold = 4000
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest = 0
    best = None
    
    
    for cnt in contours:
        area = cv2.contourArea(cnt) 
        if area > largest and area > threshold:
            largest = area
            best = cnt
    if best is not None:
        cv2.rectangle(frame, cv2.boundingRect(best), color, 2)
        x, y, w, h = cv2.boundingRect(best)
        cv2.putText(frame, f"Area: {largest}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    

while True:
    ret, frame = cam.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    g_mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))
    r_mask = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
    draw_contour(g_mask, (0,255,0))
    draw_contour(r_mask, (0,0,255))


    
    cv2.imshow('Camera', frame)


    if cv2.waitKey(1) == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()