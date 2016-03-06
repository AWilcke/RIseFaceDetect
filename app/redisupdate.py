import redis, json

r = redis.StrictRedis()

def init(dic):
    f = open(dic,'r')
    d = eval(f.read())
    f.close()
    for key in d.keys():
        r.hset('user:'+str(key), 'name', d[key])
        r.hset('user:'+str(key), 'location','unknown')

def getJson(ID):
    name = getName(ID)
    location = getLocation(ID)
    friends = getFriends(ID)

    d = {'name':name, 'location':location, 'friends':friends}
    return json.dumps(d)

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


