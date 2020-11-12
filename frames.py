import time
import numpy as np
import win32gui
from PIL import ImageGrab, Image
import cv2
import io
import os
from copy import copy
from common_header import *


QUALITY = 90


winlist = []

def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
 
def get_screens(screen_name):
    # wait for the program to start initially.
    win32gui.EnumWindows(enum_cb, winlist)
    screens = [(hwnd, title) for hwnd, title in winlist if screen_name in title.lower()]
    while len(screens) == 0:
        screens = [(hwnd, title) for hwnd, title in winlist if screen_name in title.lower()]
        win32gui.EnumWindows(enum_cb, winlist)

    return screens


def prepare_for_frames(screen_name):
    screen = copy(screen_name)
    screens = get_screens(screen)

    if len(get_screens(screen)) <= 0:   # check if closed
        return None

    window = screens[0][0]

    return window

def get_frame(window):
    # screen = 'vlc media player'
    try:
        frame = ImageGrab.grab(bbox=win32gui.GetWindowRect(window))
        frame.save(CLIENT_FRAMESAVE, optimize = True, quality = QUALITY)
        with open(CLIENT_FRAMESAVE, "rb") as f:
            frame = f.read()
        return frame
        # # print("loop took {} seconds".format(time.time() - last_time))
        # # last_time = time.time()
        # cv2.imshow('window',cv2.cvtColor(print_screen, cv2.COLOR_BGR2RGB))
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break
    except Exception as e:
        print("Error during creating frame", e)


# last_time = time.time()



# winlist = []
# screen = 'vlc media player'
# # screen = copy(screen_name)
# screens = get_screens(screen)

# cont = True
# while cont:
#     if len(get_screens(screen)) <= 0:   # check if closed
#         cont = False
#         continue

#     window = screens[0][0]

#     try:
#         print_screen = np.array(ImageGrab.grab(bbox=win32gui.GetWindowRect(window)))
#         # print("loop took {} seconds".format(time.time() - last_time))
#         # last_time = time.time()
#         cv2.imshow('window',cv2.cvtColor(print_screen, cv2.COLOR_BGR2RGB))
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()
#             break
#     except Exception as e:
#         print("error", e)