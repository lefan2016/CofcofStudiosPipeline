# @Date:   2017-10-26T01:08:44-03:00
# @Last modified time: 2017-10-30T02:00:42-03:00



import UTILITIES
reload(UTILITIES)
import pymel.core as pm
controler='C_head_01_CTRL'
nameSpace=''
path='O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES'
extension='png'
dirs=UTILITIES.dirs_files_dic(path,extension)
#objeto que contiene los atributos animables.

projections=cmds.ls(type='projection')
Aims = cmds.ls('*_AIMC',type='aimConstraint')
fileNodes = cmds.ls(type='file')
def smart_find(haystack, needle):
    if haystack.startswith(needle+" "):
        return True
    if haystack.endswith(" "+needle):
        return True
    if haystack.find(" "+needle+" ") != -1:
        return True
    return False
printes={}
#Conecta el tratibuto de frame con las variables correspondiente de la cara en el control principal
for subdir in dirs:
    att = subdir.split('\\')[-1]
    if nameSpace:
        controler=nameSpace+':'+controler
    if cmds.objExists(obj+'.'+att):#Si contiene el mismo file y el nombre del atributo coincide se conectara
        if fileNodes:
            for i in fileNodes:
                filePath = cmds.getAttr(i+'.fileTextureName')
                if not '.proxy.' in i:
                    fileInfile=(subdir+'\\'+dirs[subdir][0]).replace('\\','/')
                    if filePath == fileInfile:
                        #Conecto el dato de frames del control con los frames de la imagen
                        if not cmds.isConnected( controler+'.'+att , i+'.'+'frameExtension' ):
                            c=cmds.connectAttr(controler+'.'+att , i+'.'+'frameExtension', f=True)
                            printes[controler+'.'+att+' ---> ']=str(i)+'.'+'frameExtension'

#---------------------------------------------------------------------------------------------------------
#Conecta el atributo de visible de capa con las variables correspondiente de la cara en el control principal
    if projections:
        if cmds.objExists(obj+'.'+att+'_VIS'):
            for PRJ in projections:
                fileNode=cmds.listConnections(PRJ+'.image')[0]
                if fileNode:
                    filePath = cmds.getAttr(fileNode+'.fileTextureName')
                    if att in str(filePath.split('/')[-1]):#si existe el nombre del atributo dentro de la imagen conecta la capa
                        layer = str(cmds.listConnections( PRJ+'.outColor',plugs=True)[0])
                        if layer:
                            if not cmds.isConnected( controler+'.'+att+'_VIS' , layer.replace('color','isVisible') ):
                                v=cmds.connectAttr( controler+'.'+att+'_VIS' , layer.replace('color','isVisible'), f=True)
                                printes[controler+'.'+att+'_VIS'+' ---> ']= layer.replace('color','isVisible')
#---------------------------------------------------------------------------------------------------------
#Conecta el atributo de rotacion de capa con las variables correspondiente de la cara en el control principal
    if Aims:
        if cmds.objExists(obj+'.'+att+'_ROT'):
            for aim in Aims:
                if aim.startswith(att): #si existe el nombre del atributo en el nombre del constraint
                    if not cmds.isConnected( controler+'.'+att+'_ROT' , str(aim)+'.offset.offsetZ'):
                        cmds.connectAttr( controler+'.'+att+'_ROT' , str(aim)+'.offset.offsetZ', f=True)
                        printes[controler+'.'+att+'_ROT'+' ---> ']= str(aim)+'.offset.offsetZ'
                    else:
                        printes[controler+'.'+att+'_ROT'+' ---> ']= 'conectado'

for key,value in printes.items():
    print key , value
