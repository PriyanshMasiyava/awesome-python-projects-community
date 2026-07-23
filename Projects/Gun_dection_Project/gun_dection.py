import numpy as np
import cv2
import imutils
import datetime

# Load Haar Cascade
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cascade_path = os.path.join(BASE_DIR, "cascade.xml")

gun_cascade = cv2.CascadeClassifier(cascade_path)

# Open webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

gun_exist = False
firstFrame = None

while True:

    ret, frame = camera.read()

    if not ret:
        print("Failed to capture frame.")
        break

    frame = imutils.resize(frame, width=500)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gun = gun_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)
    )

    if len(gun) > 0:
        gun_exist = True

    for (x, y, w, h) in gun:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )

    if firstFrame is None:
        firstFrame = gray

    current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    cv2.putText(
        frame,
        current_time,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow("Security Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

if gun_exist:
    print("Gun detected.")
else:
    print("No gun detected.")