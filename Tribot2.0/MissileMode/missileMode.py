import cv2
import serial
import time
import os
import numpy as np
print(cv2.__version__)

def nothing():
    pass

dispW=680
dispH=420
flip=2
#camSet='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#camSet ='v4l2src device=/dev/video1 ! video/x-raw,width='+str(width)+',height='+str(height)+',framerate=24/1 ! videoconvert ! appsink'
cv2.namedWindow('TrackBars')
cv2.createTrackbar('hueLower', 'TrackBars', 110 , 179, nothing)
cv2.createTrackbar('hueHigher', 'TrackBars', 179 , 179, nothing)

cv2.createTrackbar('satLower', 'TrackBars', 100 , 255, nothing)
cv2.createTrackbar('satHigher', 'TrackBars', 255 , 255, nothing)

cv2.createTrackbar('valLower', 'TrackBars', 100 , 255, nothing)
cv2.createTrackbar('valHigher', 'TrackBars', 255 , 255, nothing)

cv2.createTrackbar('hueLower2', 'TrackBars', 0 , 179, nothing)
cv2.createTrackbar('hueHigher2', 'TrackBars', 10 , 179, nothing)

objx = 0
objy = 0

last_sent_time = 0  # Track the last time a command was sent
send_interval = 0.2  # Minimum time (in seconds) between sends


# Function to find the correct serial port
def find_arduino_port():
    ports = [port for port in os.listdir('/dev') if 'ttyUSB' in port or 'ttyACM' in port]
    if ports:
        return f"/dev/{ports[0]}"
    else:
        raise IOError("No Arduino found")

# Initialize serial connection to Arduino
try:
    arduino_port = find_arduino_port()
    arduino = serial.Serial(arduino_port, 115200)
    time.sleep(2)  # Wait for Arduino to initialize
except IOError as e:
    print(f"Error: {e}")
    exit(1)


last_command = None  # Track last command

def send_to_arduino(command):
    global last_sent_time, last_command

    if command != last_command or (time.time() - last_sent_time) > send_interval:
        try:
            arduino.write(f"{command}\n".encode())  # Send command with newline
            print(f"Sent: {command}")
            last_sent_time = time.time()
            last_command = command
        except serial.SerialException as e:
            print(f"Serial write failed: {e}")

cam = cv2.VideoCapture('/dev/video0')
cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)  # Reduce frame width
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)  # Reduce frame height
while True:
    _, frame = cam.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hueLow = cv2.getTrackbarPos('hueLower','TrackBars')
    hueHigh = cv2.getTrackbarPos('hueHigher','TrackBars')

    satLow = cv2.getTrackbarPos('satLower','TrackBars')
    satHigh = cv2.getTrackbarPos('satHigher','TrackBars')

    valLow = cv2.getTrackbarPos('valLower','TrackBars')
    valHigh = cv2.getTrackbarPos('valHigher','TrackBars')

    hueLow2 = cv2.getTrackbarPos('hueLower2','TrackBars')
    hueHigh2 = cv2.getTrackbarPos('hueHigher2','TrackBars')

    l_b=np.array([hueLow,satLow,valLow])
    h_b=np.array([hueHigh,satHigh,valHigh])

    l_b2=np.array([hueLow2,satLow,valLow])
    h_b2=np.array([hueHigh2,satHigh,valHigh])

    FGmask = cv2.inRange(hsv,l_b,h_b)
    FGmask2 = cv2.inRange(hsv, l_b2,h_b2)
    FGmaskComp = cv2.add(FGmask,FGmask2)
    BGmask = cv2.bitwise_not(FGmaskComp)

    FG= cv2.bitwise_and(frame,frame, mask = FGmaskComp)
    BG= cv2.cvtColor(BGmask,cv2.COLOR_GRAY2BGR)
    final = cv2.add(FG,BG) 

    contours, _ = cv2.findContours(FGmaskComp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  # Unpack only two values
    contours = sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
    if len(contours) <= 0 or cv2.contourArea(contours[0]) < 50:
        objx = 0
        objy = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        (x,y,w,h)=cv2.boundingRect(cnt)
        if(area >= 50):
            #cv2.drawContours(frame,[cnt],0,(255,0,0),3)
            cv2.line(frame, (0, int(y+(h/2))), (dispW, int(y+(h/2))), (0,255,0), 2)
            cv2.line(frame, (int(x+(w/2)), 0), (int(x+(w/2)), dispH), (0,255,0), 2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
            objx = int(x+(w/2))
            objy = int(y+(h/2))
            print(f'X: {objx} Y: {objy}')
            
    #cv2.drawContours(frame,contours,0,(255,0,0),3 )

    # Determine the command to send to the Arduino
    command = objx
    # Send the command to the Arduino
    current_time = time.time()
    if (current_time - last_sent_time) > send_interval:
        print(f"Command: {command}")
        send_to_arduino(command)
        last_sent_time = current_time  # Update last sent time
    

    cv2.imshow('myCam',frame)

    cv2.imshow('FGmaskComp',FGmaskComp)
    cv2.moveWindow('myCam',0,0)
    del hsv, FGmask, FGmask2, FGmaskComp, BGmask, FG, BG, final

    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
# Close the serial connection
arduino.close()