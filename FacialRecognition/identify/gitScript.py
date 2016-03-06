import os, time

directory = os.getcwd()
oldList = os.listdir(directory)
while True:
  time.sleep(5)
  newList = os.listdir(directory)
  for newItem in newList:
    if newItem not in oldList:
      print "should not print"
      os.system("git add --all")
      os.system("git commit -m 'added file " + newItem + "'")
      os.system("git push origin master")
      os.system("python /Users/lisaxie/Documents/Tech/Hackathon2016/SHIV/RIseFaceDetect/FacialRecognition/identification.py")
      oldList = newList