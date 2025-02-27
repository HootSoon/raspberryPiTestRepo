import cv2
print(cv2.__version__)
width=1280
height=720
flip=2
#camSet='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#camSet ='v4l2src device=/dev/video1 ! video/x-raw,width='+str(width)+',height='+str(height)+',framerate=24/1 ! videoconvert ! appsink'
eye_Cascade = cv2.CascadeClassifier("/home/hootsoon/Desktop/raspiRepo/raspberryPiTestRepo/Pi5_1/xmlFiles/eyes/eyes.xml")

cam=cv2.VideoCapture(0)
while True:
    _, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_Cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in eyes:
        cv2.rectangle(frame,(x,y),(x+w,y+h), (0,0,255))
    cv2.imshow('myCam',frame)
    cv2.moveWindow('myCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()