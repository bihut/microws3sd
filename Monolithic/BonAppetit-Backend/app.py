import base64
import json
import os
import subprocess
import time
import re
import shutil

#ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
from flask import flash, redirect, request, Flask, session
from werkzeug.utils import secure_filename
import importlib
import sys


def importModules():
    path = r'/media/bihut/dev/Proyectos/BonAppetit-Backend/Utils/__init__.py'
    #pathUtils = path+"/Utils/__init__py"
    name = r'Utils'
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    path = r'/media/bihut/dev/Proyectos/BonAppetit-Backend/MongoDB/__init__.py'
    name = 'MongoDB'

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)





importModules()
from MongoDB.MongoDB import MongoDB
from Utils.Utils import Utils


#JSONPATH = "/Users/bihut/GoogleDrive/UGR/Proyectos/BonAppetit/BonAppetit-Backend/structure.json"
f = open(Utils.JSONPATH)
structure = json.load(f)
app = Flask(__name__)
app.config['structure'] = structure
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'supersecretkey'
connection_string = structure['mongodbprotocol']+structure['mongodbusername']+":"+structure['mongodbpassword']+"@"+structure['mongodbserver']+"/"+structure['mongodbdb']
mongo = MongoDB(connection_string)
app.config['mongo'] = mongo
app.config['ROOT_DIR'] = os.path.dirname(os.path.abspath(__file__))
#app.config['UPLOAD_FOLDER_IMAGES'] = structure['images']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CONST_REGEX="%@%"
CONST_LIST_MODELS=0
CONST_LOAD_MODEL=1
CONST_GENERATE_AVATAR=2


@app.route('/')
def hello_world():
    url = request.url_root + "static/tempavatars/prueba.fbx"
    return url

@app.route("/api/model",methods = ['GET'])
def getAllModels():
    models=Utils.getAllModels(app.config['ROOT_DIR'])
    avatars = Utils.getAllAvatars(app.config['ROOT_DIR'])
    json_out = {"result": "ok","models":models,"avatars":avatars}
    return json_out

BLENDER_PATH="/home/bihut/dev/blender/blender"
BLENDER_SCRIPT_PATH="/home/bihut/dev/Proyectos/BonAppetit-Backend/BlenderServices/BlenderServices.py"
@app.route("/api/model/<name>/items")
def getModel(name):
    #path = app.config['ROOT_DIR'] + "/static/models/" + name
    command = BLENDER_PATH+' --background --python '+BLENDER_SCRIPT_PATH+' \'{"option":'+str(CONST_LOAD_MODEL)+',"rootdir":"'+app.config['ROOT_DIR']+'","name":"'+name+'"}\' '
    print("COMMAND:",command)
    output=os.popen(command).read()
    outputbueno = re.search(r'%@%(.*?)%@%', output).group(1)
    jsn = json.loads(outputbueno)
    jsn['path'] =request.url_root+"static/tempavatars/"+jsn['path']
    return jsn
    #process = subprocess.run(finalparam, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    #output = process.stdout
    #output=os.popen(finalparam).read()
    #print("OUTPUT",output)
    '''
    #bl = BlenderServices(1,path,app)
    #bl.cleanAll()
    #bl.loadModel()
    split = name.split(".")
    filenametemp ="temp_"+split[0]+"_"+str(int(time.time()))+"."+split[1]
    pathGLTF = app.config['ROOT_DIR']+"/static/tempavatars/"+filenametemp
    print("ANTES DE ENTRAR AL IF")
    if(split[1]=="gltf" or split[1]=="glb"):
        src = path
        dest = pathGLTF
        shutil.copyfile(src,dest)
        json_Data = bl.getListaPartesModeloJSON()
        json_Anims = bl.getAnimations()
        json_out = {"result": "ok", "items": json_Data,"animations":json_Anims, "path": dest}
        return json_out
    else:
        print("PATH:"+pathGLTF)
        res=bl.exportAsGLTF(pathGLTF)
        print("RES:"+str(res))
        json_Data = bl.getListaPartesModeloJSON()
        url = request.url_root+"static/tempavatars/"+filenametemp+".glb"
        json_out = {"result": "ok","items":json_Data,"path":url}
        #del bl
        return json_out
'''
@app.route("/api/model/<name>/animations")
def getModelAnimation(name):
    '''
    path = app.config['ROOT_DIR']+"/static/models/"+name
    bl = BlenderServices(1,path)
    bl.cleanAll()
    bl.loadModel()
    split = name.split(".")
    filenametemp ="temp_"+split[0]+"_"+str(int(time.time()))+"."+split[1]

    pathGLTF = app.config['ROOT_DIR']+"/static/tempavatars/"+filenametemp
    res=bl.exportAsGLTF(pathGLTF)
    json_Data = bl.getAnimations()
    url = request.url_root+"static/tempavatars/"+filenametemp
    json_out = {"result": "ok","animations":json_Data,"path":url}
    del bl
    return json_out
    '''
    return ""



@app.route("/api/models/refresh",methods = ['GET'])
def initmodels():
    files = Utils.getAllModels(app.config['ROOT_DIR'] )
    print("files "+str(files))
    if(len(files)==0):
        return -1
    mongo = app.config['mongo']
    print("MongoDB iniciado...")
    '''
    for file in files:
        res = mongo.db.models.find_one({"filename": file})
        if(res == None):
            collection = mongo.db["models"]
            model = Utils.getJSONEmptyModel(app.config['ROOT_DIR'])
            model['type'] = file.rsplit('.', 1)[1].lower()
            model['path'] = structure['models']
            model['filename'] = file
            model['lastupdate'] = int(time.time())
            collection.insert_one(model)
    json_out = {"result": "ok"}
    return json.dumps(json_out)
    '''

@app.route("/api/avatar",methods = ['GET','POST'])
def avatar():
    json_data = request.json
    command = BLENDER_PATH+' --background --python '+BLENDER_SCRIPT_PATH+' \'{"option":'+str(CONST_GENERATE_AVATAR)+',"rootdir":"'+app.config['ROOT_DIR']+'","json":'+json.dumps(json_data)+'}\' '
    output=os.popen(command).read()
    print("OUTPUT AVATAR ",output)
    outputbueno = re.search(r'%@%(.*?)%@%', output).group(1)
    print("OUTPUT BUENO avatar",outputbueno)
    jsn = json.loads(outputbueno)
    jsn['path'] =request.url_root+"static/tempavatars/"+jsn['path']
    print("JSN PATH",jsn['path'])
    return jsn
    '''
    url=""
    if request.method == 'POST':
        json_data = request.json
        #print("data final", json_data)
        path = app.config['ROOT_DIR'] + "/static/models/" +json_data['model']
        mo = BlenderServices(1, path)
        mo.cleanAll()
        mo.loadModel()
        for x in json_data['items']:
            #print("-------ITEM ---------",x['name'])
            if x['visible']==0:
                print("ITEM A OCULTAR:", x['name'])
                mo.setHideItemByName(x['name'],True)
            if x['type']==1 and x['visible']==1:
                value = x['value'].replace("#","");
                print("ITEM CON COLOR A CAMBIAR:",value)
                mo.changeColorMaterialByName(x['name'],int(value,16))
            if x['type']==2 and x['visible']==1:
                print("ITEM CON TEXTURA A CAMBIAR",x['value'],"    ",x['name'])
                mo.changeTextureMaterialByName(x['name'],app.config['ROOT_DIR'] + "/static/images/"+x['value'])

        split = json_data['model'].split(".")
        filenametemp = "avatar_" + split[0] + "_" + str(int(time.time())) + "." + split[1]
        print("FICHERO TEMPORAL ",filenametemp)
        pathGLTF = app.config['ROOT_DIR'] + "/static/tempavatars/" + filenametemp
        print("RUTA TEMPORAL ",pathGLTF)
        res = mo.exportAsGLTF(pathGLTF)
        url = request.url_root + "static/tempavatars/" + filenametemp + ".glb"
    else:
        #generamos uno temporal
        json_data = request.json
        pass
    json_out = {"result": "done","path":url}
    return json.dumps(json_out)
    '''
    return ""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    print("empezamos")
    data = dict(request.form)
    exit=False
    i=0
    photos = []
    while exit==False:
        f = "file"+str(i)
        b = f in data
        if b==True:
            print("HAY UN ",f)
            img = data[f]
            imgdata = base64.b64decode(img)
            filenametemp = "photo_" +f+"_"+ str(int(time.time())) + ".jpg"
            print("FILENAME TEMP ",filenametemp)
            filename = app.config['ROOT_DIR'] + "/static/images/" + filenametemp
            print(filename)
            with open(filename, 'wb') as f:
                f.write(imgdata)
            print("guardado")
            path = request.url_root + "static/images/" + filenametemp
            print(path)
            photos.append(filenametemp)
            i= i+1
        else: exit=True

    json_out = {"result": "created","names":photos}
    return json_out


    #pathGLTF = app.config['ROOT_DIR'] + "/static/tempavatars/" + filenametemp;
    #print("PATH:" + pathGLTF)
    #res = bl.exportAsGLTF(pathGLTF)
    #print("RES:" + str(res))
    #json_Data = bl.getListaPartesModeloJSON()


    '''
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    print("existe el fichero")
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        bl.printCustom("no selected file")
        bl = BlenderServices(1, "")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        bl.printCustom("FILE TIENE NOMBRE Y ESTA PERMITIDO")
        filename = str(int(time.time()))+"_"+secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], filename))
        #return redirect(url_for('download_file', name=filename))
    else:
        return json.dumps({"result":"fail"})
    json_out = {"result": "created","path":os.path.join(structure['images']+filename)}
    return json.dumps(json_out)
    '''

if __name__ == '__main__':
    #print(app.config['UPLOAD_FOLDER_IMAGES'])
    #print(os.path.exists(app.config['UPLOAD_FOLDER_IMAGES']+"/borrar.txt"))
    #print("AQUII")
    initmodels()
    #print("running flask")

    app.run(host='0.0.0.0',port=5001)
    #flask run --host=0.0.0.0
