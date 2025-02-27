import cv2
from PIL import Image
import serial
import time
import os

# Function to find the correct serial port
def find_arduino_port():
    ports = [port for port in os.listdir('/dev') if 'ttyUSB' in port or 'ttyACM' in port]
    if ports:
        return f"/dev/{ports[0]}"
    else:
        raise IOError("No Arduino found")

# SERIAL CODE
def send_to_arduino(command):
    try:
        arduino.write(command.encode())
    except serial.SerialException as e:
        print(f"Serial write failed: {e}")
        handle_serial_error()

def move_servo(servo, angle):
    command = f"{servo} {angle}\n"
    try:
        arduino.write(command.encode())
        print("Sent:", command.strip())
        time.sleep(0.01)  # Wait for movement
        while arduino.in_waiting:
            print("Arduino says:", arduino.readline().decode().strip())
    except serial.SerialException as e:
        print(f"Serial write failed: {e}")
        handle_serial_error()

def handle_serial_error():
    print("Closing serial connection due to error.")
    try:
        arduino.close()
    except serial.SerialException as e:
        print(f"Failed to close serial connection: {e}")

# Initialize serial connection to Arduino
try:
    arduino_port = find_arduino_port()
    arduino = serial.Serial(arduino_port, 9600)
    time.sleep(2)  # Wait for Arduino to initialize
except IOError as e:
    print(f"Error: {e}")
    exit(1)
except serial.SerialException as e:
    print(f"Serial error: {e}")
    exit(1)

# Callback functions for trackbars
def on_servo1_change(val):
    move_servo("SERVO1", val)

def on_servo2_change(val):
    move_servo("SERVO2", val)

# Create a window
cv2.namedWindow('Servo Control')

# Create trackbars for servo control
cv2.createTrackbar('Servo 1', 'Servo Control', 80, 180, on_servo1_change)
cv2.createTrackbar('Servo 2', 'Servo Control', 80, 180, on_servo2_change)


# Capture video from the default camera using V4L2 backend
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce frame width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Reduce frame height

frames = 0

# Start updating the frames
while(True):
    _, frame = cap.read()
    cv2.imshow('myCam', frame)
    cv2.moveWindow('myCam', 100, 100)
    frames += 1
    print(frames)
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

# Close the serial connection
try:
    arduino.close()
except serial.SerialException as e:
    print(f"Failed to close serial connection: {e}")