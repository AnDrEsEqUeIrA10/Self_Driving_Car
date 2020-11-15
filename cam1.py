import numpy as np
import cv2
import urllib

url = 'http://192.168.50.45:8080/shot.jpg'

cv2.namedWindow('image',cv2.WINDOW_NORMAL)

#cam=cv2.VideoCapture(1)
cv2.resizeWindow('image', 600,400)
while True:
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    #_,img=cam.read()
    cv2.imshow('image',img)   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
exit(0)
#cv2.destroyAllWindows()
#cv2.VideoCapture(1).release()
    

