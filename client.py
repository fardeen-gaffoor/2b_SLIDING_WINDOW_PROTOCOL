import socket

c = socket.socket()
c.connect(('localhost', 8001))

size = int(input("Enter number of frames to send: "))
l = list(range(size))
print("Total frames to send:", len(l))
s = int(input("Enter Window Size: "))

# Send metadata to server
c.send(str(size).encode())
import time
time.sleep(0.1)  # Small delay between sends
c.send(str(s).encode())
time.sleep(0.1)

i = 0
while i < len(l):
    st = i + s
    frames_to_send = l[i:st]
    print(f"Sending frames: {frames_to_send}")
    c.send(str(frames_to_send).encode())
    
    # Receive acknowledgment
    try:
        ack = c.recv(1024).decode()
        if ack:
            print(f"Acknowledgment received: {ack}")
            i += s
        else:
            print("No acknowledgment received")
            break
    except Exception as e:
        print(f"Error receiving ACK: {e}")
        break

c.close()
print("Client closed")