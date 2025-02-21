import socket

UDP_IP = "0.0.0.0"  # IP address in serial monitor
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    command = input("Enter command (F/B/L/R/S): ").strip().upper()
    if command in ['F', 'B', 'L', 'R', 'S']:
        sock.sendto(command.encode(), (UDP_IP, UDP_PORT))
    else:
        print("Invalid command.")