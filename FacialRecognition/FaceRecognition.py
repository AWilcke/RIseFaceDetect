import httplib, urllib, base64, os, json, urlparse, time

AuthKey = 'a7f5439ce4fe4f05a1394ece03b03390'
personsIDs = {}
groups = {}

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

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("PUT", "/face/v1.0/persongroups/"+groupID+"?", "{ 'name':'TrainingSet'}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


############### Detect a Face #####################

def detect_face(filePath):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': AuthKey,
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false'
    })

    body = json.dumps({
            'url' : "http://azurehellocloud2016one.azurewebsites.net/"+filePath,
        })

    try:
        print body;
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect?%s" % params, " %s " % body , headers)
        response = conn.getresponse()
        data = eval(response.read())
        conn.close()
        return data[0]["faceId"]
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



############### Create a Person ##########################
def create_person(name, groupID):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': AuthKey,
    }
    
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
        print(data)
        print(data["personId"])
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

############### Change Dir & get List ##################
def train_group_request(groupID):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': AuthKey,
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/persongroups/%s/train?" % groupID, "", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

############### Get Person Info ##################
def get_person(personId, groupID):

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': AuthKey,
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/face/v1.0/persongroups/%s/persons/%s?" % (groupID, personId), "", headers)
        response = conn.getresponse()
        data = eval(response.read())
        conn.close()
        return data["name"]
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



############### Face Grouping ##########################
def do_TrainingSet(FolderFilePath):
    originalPath = os.getcwd()
    oldPath = originalPath+"/"+FolderFilePath
    folders = change_dir_get_file_list(FolderFilePath)
    create_group(FolderFilePath)
    for name in folders:
         currPersonId = create_person(name, FolderFilePath)
         os.chdir(oldPath)
         pictureNames = change_dir_get_file_list(name)
         for pictureName in pictureNames:
            picturePath = "http://azurehellocloud2016one.azurewebsites.net/"+name+"/"+pictureName
            add_Face_to_Person(FolderFilePath, currPersonId, picturePath)
         time.sleep(20)
    train_group_request(FolderFilePath)
    os.chdir(originalPath)
    time.sleep(40)

############### Identify Face ##########################

def identify_face_from_Group(faceId, groupID):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': AuthKey,
    }

    params = urllib.urlencode({
    })

 
    body = json.dumps({
        "faceIds": [faceId],
        "maxNumOfCandidatesReturned": 2,
        "personGroupId": groupID,
        })

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/identify?%s" % params, " %s" % body, headers)
        response = conn.getresponse()
        data = eval(response.read())
        conn.close()
        print data
        mostLikelyCandidate = data[0]["candidates"]
        if not mostLikelyCandidate:
            return "Unknown"
        else:
            print "Sure with confidence of %f" % data[0]["candidates"][0]["confidence"]
            return data[0]["candidates"][0]["personId"]
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))




################## Match face to Group #######################
def identify_face(groupID):
    names_of_identifies = []
    originalPath = os.getcwd()
    identify_pictures = change_dir_get_file_list("identify")
    for filename in identify_pictures:
        faceId = detect_face("identify/"+filename)
        if faceId is not None:
            candidateID = identify_face_from_Group(faceId, groupID)
            time.sleep(5)
            if candidateID == "Unknown":
                names_of_identifies.append("Unknown")
            else: 
                names_of_identifies.append(get_person(candidateID, groupID))
    return names_of_identifies


#do_TrainingSet("squadgroup")
print identify_face("squadgroup")
