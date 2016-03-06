from flask import Flask
from flask import render_template
from flask import request
import redis
import json

app = Flask(__name__)
r = redis.StrictRedis()

@app.route('/')
def main():
    r.hset('user:7','location','Room 1')
    r.hset('user:7','name','Arthur Wilcke')
    r.rpush('user7friends','0')
    r.rpush('user7friends','1')
    return render_template("index.html")

@app.route('/<usernum>/location')
def location(usernum):
    return r.hget('user:'+usernum,'location')

@app.route('/<usernum>/name')
def name(usernum):
    return r.hget('user:'+usernum,'name')

@app.route('/<usernum>/friends')
def friends(usernum):
    return r.lrange('user'+ usernum + 'friends', 0, -1)

# Receive image as POST data from the UI
@app.route('/push_face', methods=['POST'])
def push_face():
    # do something with request.form['file']
    return "TODO"

# Return JSON object with data about the person, or a None
@app.route('/get_face', methods=['GET'])
def get_face():
    return "TODO"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, processes=30, debug=True, ssl_context='adhoc')
