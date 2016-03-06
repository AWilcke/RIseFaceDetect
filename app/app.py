from flask import Flask
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
    return "Set data for user 7"

@app.route('/<usernum>/location')
def location(usernum):
    return r.hget('user:'+usernum,'location')

@app.route('/<usernum>/name')
def name(usernum):
    return r.hget('user:'+usernum,'name')

@app.route('/<usernum>/friends')
def friends(usernum):
    return r.lrange('user'+ usernum + 'friends', 0, -1)

if __name__ == '__main__':
    app.run()
