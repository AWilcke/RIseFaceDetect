import os
from PIL import Image
import time
import cv2

cascadePath = "haarcascade_frontalface_default.xml"

def getPersonNumber(file, name):
    f = open(file, 'rw+')
    line = f.readlines()[0]
    dic = eval(line)
    if name not in dic.values():
        keys = dic.keys()
        newnumber = keys[-1] + 1
        dic[newnumber] = name
        f.seek(0)
        f.write(str(dic))
    else:
        for i in range(0,len(dic)):
            if dic[i] == name:
                newnumber = i
                break
    f.truncate()
    f.close()
    return newnumber
    
def createPerson(name):
    i = 0
    number = getPersonNumber('dic.txt', name)
    path = '../FacialRecognition/squadgroup/' + name 
    for file in os.listdir(path):
        current = Image.open(path + '/' + file)
        current.save('images/' + str(number) + '_' + str(i), "JPEG")
        i+=1

def videoDic(name):
    #initialise stuff
    video_capture = cv2.VideoCapture(0)
    cv2.startWindowThread()
    cv2.namedWindow("Recording...")
    faceCascade = cv2.CascadeClassifier(cascadePath)
    i = 0
    number = getPersonNumber('dic.txt', name)
    os.chdir('TrainingData')
    start = time.time()
    lastRecord = start
    #capture for 10s
    while(time.time() - start<10):
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(50,50),
                flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        #get the pics
        if time.time() - lastRecord>0.25:
            cv2.imwrite(str(number) + '_' + str(i) + '.jpg', frame)
            lastRecord = time.time()
            i+=1

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)
          
        cv2.imshow('Recording...',frame)
    os.chdir('..')
    cv2.destroyAllWindows()
