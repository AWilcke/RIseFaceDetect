from flask import Flask
from flask import render_template
from flask import request
from redisupdate import *
from webapp import *
import numpy as np
from PIL import Image
import base64

app = Flask(__name__)
init()

#global variables
face = []   #store the face of current frame
name = ''   #store name predicted
names = [] #store list of all predicted names
seen = time.time() # store last time a face was seen

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/<usernum>/location')
def location(usernum):
    return r.hget('user:'+usernum,'location')

@app.route('/<usernum>/name')
def name(usernum):
    return r.hget('user:'+usernum,'name')

@app.route('/<usernum>/friends')
def friends(usernum):
    return json.dump(r.lrange('user'+ usernum + 'friends', 0, -1))

# Receive image as POST data from the UI
@app.route('/push_face', methods=['POST'])
def push_face():
    
    # do something with request.form['image']
    global face
    image = request.data.split(',')[1]
    img = image.decode('base64')
    im = cv2.imdecode(np.frombuffer(img, dtype='uint8'), 1)
    face, (x,y,w,h) = getFace(im)
    return 'OK'

# Return JSON object with data about the person, or a None
@app.route('/get_face', methods=['GET'])
def get_face():
    global names, name, seen, face

    #if a face is seen, predict most likely name
    if len(face)!=0:
        seen = time.time()
        names.append(recogniseID(face, recogniser))
        name = max(set(names), key=names.count)
    #JSON data for name
    data = getJson(name)
    
    if time.time() - seen >1: #no face seen in 1s
        names = []
        name = ''
        return "Not yet", 204
    
    else:
        return data

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5010, processes=30, debug=True, ssl_context='adhoc')
    #app.run()
