
import numpy as np
import cv2
import urllib
import socket 

# setting a socket to send message to pi3:

TCP_IP = '192.168.1.4'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = 'MATCH!'
QUIT = 'quit!'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# Matching stopsign:

detector=cv2.xfeatures2d.SIFT_create()
FLANN_INDEX_KDITREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})

trainImg=cv2.imread('stopSign.png',0)
trainKP,trainDesc=detector.detectAndCompute(trainImg,None)

url = 'http://192.168.1.2:8080/shot.jpg'
cv2.namedWindow('result',cv2.WINDOW_NORMAL)
cv2.resizeWindow('result', 600,400)    
#cam = cv2.VideoCapture(1)
while True:
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
      


    QueryImgBGR=img
    QueryImg=cv2.cvtColor(QueryImgBGR,cv2.COLOR_BGR2GRAY)
    queryKP,queryDesc=detector.detectAndCompute(QueryImg,None)
    bf = cv2.BFMatcher()    
    matches=bf.knnMatch(queryDesc,trainDesc,k=2)    
    goodMatch=[]
    for m,n in matches:
        if(m.distance<0.75*n.distance):
            goodMatch.append(m)

    MIN_MATCH_COUNT=30
    if(len(goodMatch)>=MIN_MATCH_COUNT):
        
        tp=[]
        qp=[]

        for m in goodMatch:
            tp.append(trainKP[m.trainIdx].pt)
            qp.append(queryKP[m.queryIdx].pt)

        tp,qp=np.float32((tp,qp))

        H,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)

        h,w=trainImg.shape
        trainBorder=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
        queryBorder=cv2.perspectiveTransform(trainBorder,H)
        cv2.polylines(QueryImgBGR,[np.int32(queryBorder)],True,(0,255,0),5)
        print "Match!!! -> %d/%d"%(len(goodMatch),MIN_MATCH_COUNT)
        s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        print 'data received',data
    else:
        print "Not Enough match found- %d/%d"%(len(goodMatch),MIN_MATCH_COUNT)
    
    cv2.imshow('result',QueryImgBGR)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        s.send(QUIT)
        break
s.close()
exit(0)
    
   








