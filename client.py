import socket
import numpy as np
import pickle
import frames
import cv2
import win32gui
import os
import io
from time import sleep
from common_header import *
from PIL import ImageGrab, Image

SERVER = "192.168.192.44"
ADDR = (SERVER, PORT)

SCREEN_NAME = "vlc media player"




def send_frame(image):

    # frame = {
    #     'pixels': image.tobytes(),
    #     'size': image.size,
    #     'mode': image.mode
    # }
    
    # dp = pickle.dumps(image)
    # print(f"Sending img of size {image.size} and pickle size is {len(dp)} and len of image to bytes {len(image.tobytes())}")
    # img_byte_arr = io.BytesIO()
    # frame.save(img_byte_arr, 'png')
    # frame_send = img_byte_arr.getvalue()
    
    to_send = bytes(f"{len(image):<{HEADER}}", FORMAT) + bytes(FRAME_MSG, FORMAT) + image
    client.send(to_send)

def send_frame_size(frame):
    fsize = pickle.dumps(frame.size)
    to_send = bytes(f"{len(fsize):<{HEADER}}", FORMAT) + fsize
    client.send(to_send)

def send_dc():
    msg = bytes(f"{len(DISCONNECT_MESSAGE):<{HEADER}}", FORMAT) + bytes(TEXT_MSG, FORMAT) + bytes(DISCONNECT_MESSAGE, FORMAT)
    client.send(msg)
    client.close()


def send_img():
    FILENAME = "img/sao.png"
    # img = cv2.imread(FILENAME)
    # while True:
    #     cv2.imshow("test", img)
    #     cv2.waitKey()
    file_size = os.stat(FILENAME).st_size
    while True:
        with open(FILENAME, "rb")as img:
            bytes_read = img.read(file_size)
            to_send = bytes(f"{file_size:<{HEADER}}", FORMAT) + bytes(IMG_MSG, FORMAT) + bytes_read
            print(f"[SENDING] Msg of size {len(to_send)}, img size: {len(bytes_read)}")
            client.send(to_send)
        print("[IMG SENT]")
        sleep(1)


    # img = Image("img/sao.png")
    # img.show()


def sending_procedure(window_name):

    window = frames.prepare_for_frames(window_name)
    if window is None:
        print(f"[ERROR] Client couldn't send a valide frame")
        return
    for _ in range(100000):
        frame = frames.get_frame(window)
        send_frame(frame)
        # send_frame_size(frame)
        sleep(0.033)
        # cv2.imshow('client',cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     # send_dc()
        #     cv2.destroyAllWindows()
        #     break
        

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

sending_procedure(SCREEN_NAME)
send_dc()