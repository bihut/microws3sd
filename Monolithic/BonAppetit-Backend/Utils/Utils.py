import json
import os

'''
def initPath():
    f = open(JSONPATH)
    data = json.load(f)
    os.makedirs(data['rootPath'] +"/"+ data['scenesPath'],exist_ok=True)
'''
class Utils:
    JSONPATH = "/media/bihut/dev/Proyectos/BonAppetit-Backend/structure.json"
    f = open(JSONPATH)

    structure = json.load(f)

    @staticmethod
    def getAllAvatars(ROOT_DIR):

        #abs_path = str(Path(__file__).parent.absolute()) + "/" + Utils.structure['avatars']
        # print(abs_path)
        #print("ROOT DIR:" + str(ROOT_DIR))
        if not os.path.exists(ROOT_DIR + "/" + Utils.structure['avatars']):
            return []
        files = os.listdir(ROOT_DIR + "/" + Utils.structure['avatars'])
        return files

    @staticmethod
    def getAllModels(ROOT_DIR):
        #abs_path = os.path.join(Utils.structure['models'])
        #abs_path = str(Path(__file__).parent.absolute())+"/"+Utils.structure['models']
        #print(abs_path)
        #print("ROOT DIR:"+str(ROOT_DIR))
        if not os.path.exists(ROOT_DIR+"/"+Utils.structure['models']):
            return []
        files = os.listdir(ROOT_DIR+"/"+Utils.structure['models'])
        print(files)
        return files

    @staticmethod
    def getJSONEmptyAvatar():
        jsonObject=None
        with open("utils/collections/avatar/avatar.json") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        return jsonObject

    @staticmethod
    def getJSONEmptyItem():
        jsonObject = None
        with open("utils/collections/avatar/item.json") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        return jsonObject

    @staticmethod
    def getJSONEmptyModel(ROOT_DIR):
        jsonObject = None
        print("PATH0: " + os.getcwd())
        with open(ROOT_DIR+"/"+Utils.structure['collections']+"model.json") as jsonFile:
            #print("PATH: "+os.path.join(jsonFile))
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        return jsonObject

    @staticmethod
    def getPartesModelo(modelid):
        return 1
