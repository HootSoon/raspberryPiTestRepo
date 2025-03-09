import tkinter as tk
from tkinter import Label
import cv2
from PIL import Image, ImageTk
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

# Initialize serial connection to Arduino
try:
    arduino_port = find_arduino_port()
    arduino = serial.Serial(arduino_port, 9600)
    time.sleep(2)  # Wait for Arduino to initialize
except IOError as e:
    print(f"Error: {e}")
    exit(1)

# Initialize Tkinter window
menu = tk.Tk()
menu.title("OpenCV and Tkinter Integration")
menu.geometry("640x480")

# Create a label to display the video frames
video_label = Label(menu)
video_label.grid(row=1, column=0, columnspan=2)

# Create Scale widgets to control the servos
servoScale = tk.Scale(menu, from_=0, to=180, orient='horizontal', label='Servo 1', length=200, command=lambda x: move_servo("SERVO1", x))
servoScale.grid(row=3, column=0)

servoScale1 = tk.Scale(menu, from_=0, to=180, orient='horizontal', label='Servo 2', length=200, command=lambda y: move_servo("SERVO2", y))
servoScale1.grid(row=3, column=1)

# Create a label to display the frame number
frame_number_label = Label(menu, text="Frame: 0")
frame_number_label.grid(row=0, column=0)

# Create a flag to control the video capture
capture_video = True

# Function to handle key presses
def key_handler(event):
    if event.char in ['w', 'a', 's', 'd']:
        print(f"Key Pressed: {event.char}")
        send_to_arduino(event.char)

# Bind key events
menu.bind('<KeyPress>', key_handler)

# SERIAL CODE
def send_to_arduino(command):
    try:
        arduino.write(command.encode())
    except serial.SerialException as e:
        print(f"Serial write failed: {e}")

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

# Capture video from the default camera using V4L2 backend
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce frame width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Reduce frame height

frame_number = 0

def update_frame():
    global frame_number
    if capture_video:
        ret, frame = cap.read()
        if ret:
            frame_number += 1
            # Convert the frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to a PIL image
            img = Image.fromarray(frame)
            # Convert the PIL image to an ImageTk image
            imgtk = ImageTk.PhotoImage(image=img)
            # Update the video label with the new image
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
            # Update the frame number label
            frame_number_label.config(text=f"Frame: {frame_number}")

        # Increase the update interval to reduce CPU load
        video_label.after(10, update_frame)




# Start updating the frames
update_frame()

# Start the Tkinter main loop
menu.mainloop()

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

# Close the serial connection
arduino.close()