import os
import cv2
import shutil
import sys
from matplotlib import pyplot as plt
from io import StringIO
import numpy as np
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

class ListStream:
    def __init__(self):
        self.data = []

    def write(self, s):
        self.data.append(s)

# Image processing method - Brighten image
def increase_brightness(img, value = 30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

# turn off stdout
old_stdout = sys.stdout

sys.stdout = mystdout = StringIO()

# declare threshold for accuracy
threshold = 0.4

# Check system to load directory
if os.name == "nt":
    slash = "\\"  # windows
else:
    slash = "/"  # unix


# CAT DETECTION WITH HAAR CASCADE
cat_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface_extended.xml')

# load webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

while (cap.isOpened()):

    # Display stream - capture frame by frame
    ret, frame = cap.read()
    # Brighten input so facenet can detect animal better
    bframe = increase_brightness(frame)

    gray = cv2.cvtColor(bframe, cv2.COLOR_BGR2GRAY)
    # detectMultiScale() returns rectangles with coordinates (x,y,w,h) around detected cat face
    cats = cat_cascade.detectMultiScale(gray, 1.3, 5)

    # Display text to bframe in opencv if no animal detected
    if (len(cats) != 1):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(bframe, 'ADJUST PLEASE', (20, 250), font, 1, (0, 0, 255), 3, cv2.LINE_AA)
        # publish.single(topic='ledStatus', payload='Off', hostname='broker.hivemq.com', protocol=mqtt.MQTTv31)

    # Draw bounding box in live webcam feed
    for (x, y, w, h) in cats:
        cv2.rectangle(bframe, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display results
    cv2.imshow('Bounding Box', bframe)

    # listen for keypress
    c = cv2.waitKey(1) % 256

    # if 'c' is pressed - ord(): returns integer representation of character
    # MAKE SURE USER CAN'T TAKE SCREEN SHOT IF NO BOUNDING BOX
    # if (c == ord('c') and len(cats) == 1):
    #     # delete if pic is already present
    #     capPic = '..' + slash + 'datasets' + slash + 'animal_cap' + slash + 'capture.jpg'
    #     if os.path.isfile(capPic):
    #         os.remove(capPic)
    #
    #     # save input into capPic directory
    #     cv2.imwrite(capPic, bframe)
    #
    #     # redirect output from testing classifier to a variable
    #     sys.stdout = output = ListStream()
    #
    #     # check if a snapshot was generated
    #     if os.path.isfile(capPic):
    #         # AN- original Image captured from webcam
    #         capturedFrame = cv2.imread(capPic, cv2.IMREAD_COLOR)
    #         cv2.imshow("Original Picture", capturedFrame)
    #
    #         # AN- Convert above image to gray just for processing
    #         capturedFrame_Gray = cv2.cvtColor(capturedFrame, cv2.COLOR_BGR2GRAY)
    #
    #         # Display and show bounding box around detected cats - resulting image
    #
    #
    #     else:
    #         print("Unknown")

    # 'q' = exit
    # elif c == ord('q'):
    #     break

    if c == ord('q'):
        break

    sys.stdout = mystdout = StringIO()

# release resources
cap.release()
cv2.destroyAllWindows()

print("Exit")