import httplib, urllib, base64, os, json, urlparse

AuthKey = 'a7f5439ce4fe4f05a1394ece03b03390'
personsIDs = {}
groups = {}

############ FaceDetect Request ######################
def request_faceDetection(imgPath):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': AuthKey,
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
    })

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect?%s" % params, "{ 'url':' "+ imgPath +"'}" , headers)
        response = conn.getresponse()
        data = eval(response.read())
        print(data[0]["faceId"])
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


############### Create a Group ##########################
def create_group(groupID):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': AuthKey,
    }

    params = urllib.urlencode({
        'name' : groupID,
    })




#db425b87-aae7-49c8-bd7f-d62e73160b49



    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("PUT", "/face/v1.0/persongroups/"+groupID+"?", "{ 'name':'TrainingSet'}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

############### Create a Person ##########################
def create_person(name, groupID):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': AuthKey,
    }

    params = urllib.urlencode({
    })
    
    body = json.dumps({
        'name' : name,
        'userData':"None",
    })

    try:
        print (body)
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/persongroups/%s/persons?" % groupID, " %s " % body, headers)
        response = conn.getresponse()
        data = eval(response.read())
        print(data["personId"])
        personsIDs[name] = data["personId"]
        conn.close()
        return data["personId"]
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

############### Add Face to Person #####################
def add_Face_to_Person(groupID, currPersonId, picturePath):
    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': AuthKey,
    }

    params = urllib.urlencode({
        # Request parameters
        'userData': 'Picturename %s' % picturePath,
    })
    
    body = json.dumps({
        'url' : picturePath,
    })
    print body

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/persongroups/%s/persons/%s/persistedFaces?%s" % (groupID, currPersonId, params), " %s " % body, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


############### Change Dir & get List ##################
def change_dir_get_file_list(dirPath):
    os.chdir(dirPath)
    pwd = os.getcwd()
    return os.listdir(pwd)

############### Face Grouping ##########################
def do_TrainingSet(FolderFilePath):
    oldPath = os.getcwd()+"/"+FolderFilePath
    folders = change_dir_get_file_list(FolderFilePath)
    create_group(FolderFilePath)
    for name in folders:
         currPersonId = create_person(name, FolderFilePath)
         os.chdir(oldPath)
         pictureNames = change_dir_get_file_list(name)
         for pictureName in pictureNames:
            picturePath = "http://azurehellocloud2016one.azurewebsites.net/"+name+"/"+pictureName
            print picturePath
            add_Face_to_Person(FolderFilePath, currPersonId, picturePath)
            break
     


do_TrainingSet("squadgroup")
print (personsIDs)
