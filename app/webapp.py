from train import *
import time

faceCascade = cv2.CascadeClassifier(cascadePath)
dic = eval(open('dic.txt','r').read())
video_capture = cv2.VideoCapture(0)
recogniser = trainRecog('TrainingData')

#returns face as grayscale
def getFace(pic):

    try:
        gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    except:
        gray = pic

    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=10,
            minSize=(50,50),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
    
    if len(faces) == 1:
        (x, y, w, h) = faces[0]
        output = gray[y:y+h, x:x+w]
        return output, faces[0]
    else:
        return [] , (0,0,0,0)

#returns most common answer for a list of faces
def getName(facePics):
    names = [recogniseID(face, recogniser) for face in facePics]
    best = max(set(names), key=names.count)
    return best

#testing how it works in local
def testLocal(runtime):
    start = time.time()
    faces = []
    cv2.startWindowThread()
    cv2.namedWindow('Recognising')

    while(time.time() - start<runtime):
        ret, frame = video_capture.read()
        face, (x,y,w,h) = getFace(frame)
        if len(face) != 0:
            faces.append(face)
        cv2.rectangle(frame, (x, y), (x+w, y+h) ,(0,0,255),2)
        cv2.imshow('Recognising', frame)
    
    name = getName(faces)
    cv2.destroyAllWindows()
    return name, len(faces)
