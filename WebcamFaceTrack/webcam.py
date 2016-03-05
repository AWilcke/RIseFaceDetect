import cv2
import time
from train import *

faceCascade = cv2.CascadeClassifier(cascadePath)
timeAtFound = time.time() - 6 #first time ini of time


video_capture = cv2.VideoCapture(0)
recogniser = trainRecog('images')
dic = {0:'Lisa', 1:'Angus',2:'Serafin',3:'Raz',4:'Ricardo',5:'Andreea',6:'Flaminia',7:'Arthur',8:'Viktorija'}

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    timeSinceFound = time.time() - timeAtFound

    # Draw a rectangle around the faces
    #if len(faces) == 0 or timeSinceFound<5:
    #    pass
    #else:
    #    x, y , w, h = faces[0]
    #    cropimg = frame[y:y+h, x:x+w]
    #    cv2.imshow("face", cropimg)
    #    timeAtFound = time.time();


    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        name = recogniseFace(cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY), recogniser, dic)
        cv2.putText(frame, name, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)
#
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
