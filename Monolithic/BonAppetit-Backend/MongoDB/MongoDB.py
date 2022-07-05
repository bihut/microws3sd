from pymongo import MongoClient
import hashlib
import json

class MongoDB:
    client=None
    db = None
    def __init__(self, connection_string):
        #self.connectMongo(connection_string)
        #self.testing()
        pass

    def checkIfAvatarExist(self,datajson):
        avatars = self.db.avatar.find({})
        hash1 = hashlib.md5(json.dumps(datajson).encode()).hexdigest()
        for document in avatars:
            idaux = str(document['_id'])
            del document['_id']
            hash_object = hashlib.md5(json.dumps(document).encode())
            if(hash_object.hexdigest()==hash1):
                return idaux
        return None

    def connectMongo(self,url):
        #print("URL "+url)
        client = MongoClient(url)
        self.db=client.bonappetit
        serverStatusResult = self.db.command("serverStatus")
        #print(serverStatusResult)

    def insertAvatar(self,data):
        if(self.checkIfAvatarExist(data) == False):
            return 0
    '''
    def initDB(self):
        #try:
        #    self.db.validate_collection("avatar")  # Try to validate a collection
        #except pymongo.errors.OperationFailure:  # If the collection doesn't exist
        #    self.db.createCollection("avatar")
        collection = self.db["avatar"]
        avatar = Utils.getJSONEmptyAvatar()

        avatar["modelid"] = 1
        item = Utils.getJSONEmptyItem()
        item["name"] = "cape"

        avatar['items'].append(item)
        item = Utils.getJSONEmptyItem()
        item["name"] = "cape1"
        avatar['items'].append(item)
        collection.insert_one(avatar)

        avatar = Utils.getJSONEmptyAvatar()
        avatar["modelid"]=2
        item = Utils.getJSONEmptyItem()
        item["name"]="aaa1"

        avatar['items'].append(item)
        item = Utils.getJSONEmptyItem()
        item["name"] = "aa2"
        avatar['items'].append(item)
        print(json.dumps(avatar))
        collection.insert_one(avatar)
    '''
#mongo = MongoDB(CONST_USERNAME,CONST_PASSWORD,CONST_CONNECTION_STRING)
# Issue the serverStatus command and print the results
