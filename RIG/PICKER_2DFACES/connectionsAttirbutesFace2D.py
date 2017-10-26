# @Date:   2017-10-26T01:07:51-03:00
# @Last modified time: 2017-10-26T01:07:54-03:00
path=r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\UTIL'
if not path in sys.path:
    sys.path.append(path)
import UTILITIES
reload(UTILITIES)
import pymel.core as pm
controler='C_head_01_CTRL'
nameSpace=''
path='O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES'
extension='png'
layerTexture='Face_LTX' #objeto que contiene los atributos animables.

dirs=UTILITIES.dirs_files_dic(path,extension)
fileNodes = cmds.ls(type='file')
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
                        if not cmds.isConnected( controler+'.'+att , i+'.'+'frameExtension' ):
                            c=cmds.connectAttr(controler+'.'+att , i+'.'+'frameExtension', f=True)
                            print 'coneccion de: ', c
#---------------------------------------------------------------------------------------------------------
    prjNodes = cmds.ls(type='projection')
    if prjNodes:
        if cmds.objExists(obj+'.'+att+'_VIS'):
            for prj in prjNodes:

            multiAttrTexture = cmds.listAttr( layerTexture+'.image',multi=True,inUse=True,string='inputs' )
        cmds.connectAttr( controler+'.'+att+'_VIS' , RIG_milo_0049_DEMO:Face_LTX.inputs[10].isVisible;
#---------------------------------------------------------------------------------------------------------
    prjNodes = cmds.ls(ACNS,type='aimConstraint')
        if cmds.objExists(obj+'.'+att+'_VIS')
