import socket 
import threading
import numpy as np
import pickle
import cv2
import os
from PIL import Image
from common_header import *

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
WINDOWNAME_DISPLAY = 'server'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def receive_msg(msg_len, conn, buffer):
    msg = b''
    while(len(msg) < msg_len):
        msg += conn.recv(buffer)
        # msg.append(conn.recv(buffer))
    return msg

def cleanup():
    os.remove(SERVER_FRAMESAVE)
    cv2.destroyAllWindows()


def handle_frame_msg(conn, msg_len):
    msg = receive_msg(msg_len, conn, BUFFER_SIZE)
    # frame_bytes = pickle.loads(msg)
    
    with open(SERVER_FRAMESAVE, "wb") as f:
        f.write(msg)
    frame = cv2.imread(SERVER_FRAMESAVE)
    # frame = Image.frombytes(img['mode'], img['size'], img['pixels'])
    # cv2.imshow('server',cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    cv2.namedWindow(WINDOWNAME_DISPLAY, cv2.WND_PROP_FULLSCREEN)          
    cv2.setWindowProperty(WINDOWNAME_DISPLAY, cv2.WND_PROP_FULLSCREEN, 1)
    cv2.imshow(WINDOWNAME_DISPLAY,frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

def handle_text_msg(conn, msg_len, connected, addr):
    msg = conn.recv(msg_len).decode(FORMAT)
    print(f"Server received text msg: {msg}, from addr({addr})")
    if msg == DISCONNECT_MESSAGE:
        connected = False

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        msg_len = None
        try:
            msg_len = int(msg)
            print(f"[STATISTICS] Server is going to receive msg of a length {msg_len}")
        except ValueError:
            print("[CLOSING CONNECTION: ERROR] Value in header was wrong, DISCONNECTING")
            connected = False
            continue

        msg_type = conn.recv(1).decode(FORMAT)

        if msg_type == FRAME_MSG: handle_frame_msg(conn, msg_len)

        if msg_type == TEXT_MSG: handle_text_msg(conn, msg_len, connected, addr)
            

        
    print(f"[CLOSING CONNECTION] Server is closing connection with {addr}.")
    cleanup()
    conn.close()
    print(f"[CLOSING CONNECTION] Connection closed.")
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] Server has accepted new connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[STATISTICS] Active connections: {threading.activeCount() - 1}")


print("[STARTING] Server is starting...")
start()