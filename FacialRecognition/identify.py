import imp

FR = imp.load_source('FaceRecognition', '/Users/lisaxie/Documents/Tech/Hackathon2016/SHIV/RIseFaceDetect/FacialRecognition/FaceRecognition.py')
print FR.identify_face("squadgroup", '/Users/lisaxie/Documents/Tech/Hackathon2016/SHIV/trainingSet/')