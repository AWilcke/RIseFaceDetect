import cv2, os
import numpy as np
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# gets training data from folder
# files need to be formatted as 01_.*
# where 01 is number in dic
def getImgLbl(path):
    labels = [int(f.split('_')[0]) for f in os.listdir(path)]
    images = [cv2.imread(path+'/'+f) for f in os.listdir(path)]
    endfaces = []
    endlabels = []
    i = 0 #index for getting name
    for image in images:
        try: #convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except: #if fails, was already gray
            gray = image
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(50, 50), flags = cv2.CASCADE_SCALE_IMAGE)
        for (x, y, w, h) in faces:
            endfaces.append(gray[y:y+h, x:x+w])
            endlabels.append(labels[i])
        i+=1
    #test to find optimal detection values
    print "Labels : %d, faces : %d" % (len(labels), len(endfaces))
    return endfaces, endlabels

# returns a trained recogniser
def trainRecog(path):
    recog = cv2.face.createLBPHFaceRecognizer()
    images, labels = getImgLbl(path)
    recog.train(images, np.array(labels))
    return recog

# returns name of recognised face
def recogniseFace(face, recog, dic):
    predicted = recog.predict(face)
    return dic[predicted]

#Testing

#path = 'images'
#dic = {1:'Angus', 2:'Arthur',3:'Lisa'}
#recogniser = trainRecog(path)
#while(True):
#    img = 'Test/' + raw_input("Image?")
#    img = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
#    faces = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
#    for (x, y, w, h) in faces:
#        predicted = recogniser.predict(img[y:y+h, x:x+w])
#        print "%s is predicted" % (dic[predicted])
        

