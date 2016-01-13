import cv2
import numpy as np
import math
import win32api,win32con
from cv2 import imshow, waitKey, destroyAllWindows

ORANGE_MIN = np.array([5, 50, 50],np.uint8)
ORANGE_MAX = np.array([15, 255, 255],np.uint8)
ci=0
clickk=False
cap=cv2.VideoCapture(0)
while True:
    
    ret,img=cap.read()
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV_FULL)

    frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
    #frame_threshed=cv2.erode(frame_threshed,element,iterations=5)
    frame_threshed = cv2.dilate(frame_threshed,element,iterations=5)
    
    frame_threshed = cv2.erode(frame_threshed,element, iterations=3)
    frame_threshed = cv2.dilate(frame_threshed,element, iterations=6)
    #mask = cv2.erode(mas,element,iterations=3)
    #mask=cv2.dilate(mask,element,iterations=1)
    blurred = cv2.GaussianBlur(frame_threshed,(55,55),0)
   
    _,fin=cv2.threshold(blurred, 127, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    _,fin1=cv2.threshold(fin, 127, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(fin1.copy(),cv2.RETR_TREE, \
            cv2.CHAIN_APPROX_NONE)
    max_area = -1
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
    print ci
    cnt=contours[ci]
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),0)
    hull = cv2.convexHull(cnt)
    cv2.drawContours(img,[cnt],0,(0,255,0),0)
    cv2.drawContours(img,[hull],0,(0,0,255),0)
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0
    
    no_of_fingers=0
    
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
        #print topmost
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        
        if angle <= 90:
            count_defects += 1
            cv2.circle(img,far,1,[0,0,255],-1)
       
        cv2.line(img,start,end,[0,255,0],2)
        cv2.circle(img,topmost,5,[0,0,255],-1)
        
    if count_defects == 1:
        cv2.putText(img,"2", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        no_of_fingers=2
    elif count_defects == 2:
        stri = "3"
        no_of_fingers=3
        print stri
        cv2.putText(img, stri, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 3:
        cv2.putText(img,"4", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        no_of_fingers=4
    elif count_defects == 4:
        cv2.putText(img,"5", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        no_of_fingers=5
    elif count_defects==0 and angle>=134 :
        cv2.putText(img,"1", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        #cv2.putText(img,str(angle), (50,150), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        no_of_fingers=1
    if no_of_fingers==1:
        x=topmost[0]
        y=topmost[1]
        win32api.SetCursorPos(topmost)
    elif (clickk==True and no_of_fingers==2):
        x=topmost[0]
        y=topmost[1]
        a,b=win32api.GetCursorPos()
        win32api.SetCursorPos(topmost)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,a,b,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,a,b,0,0)
        clickk=False
    
    imshow("Window 1",fin1)
    imshow("Window 2",img)
    k=waitKey(30)
    if k==27:
        break
    elif k==99:
        clickk=True
        
cap.release()
destroyAllWindows()