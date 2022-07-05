'''
./Blender --background --python "/Users/bihut/Google Drive/Mi unidad/UGR/Proyectos/BonAppetit/BonAppetit-Backend/app.py"
./blender --background --python "/home/bihut/dev/Proyectos/BonAppetit-Backend/app.py"
/Applications/Blender\ 3.0.app/Contents/MacOS/Blender --background <PATH BLEND FILE> --python <PATH SCRIPT>"
'''

import shutil
import time
import bpy
import sys
import json
import os

CONST_FBX = "fbx"
CONST_BLEND ="blend"
CONST_GLTF = "gltf"
CONST_GLB = "glb"
CONST_COMPLEX="complex"
CONST_LIST_MODELS=0
CONST_LOAD_MODEL=1
CONST_GENERATE_AVATAR=2
CONST_REGEX = "%@%"

class BlenderServices:
    modelid=-1
    path=""

    def __init__(self, id,path):
        self.modelid = id
        self.path = path

    def printCustom(self,data):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'CONSOLE':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")


    def getListaPartesModeloJSON(self):
        items = self.getListaPartesModelo()
        items2 = []
        json_out = {"modelid": self.modelid, "items": []}
        try:
            for o in items:
                items2.append(o.name)
        except:
            pass
        return items2


    def getListaPartesModelo(self):
        objetos =[]
        try:
            for collection in bpy.data.collections:
               for obj in collection.all_objects:
                  objetos.append(obj)
        except:
            pass
        return objetos
    
    def getAnimations(self):
        objetos =[]
        values = {}
        i = 0
        for ob in bpy.context.scene.objects:
            if not ob.animation_data:
                continue
            for track in ob.animation_data.nla_tracks:
                values[str(i)] = track.name
                i = i + 1
        for b in values:
            objetos.append(values[b])
            # mo.printCustom(" 2 "+track.name)

        objetos = list( dict.fromkeys(objetos) )
        json_out = {"animations":objetos}    
        return objetos
        

    def setHideItemByName(self,name,visible):
        item = bpy.data.objects[name]
        if item:
            self.setHideItem(item,visible)
        
    def setHideItem(self,item,visible):
        item.hide_viewport = visible
        item.hide_render = visible
        item.hide_set(visible)
        objs = bpy.data.objects
        objs.remove(item, do_unlink=True)

    def srgb_to_linearrgb(self, c):
        if   c < 0:       return 0
        elif c < 0.04045: return c/12.92
        else:             return ((c+0.055)/1.055)**2.4

    def hex_to_rgb(self,h,alpha=1):
        r = (h & 0xff0000) >> 16
        g = (h & 0x00ff00) >> 8
        b = (h & 0x0000ff)
        return tuple([self.srgb_to_linearrgb(c/0xff) for c in (r,g,b)] + [alpha])

    def changeColorMaterialByName(self,name, h):
        obj = bpy.context.scene.objects[name]
        self.changeColorMaterial(obj,obj.active_material.name,h)
    
    def changeColorMaterial(self,obj,material_name, h):
        mat =  bpy.data.materials.new(material_name)
        mat.use_nodes = True
        principled = mat.node_tree.nodes['Principled BSDF']
        principled.inputs['Base Color'].default_value = self.hex_to_rgb(h)
        obj.data.materials[0] = mat

    
    def changeTextureMaterialByName(self,name,image_file):
        obj = bpy.context.scene.objects[name]
        self.changeTextureMaterial(obj,image_file,obj.active_material.name)
    
    def changeTextureMaterial(self,obj,image_file,material_name):
        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image = bpy.data.images.load(image_file)
        mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

    def changeMaterialColorAllItems(self,data):
        #print("LEN DE DATA"+str(len(data)))
        for item in data:
            obj = bpy.data.objects[item['name']]
            self.changeColorMaterial(obj,obj.active_material.name,int(item['color'],16))

    def megapurge(self):
        removeThese = bpy.context.copy()
        removeThese['selected_objects'] = list(bpy.context.scene.objects)
        bpy.ops.object.delete(removeThese)

    def cleanAll(self):
        self.megapurge()
        '''
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)
        #quitar todos los materials
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)
            #material.user_clear()
        try:
            objs = bpy.data.objects
            objs.remove(objs["Cube"], do_unlink=True)
            objs.remove(objs["Camera"], do_unlink=True)
            objs.remove(objs["Light"], do_unlink=True)
        except:
            pass
        '''
    def loadModel(self):
        #try:
        #    bpy.ops.object.mode_set(mode='OBJECT')
        #except:
        #    pass
        ext = self.path.rsplit('.', 1)[1].lower()
        if(ext==CONST_FBX):
            self.loadModelFBX()
        elif(ext==CONST_BLEND):
            self.loadModelBlend()
        elif(ext==CONST_GLTF):
            self.loadModelGLTF()
        elif(ext==CONST_GLB):
            self.loadModelGLTF()
        elif(ext==CONST_COMPLEX):
            self.loadModelComplex()

    def loadModelComplex(self):
        if(self.path==None):
            return None
        #pathaux = self.path.rsplit('.', 1)[0].lower()+"/"
        if not os.path.exists(self.path):
            return None
        files = os.listdir(self.path)
        for file in files:
            pathaux = self.path+"/"+file
            #self.printCustom(pathaux)
            bpy.ops.import_scene.gltf(filepath=pathaux)

    def moveAllItemsToCollection(self,name):
        objs = []
        for collection in bpy.data.collections:
            print(collection.name)
            if collection.name == name:
                for obj in collection.all_objects:
                    objs.append(obj)
        
        if len(objs) != 0:
            return 0
        
        bpy.ops.object.select_all(action='SELECT')
        C = bpy.context

        # List of object references
        objs = C.selected_objects

        # Set target collection to a known collection 
        coll_target = C.scene.collection.children.get(name)

        # Set target collection based on the collection in context (selected) 
        #coll_target = C.collection

        # If target found and object list not empty
        if coll_target and objs:

            # Loop through all objects
            for ob in objs:
                # Loop through all collections the obj is linked to
                for coll in ob.users_collection:
                    # Unlink the object
                    coll.objects.unlink(ob)

                # Link each object to the target collection
                coll_target.objects.link(ob)
                
    def loadModelGLTF(self):
        if (self.path == None):
            return None
        bpy.ops.import_scene.gltf(filepath=self.path)

    

    def loadModelBlend(self):
        if(self.path==None):
           return None
        #print("PATH ",self.path)
        #v = self.app.config['ROOT_DIR']+"/static/scriptExportGLTF.py"
        #print("PATH SCRIPT ",v)
        #print("FINAL ","/Applications/Blender 3.0.app/Contents/MacOS/Blender --background "+self.path+" --python "+v)
        #os.system("/Applications/Blender 3.0.app/Contents/MacOS/Blender --background "+self.path+" --python "+v)
        bpy.ops.wm.open_mainfile(filepath=self.path)


    def loadModelFBX(self):
        if(self.path==None):
           return None
        bpy.ops.import_scene.fbx(filepath = self.path)

    def enableDisableElements(self,data):
        #objs = getListaPartesModelo()
        for item in data:
            self.setHideItem(bpy.data.objects[item['name']],item['hide'])

    def generateModel(self,data):
        for item in data['items']:
            obj = bpy.data.objects[item['name']]
            self.setHideItem(obj,item['hide'])
            if(item['hide']==False):
                if(item['color']!=None):
                    self.changeColorMaterial(obj,obj.active_material.name,int(item['color'],16))
                elif (item['texture']!=None):
                    self.changeTextureMaterial(obj,item['texture'],obj.active_material.name)

    def exportAsGLTF(self,output):
        #ctx = bpy.context.copy()
        #ctx = bpy.context
        # because the active_object attribute isn't created until the user interacts
        # with the scene we create one here but we don't need to set it to anything
        #ctx['active_object'] = None
        #res=bpy.ops.export_scene.gltf(
        #    filepath=output,
        #     #export_selected=False,
        #    use_selection=False
        #)
        #bpy.ops.export_scene.gltf(ctx, export_format="GLB", filepath=output)
        bpy.ops.export_scene.gltf(export_format="GLB", filepath=output,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
        
        #return res


    def getElementsCount(self): 
        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        total_vertices = 0
        total_edges = 0
        total_polygons = 0
        total_mesh = 0
        csv_aux = "mesh_name,vertices,edges,polygons\n"
        for obj in sel_objs:
            total_mesh += 1
            #self.printCustom("MALLA "+obj.name+" -------")
            data = bpy.data.meshes[obj.name]
            # 'Плоскость' - name of manually selected mesh, for example
            

            # VERTICES
            vertices = [];
            for _ in data.vertices: vertices.append(list(_.co))

            #self.printCustom("vertices:"+str(len(vertices)));

            # EDGES
            edges = [];
            for _ in data.edges: edges.append(list(_.vertices))

            #self.printCustom("EDGES:"+str(len(edges)));

            # POLYGONS
            polygons=[];
            for _ in data.polygons: polygons.append(list(_.vertices))

            #self.printCustom("POLYGONS"+str(len(polygons)));
            total_vertices += len(vertices)
            total_edges += len(edges)
            total_polygons += len(polygons)
            csv_aux += obj.name+","+str(len(vertices))+","+str(len(edges))+","+str(len(polygons))+"\n"
        
        self.printCustom("-----------------------------")
        self.printCustom("Total Mallas:"+str(total_mesh))
        self.printCustom("Total Vertices:"+str(total_vertices));
        self.printCustom("Total Edges:"+str(total_edges));
        self.printCustom("Total Polygons:"+str(total_polygons))
        return csv_aux

'''
path = "/home/bihut/dev/Proyectos/BonAppetit-Backend/static/models/Atoona.complex"
#path = "/home/bihut/atoona.gltf"
mo = BlenderServices(1,path) 
mo.cleanAll()
mo.loadModel()
mo.printCustom("-------------- MODELO: "+path)
mo.moveAllItemsToCollection("Collection")
csv_aux=mo.getVerticesCount()
res = mo.getAnimations()
mo.printCustom("animations:"+str(len(res)))
mo.exportAsGLTF("/home/bihut/atoona_prueba.gltf")


path = "/home/bihut/dev/Proyectos/BonAppetit-Backend/static/models/RobotExpressive.glb"
mo = BlenderServices(1,path) 
mo.cleanAll()
mo.loadModel()
mo.printCustom("-------------- MODELO: "+path)
mo.moveAllItemsToCollection("Collection")
mo.getVerticesCount()
res = mo.getAnimations()
mo.printCustom("animations:"+str(len(res)))
mo.exportAsGLTF("/home/bihut/robot_prueba.gltf")

'''
'''
path = "/home/bihut/dev/Proyectos/BonAppetit-Backend/static/models/Atoona.complex/Avatar_Atoona.gltf"
mo = BlenderServices(1,path) 
mo.cleanAll()
mo.loadModel()
mo.printCustom("-------------- MODELO: "+path)
#mo.moveAllItemsToCollection("Collection")
mo.getElementsCount()
#res = mo.getAnimations()
#mo.printCustom("animations:"+str(len(res)))
mo.exportAsGLTF("/home/bihut/atoona_chumbo_prueba.gltf")

'''
'''
path = "/home/bihut/dev/Proyectos/BonAppetit-Backend/static/models/Dummy_test_UGR.fbx"
mo = BlenderServices(1,path) 
mo.cleanAll()
mo.loadModel()
mo.printCustom("-------------- MODELO: "+path)
mo.moveAllItemsToCollection("Collection")
mo.getelementsCount()
res = mo.getAnimations()
mo.printCustom("animations:"+str(len(res)))
mo.exportAsGLTF("/home/bihut/pelota_animada_prueba.gltf")

#mo.printCustom("----------------------CSV--------------------------")
#mo.printCustom(csv_aux)

#res=mo.getListaPartesModeloJSON()
#mo.printCustom("------------ITEMS--------------_")
#mo.printCustom(res)
#mo.printCustom("------------Animations--------------_")
#res = mo.getAnimations()
#res = list( dict.fromkeys(res) )
#mo.printCustom(res)
#obj = bpy.context.active_object

#mo.exportAsGLTF("/home/bihut/atoonav3.gltf")

#print("PARAMs0",sys.argv)
#print("%@%",sys.argv[len(sys.argv)-1],"%@%")


'''

#stri = sys.argv[len(sys.argv)-1]
stri= '{"option":2, "rootdir":"/tmp/DATA",  "json":{ "model":"dragonbonappetit.fbx","items":[{"name":"Dragon_Mesh","visible":1,"type":1,"value":"#FF0000"}]}}' #'{"option":1,"rootdir":"/home/bihut/dev/Proyectos/BonAppetit-Backend","name":"Atoona.complex"}' 
jsn=json.loads(stri)

if(jsn['option']==0):
    print(CONST_REGEX,"ES CERO",CONST_REGEX)
elif(jsn['option']==1):#obtener info de un modelo
    name = jsn['name']
    rootdir = jsn['rootdir']
    path = rootdir+"/static/models/" + name
    print("PATH ES "+path)
    bl = BlenderServices(1,path)
    bl.printCustom("PATH ES---"+path)
    #print("PATH ES "+path)
    bl.cleanAll()
    bl.loadModel()
    bl.moveAllItemsToCollection("Collection")
    split = name.split(".")
    filenametemp = "temp_" + split[0] + "_" + str(int(time.time())) + "." + split[1]
    pathGLTF =rootdir + "/static/tempavatars/" + filenametemp
    bl.printCustom("PATH GLTF" + pathGLTF)
    if (split[1] == CONST_GLB or split[1] == CONST_GLTF):
        src = path
        dest = pathGLTF
        shutil.copyfile(src, dest)
        json_Data = bl.getListaPartesModeloJSON()
        json_Anims = bl.getAnimations()
        json_out = {"result": "ok", "items": json_Data, "animations": json_Anims, "path": dest}
        print(CONST_REGEX, json.dumps(json_out), CONST_REGEX)
    else:
        res = bl.exportAsGLTF(pathGLTF)
        json_Data = bl.getListaPartesModeloJSON()
        json_Anims = bl.getAnimations()
        filenametemp = filenametemp+".glb"
        json_out = {"result": "ok", "items": json_Data, "animations": json_Anims, "path": filenametemp}
        print(CONST_REGEX,json.dumps(json_out),CONST_REGEX)
elif(jsn['option']==CONST_GENERATE_AVATAR):
    #print("DATA JSON 0 ", jsn)
    json_data = jsn['json']
    #print("DATA JSON",json_data)
    rootdir = jsn['rootdir']
    path = rootdir + "/static/models/" + json_data['model']
    mo = BlenderServices(1, path)
    mo.cleanAll()
    mo.loadModel()
    mo.printCustom(mo.getListaPartesModeloJSON())
    for x in json_data['items']:
        if x['visible'] == 0:
            mo.setHideItemByName(x['name'], True)
        if x['type'] == 1 and x['visible'] == 1:
            value = x['value'].replace("#", "");
            mo.printCustom("VALUE" + str(value))
            mo.printCustom("NAME" + x['name'])
            mo.changeColorMaterialByName(x['name'], int(value, 16))
        if x['type'] == 2 and x['visible'] == 1:
            mo.changeTextureMaterialByName(x['name'], rootdir + "/static/images/" + x['value'])
    #print("JSONDATA","json_data")
    split = json_data['model'].split(".")
    #print("SPLIT",split)
    filenametemp = "avatar_" + split[0] + "_" + str(int(time.time())) + "." + split[1]
    #print("FILENAMETEMP",filenametemp)
    pathGLTF = rootdir + "/static/tempavatars/" + filenametemp
    res = mo.exportAsGLTF(pathGLTF)
    url = "static/tempavatars/" + filenametemp + ".glb"
    json_out = {"result": "done", "path": url}
    print(CONST_REGEX, json.dumps(json_out), CONST_REGEX)

#print(CONST_REGEX,stri,CONST_REGEX)

'''
path = "/Users/bihut/Documents/EjemplosBlender/character1.fbx"
mo = BlenderServices(1,path) 
mo.cleanAll()
mo.loadModel()
mo.setHideItemByName("cape",True)
mo.setHideItemByName("cape1",True)
bpy.ops.object.select_all(action='SELECT')
pathGLTF ="/Users/bihut/PersonajeBueno2.gltf"
mo.exportAsGLTF(pathGLTF)
'''
'''
path ="/Users/bihut/Documents/EjemplosBlender/personajebueno.blend"
#path ="/Users/bihut/Downloads/borrar/AvatarTest2/Preview/Pelota_ModeloAnimado.fbx"
mo = BlenderServices(1,path) 
mo.loadModel()
json=mo.getListaPartesModeloJSON()
mo.printCustom(json)
#mo.cleanAll()
#mo.loadModel()
#mo.setHideItemByName("cape",True)
h = 
json=mo.getListaPartesModeloJSON()
#animations = mo.getAnimations()

#mo.printCustom(animations);
#mo.changeColorMaterialByName("Pelota",h)
#mo.changeColorMaterialByName("cape",h)
#pathImg="/Users/bihut/zappa.jpeg"
#mo.changeTextureMaterialByName("Pelota",pathImg)
pathGLTF ="/Users/bihut/PersonajeBueno.gltf"
mo.exportAsGLTF(pathGLTF)
'''
'''

    Ejemplo de json 
    {
	"items": [{
			"name": "cape",
			"hide": false
		},
		{
			"name": "cape1",
			"hide": true
		}
	]
}


{
    "type": 0,
    "modelid": "",
    "animnation": "",
    "items": [{
        "name": "cape",
        "hide": false
    }, {
        "name": "cape1",
        "hide": true
    }]
}

{
	"type": 2,
	"modelid": "",
	"animnation": "",
	"items": [{
		"name": "cape",
		"hide": false,
		"color": "0xFF0000",
		"texture": null
	}, {
		"name": "cape1",
		"hide": true,
		"color": "0x0000FF",
		"texture": null
	}]
}
'''
