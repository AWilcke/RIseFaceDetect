import httplib, urllib, base64, os, json, urlparse, time

AuthKey = 'a7f5439ce4fe4f05a1394ece03b03390'
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': AuthKey,
}

header = {
    # Request headers
    'Ocp-Apim-Subscription-Key': AuthKey,
}

############### Send request to server #################
def send_request(requestType, URL, body, header):

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request(requestType, URL, body, header)
        print URL
        response = conn.getresponse()
        data = eval(response.read())
        conn.close()
        return data
    except Exception as e:
        print(e)
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

############### Create a Group ##########################
def create_group(groupID):

    body = json.dumps({
            'name' : 'TrainingSet'
        })

    data = send_request("PUT", "/face/v1.0/persongroups/"+groupID+"?", body, headers)
    print data


############# List Persons in Group ###############

def populate_personIDs(groupID):
    personIDs = {}
    data = send_request("GET", "/face/v1.0/persongroups/"+ groupID+"/persons", "", header)
    for person in data:
        personIDs[person["personId"]] = person["name"]
    return personIDs


############### Detect a Face #####################

def detect_face(filePath):

    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false'
    })

    body = json.dumps({
            'url' : "http://facehosting.azurewebsites.net/"+filePath,
        })

    data = send_request("POST", "/face/v1.0/detect?%s" % params, body , headers)
    return data[0]["faceId"]



############### Create a Person ##########################
def create_person(name, groupID):

    body = json.dumps({
        'name' : name,
        'userData':"None",
    })

    data = send_request("POST", "/face/v1.0/persongroups/%s/persons?" % groupID, body, headers)
    return data["personId"]

############### Add Face to Person #####################
def add_Face_to_Person(groupID, currPersonId, picturePath):

    params = urllib.urlencode({
        'userData': 'Picturename %s' % picturePath,
    })
    
    body = json.dumps({
        'url' : picturePath,
    })
    data = send_request("POST", "/face/v1.0/persongroups/%s/persons/%s/persistedFaces?%s" % (groupID, currPersonId, params), body, headers)
    print data

############### Change Dir & get List ##################
def change_dir_get_file_list(dirPath):
    os.chdir(dirPath)
    pwd = os.getcwd()
    return os.listdir(pwd)


############### Change Dir & get List ##################
def train_group_request(groupID):

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        print "sending post requests"
        conn.request("POST", "/face/v1.0/persongroups/%s/train?" % groupID, "", header)
        response = conn.getresponse()
        conn.close()
        print "post request done"
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

############### Get Person Info ##################
def get_person(personId, groupID):

    data = send_request("GET", "/face/v1.0/persongroups/%s/persons/%s?" % (groupID, personId), "", header)
    return data["name"]


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
            picturePath = "http://facehosting.azurewebsites.net/"+FolderFilePath+"/"+name+"/"+pictureName
            add_Face_to_Person(FolderFilePath, currPersonId, picturePath)
         time.sleep(20)

    train_group_request(FolderFilePath)
    os.chdir(originalPath)

############### Identify Face ##########################
def identify_face_from_Group(faceId, groupID):

    body = json.dumps({
        "faceIds": [faceId],
        "maxNumOfCandidatesReturned": 2,
        "personGroupId": groupID,
        })
    data = send_request("POST", "/face/v1.0/identify?", body, headers)
    mostLikelyCandidate = data[0]["candidates"]
    if not mostLikelyCandidate:
        return "Unknown"
    else:
        print "Sure with confidence of %f" % data[0]["candidates"][0]["confidence"]
        return data[0]["candidates"][0]["personId"]


################## Match face to Group #######################
def identify_face(groupID):
    names_of_identifies = []
    originalPath = os.getcwd()
    identify_pictures = change_dir_get_file_list("identify")
    personIDs = populate_personIDs(groupID)

    for filename in identify_pictures:
        faceId = detect_face("identify/"+filename)

        if faceId is not None:
            time.sleep(7)
            candidateID = identify_face_from_Group(faceId, groupID)

            if candidateID == "Unknown":
                names_of_identifies.append("Unknown")
            else: 
                names_of_identifies.append(personIDs[candidateID])
    return names_of_identifies


#do_TrainingSet("squadgroup")
print identify_face("squadgroup")
