import socket 
import threading
import numpy as np
import pickle
import cv2
from PIL import Image
from common_header import *

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def receive_msg(msg_len, conn, buffer):
    msg = b''
    while(len(msg) < msg_len):
        msg += conn.recv(buffer)
        # msg.append(conn.recv(buffer))
    return msg

def receive_frame_size(conn):
    leng = conn.recv(HEADER).decode(FORMAT)
    m = receive_msg(leng, conn, BUFFER_SIZE)
    m = pickle.loads(m)
    print(m)
    return m

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        msg_len = None
        try:
            msg_len = int(msg)
            print(f"[MESSAGE PROPERTY] Server is going to receive msg of a length {msg_len}")
        except ValueError:
            print("[CLOSING CONNECTION: ERROR] Value in header was wrong, DISCONNECTING")
            connected = False
            continue

        msg_type = conn.recv(1).decode(FORMAT)

        


        if msg_type == FRAME_MSG:
            msg = receive_msg(msg_len, conn, BUFFER_SIZE)
            # frame_bytes = pickle.loads(msg)
            FRAME_SAVE = 'server/framesaved.jpg'
            with open(FRAME_SAVE, "wb") as f:
                f.write(msg)
            frame = cv2.imread(FRAME_SAVE)
            # frame = Image.frombytes(img['mode'], img['size'], img['pixels'])
            # cv2.imshow('server',cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            WINDOWNAME = 'server'
            cv2.namedWindow(WINDOWNAME, cv2.WND_PROP_FULLSCREEN)          
            cv2.setWindowProperty(WINDOWNAME, cv2.WND_PROP_FULLSCREEN, 1)
            cv2.imshow(WINDOWNAME,frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


        if msg_type == TEXT_MSG:
            msg = conn.recv(msg_len).decode(FORMAT)
            print(f"Server received text msg: {msg}, from addr({addr})")
            if msg == DISCONNECT_MESSAGE:
                connected = False
                continue
        
        if msg_type == IMG_MSG:
            img = receive_msg(msg_len, conn, 1024)
            print(f"[SERVER HAS RECEIVED IMG] Size of img = {len(img)}")
            SAVEPATH = "server/frame.png" 
            with open(SAVEPATH, "wb+") as to_save:
                to_save.write(img)

            i = cv2.imread(SAVEPATH)
            cv2.imshow('img', i)
            cv2.waitKey(27)
            # connected = False
            # continue
    print(f"[CLOSING CONNECTION] Server is closing connection with {addr}.")
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()