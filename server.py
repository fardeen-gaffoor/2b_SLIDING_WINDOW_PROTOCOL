import socket
import time

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 8001))
s.listen(5)
print("Server is listening for Sliding Window requests...")

c, addr = s.accept()
print(f"Connection established with {addr}")

try:
    # Receive total frames
    total_frames = int(c.recv(1024).decode())
    print(f"Total frames to receive: {total_frames}")
    
    # Receive window size
    window_size = int(c.recv(1024).decode())
    print(f"Window size: {window_size}")
    
    # Calculate number of transmissions
    num_windows = (total_frames + window_size - 1) // window_size
    print(f"Expected {num_windows} window(s)")
    
    for i in range(num_windows):
        # Receive frame data
        frame_data = c.recv(1024).decode()
        if frame_data:
            print(f"Received frames: {frame_data}")
            
            # Send acknowledgment
            ack = f"ACK {frame_data}"
            c.send(ack.encode())
            print(f"Sent: {ack}")
            time.sleep(0.1)
        else:
            break
    
    print("All frames received successfully!")

except Exception as e:
    print(f"Server error: {e}")

finally:
    c.close()
    s.close()
    print("Server closed")