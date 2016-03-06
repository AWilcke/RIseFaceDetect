import redis, json

r = redis.StrictRedis()
f = open('../WebcamFaceTrack/dic.txt', 'r')
d = eval(f.read())
f.close()

def init():
    for key in d.keys():
        r.hset('user:'+str(key), 'name', d[key])
        r.hset('user:'+str(key), 'location','unknown')

def getJson(ID):
    name = getName(ID)
    location = getLocation(ID)
    friends = [d[int(friend)] for friend in getFriends(ID)]
    friendsLoc = getFriendLoc(ID)

    output = {'name':name, 'location':location, 'friends':friends, 'friendLocation':friendsLoc}
    return json.dumps(output)

def getName(ID):
    return r.hget('user:'+str(ID),'name')

def setLocation(ID, loc):
    r.hset('user:'+str(ID), 'location',loc)

def getLocation(ID):
    return r.hget('user:'+str(ID),'location')

def addFriend(ID, friendID):
    r.sadd(str(ID)+'friends', friendID)

def getFriends(ID):
    return list(r.smembers(str(ID)+'friends'))

def getFriendLoc(ID):
    friends = getFriends(ID)
    output = {}
    for friend in friends:
        output[d[int(friend)]] = getLocation(friend)
    return output
