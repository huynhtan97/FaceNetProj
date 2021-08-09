import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")

img = cv2.imread('cat.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.05, 5)

print(len(faces))

if len(faces) == 1:
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imshow('Detected Face', img)
print("Success!")

keypress = cv2.waitKey(1) % 256
if keypress == ord('q'):
    cap.release()
    cv2.destroyAllWindows()
    print("Exit")

