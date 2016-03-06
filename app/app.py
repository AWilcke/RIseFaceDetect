from flask import Flask
from flask import render_template
from flask import request
from redisupdate import *
from webapp import *
import numpy as np

app = Flask(__name__)
init()
face = []
faces = [] #needs to be initialised and empty on first run

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
    image = request.data.decode('base64')
    face, (x,y,w,h) = getFace(np.array(image))
    return

# Return JSON object with data about the person, or a None
@app.route('/get_face', methods=['GET'])
def get_face():
    global faces
    if len(face)!=0:
        seen = time.time()
        faces.append(face)
    
    ID = getName(faces)
    data = getJson(int(ID))
    if time.time() - seen >3: #no face seen in 3s
        faces = []
        return "Not yet", 204
    else:
        return data

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, processes=30, debug=True, ssl_context='adhoc')
    #app.run()
