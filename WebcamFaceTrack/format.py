import os
from PIL import Image

def getPersonNumber(file, name):
    f = open(file, 'rw+')
    line = f.readlines()[0]
    dic = eval(line)
    keys = dic.keys()
    newnumber = keys[-1] + 1
    dic[newnumber] = name
    f.seek(0)
    f.write(str(dic))
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
