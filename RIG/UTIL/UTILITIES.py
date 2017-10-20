# -*- encoding: utf-8 -*-

from os import listdir
from os.path import isfile, join

import maya.cmds as cmds
from pymel.core import *


# Devuelve un diccionario con las carpetas y archivos del path que le
# pases y puede buscar palabra especificas en archivo

def addAttr_FromFolders( sel , path , extension , filtering , contarArchivos): #del archivosCarpetas
    '''
    Cuenta la cantidad de archivos EXTENSION filtrando por FILTERING. Agrega atributos a SEL por cada carpeta encontrada.
    Si contarArchivos == 0, el maximo de cada atributo es seteado a la cantidad de archivos encontrada en esa carpeta.
    Si contarArchivos != 0, el maximo de cada atributo es seteado arbitrariamente al valor de contarArchivos.

    Ejemplos:

        # asigna a los atributos 31 como maximo.

        sel=ls(sl=1)[0]
        UTILITIES.addAttr_FromFolders( sel , 'O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES' , 'png' , 'proxy', 31 )


        # asigna a los atributos la cantidad de archivos encontrada en la carpeta como maximo.

        asdf = sphere()[0]
        UTILITIES.addAttr_FromFolders( asdf , 'O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES' , 'png' , 'proxy', 0 )


    '''

    archivosCarpetas = dirs_files_dic(path , extension, filtering )
    for key in sorted( archivosCarpetas.keys() ):
        att = key.split('\\')[-1]   # spliteo nombre del atributo

        if not contarArchivos :
            cantidadArchivos = len( archivosCarpetas[key])
            offset           =  (1,0)[cantidadArchivos==0]
            frames = cantidadArchivos - offset
        else:
            frames = contarArchivos
        sel.addAttr( att , keyable=True ,  min=0 , max = frames  , dv=0 , at='long')
        # esto es lo que habiamos hablado pero no sé si es realmente conveniente. charlarlo.
        #sel.addAttr( att+'MIRROR' , keyable=True ,  min=0 , max= len( archivosCarpetas[key])-1 , dv=0 , at='long')




def dirs_files_dic(mypath, filterExtension, keyWord=''):
    '''
    type (string) mypath: Ruta de carpeta.
    type (string) filterExtension: contiene el tipo de extencion a buscar.
    type (string) keyWord: enlista archivos si contiene la palabra dentro de keyWord.
    Returns a dic { Dir : files in Dir }. A dictonary with subdirectories and files inside them from a directory input.
    Example:
        dirs_files_dic('O:\EMPRESAS\RIG_FACE2D\ScriptingGuideRig\Maps','png', 'proxy')


    '''
    returnDic = {}
    dirs = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
    for subdir in dirs:
        subdir = mypath + '\\' + subdir
        onlyfiles = [f for f in listdir(subdir) if ( isfile(join(subdir, f)) and os.path.splitext(f)[1] == '.' + filterExtension) and keyWord in f]
        if not keyWord=='':
            fileText = []
            for f in onlyfiles:
                if keyWord in f:
                    fileText.append(f)
            returnDic[subdir] = fileText
        else:
            returnDic[subdir] = onlyfiles
    return returnDic


def createIfNeeded( node_Name , node_Type ):
    '''
    Creates a node_Type with named node_Name if it doesnt exist.
    Returns node_Name
    Example:
    '''
    if not objExists ( node_Name ) :
        nodeRet  =   createNode ( node_Type , n = node_Name )
    else:
        nodeRet   = node_Name
    return nodeRet

# Crea un offset en seleccion.
def offSetGrp(obj=None, suf=''):
    newName = ''
    newNode = None
    if cmds.nodeType(obj) == 'transform':
        newName = obj
        if '|' in newName:
            newName = str(obj.split('|')[-1])
        if '_' in str(newName) and (not suf in str(newName)):
            newName = str(newName[:newName.rfind("_")]) + suf
        else:
            newName = str(newName) + suf

        newNode = cmds.duplicate(obj, n=newName, parentOnly=True)
        cmds.parent(obj, newNode[0])
        return newNode[0]
    else:
        print str(obj) + ' necesitas que sea un nodo de transformacion.'


def extraControl(objs=[], nameSuf='ZTR', nameTrf='TRF', nameCNT='CNT', rad=14):
    # objs=cmds.ls(sl=1)
    grpYcnt = []
    for obj in objs:
        print obj
        if '|' in obj:
            obj = obj.split('|')[-1]
        if '_' in obj:
            newName = obj.split(obj.split('_')[-1:][0])[0]
        else:
            newName = obj
        # currentParent=cmds.listRelatives(obj,parent=1)
        ztr = cmds.group(em=True, n=str(newName + nameSuf))
        pcns = cmds.parentConstraint(obj, ztr)[0]
        scns = cmds.scaleConstraint(obj, ztr)[0]
        cmds.delete(pcns, scns)
        trf = cmds.duplicate(ztr, n=str(newName + nameTrf))[0]
        cmds.parent(trf, ztr)
        cnt = cmds.circle(radius=rad, nrx=1, normalZ=0,
                          name=str(newName + nameCNT))[0]
        pcns = cmds.parentConstraint(trf, cnt)
        scns = cmds.scaleConstraint(trf, cnt)
        cmds.delete(pcns, scns)
        cmds.parent(cnt, trf)
        # p=cmds.parent(obj,cnt)
        grpYcnt.append(ztr)
        grpYcnt.append(trf)
        grpYcnt.append(cnt)
    return grpYcnt


def compilarPySideUI(pathUI='', fileUI='', openFolder=False):
    def msg(msg=''):
        print msg
        mc.warning(msg)

    if pathUI and fileUI:
        if '.ui' in fileUI:
            fullPathUI = pathUI + '\\' + fileUI
            if os.path.exists(fullPathUI):
                fullPathPY = fullPathUI.replace('.ui', '.py')
                pyfile = open(fullPathPY, 'w')
                if pyfile:
                    compileUi(fullPathUI, pyfile, False, 4, False)
                    pyfile.close()
                    msg('SE COMPILO EN: ' + fullPathPY)
                    if openFolder:
                        os.startfile(pathUI)
                    return fullPathPY
            else:
                msg('No existe el directorio o archivo.')
        else:
            msg('Necesitas que contanga el nombre del archivo con extencion .ui')
    else:
        msg('No se especifico o no esta correcta la ruta o archivo de .ui')

'''
* DESCRIPCION *
Alinear y Crear offset
makeOffsetGrp('L_FOOT_HEEL_CNT','L_FOOT_HEEL_')
'''


def Aliniar(object=None, offsetGrp=None):
    # match object transform
    cmds.delete(cmds.parentConstraint(object, offsetGrp))
    cmds.delete(cmds.scaleConstraint(object, offsetGrp))


def makeOffsetGrp(object, prefix='noname', control=False, radio=1):

    objectParents = cmds.listRelatives(object, p=1)
    offsetGrp = cmds.group(n=prefix + '_TRF', em=1)
    if objectParents != None:
        Aliniar(object, offsetGrp)
        cmds.parent(offsetGrp, objectParents[0])
    if control:
        cnt = cmds.circle(n=prefix + '_CNT', normal=[1, 0, 0], r=radio)
        Aliniar(object, offsetGrp)
        Aliniar(object, cnt)
        # parent object under offset cnt
        cmds.parent(object, object)
        cmds.parent(cnt, offsetGrp)
    else:
        # Alinia al objeto
        Aliniar(object, offsetGrp)
        # parent object under offset group
        cmds.parent(object, offsetGrp)
    return offsetGrp


'''
* DESCRIPCION *
Activa plugin de Arnold y lo setea como currentRenderer.
'''


def arnoldON():
    # Cargo el pluging de arnold si no esta cargado
    if mc.pluginInfo('mtoa.mll', q=True, l=True):
        mc.setAttr('defaultRenderGlobals' +
                   '.currentRenderer', 'arnold', type='string')
        print 'Arnold it is ON'
    else:
        mc.loadPlugin('mtoa.mll')
        print 'Arnold ON'

    if not mc.getAttr('defaultRenderGlobals' + '.currentRenderer') == 'arnold':
        # Pongo como render el arnold
        mc.setAttr('defaultRenderGlobals' +
                   '.currentRenderer', 'arnold', type='string')
        print 'Arnold se puse como render predefinido'

    # get aov defauld
    if mc.getAttr('defaultRenderGlobals' + '.currentRenderer') == 'arnold':
        try:
            aov_list = mc.getAttr(
                'defaultArnoldRenderOptions.aovList', size=True)
        except:
            mc.setAttr('defaultRenderGlobals' +
                       '.currentRenderer', 'arnold', type='string')
    else:
        print 'Primero hay que setear arnold como motor principal de render'


'''
* DESCRIPCION *
Funciones de JSON para leer, sumar y guardar.
'''


def saveJSONFile(dataBlock, filePath):
    outputFile = open(filePath, 'w')
    JSONData = json.dumps(dataBlock, sort_keys=True, indent=4)
    outputFile.write(JSONData)
    outputFile.close()


def loadJSONFile(filePath):
    inputFile = open(filePath, 'r')
    JSONData = json.load(inputFile)
    inputFile.close()
    return JSONData


def writeJSONFile(dataBlock, filePath):
    f = open(filePath, 'a')
    d = json.dumps(dataBlock, sort_keys=True, indent=4)
    f.write(d)
    f.close()
'''
* DESCRIPCION *
Prende o apaga los atributos menos la visibilidad.
'''


def switch(onOff=True):
    sel = mc.ls(sl=1)
    if onOff:
        for o in sel:
            mc.setAttr(o + '.tx', lock=False, keyable=True, channelBox=False)
            mc.setAttr(o + '.ty', lock=False, keyable=True, channelBox=False)
            mc.setAttr(o + '.tz', lock=False, channelBox=False, keyable=True)
            mc.setAttr(o + '.rx', lock=False, channelBox=False, keyable=True)
            mc.setAttr(o + '.ry', lock=False, channelBox=False, keyable=True)
            mc.setAttr(o + '.rz', lock=False, channelBox=False, keyable=True)
            mc.setAttr(o + '.sx', lock=False, channelBox=False, keyable=True)
            mc.setAttr(o + '.sy', lock=False, channelBox=False, keyable=True)
            mc.setAttr(o + '.sz', lock=False, channelBox=False, keyable=True)
            mc.setAttr(o + '.v', lock=False, channelBox=False, keyable=True)
        print 'Unlock en todo.'
        onOff = False

    else:
        for x in sel:
            mc.setAttr(x + '.tx', lock=True, channelBox=False, keyable=False)
            mc.setAttr(x + '.ty', lock=True, channelBox=False, keyable=False)
            mc.setAttr(x + '.tz', lock=True, channelBox=False, keyable=False)
            mc.setAttr(x + '.rx', lock=True, channelBox=False, keyable=False)
            mc.setAttr(x + '.ry', lock=True, channelBox=False, keyable=False)
            mc.setAttr(x + '.rz', lock=True, channelBox=False, keyable=False)
            mc.setAttr(x + '.sx', lock=True, channelBox=False, keyable=False)
            mc.setAttr(x + '.sy', lock=True, channelBox=False, keyable=False)
            mc.setAttr(x + '.sz', lock=True, channelBox=False, keyable=False)
            mc.setAttr(x + '.v', lock=True, channelBox=False, keyable=True)
            print 'Lock en todo.'
            onOff = True
    return onOff

# Colocar control con offset en el lugar deseado.
# sn=extraControl(cmds.ls(sl=1,long=True))
