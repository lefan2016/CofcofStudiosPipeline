# -*- coding: utf-8 -*-
# @Date:   2017-10-10T11:13:42-03:00
# @Last modified time: 2017-10-29T03:47:33-03:00
import random
import re
import sys
from functools import partial

import UTILITIES #necesaria para funciones de diccionario y archivos
import maya.cmds as cmds
import pymel.core as pm

# path = r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\UTIL'
#
# if not path in sys.path:
#     sys.path.append(path)
# try:
#     import UTILITIES
#     reload(UTILITIES)
# except (RuntimeError, TypeError, NameError, IOError):
#     print 'NO SE PUDO IMPORTAR EL MODULO'


def setKeyNow(obj='C_head_01_CTRL', attr='r_ojo'):
    currentTimeX = cmds.currentTime(query=True)
    cmds.setKeyframe(obj, attribute=attr, t=[currentTimeX, currentTimeX])
    cmds.keyTangent(obj, at=attr, itt='linear', ott='linear')


def rotLayer(attr='l_ojo', ctr='C_head_01_CTRL',barraUI=None ,*args):
    if barraUI:
        attr = attr + '_ROT'
        if cmds.objExists(ctr + '.' + attr):
            val=cmds.floatSlider(barraUI,q=True,value=True)
            cmds.setAttr(ctr + '.' + attr, val)
            setKeyNow(ctr, attr)
        else:
            cmds.warning('No existe el atributo ',attr)

def resetSlide(attr,controlAttributos,value,slider,*args):
    cmds.floatSlider(slider,e=True,value=value)
    rotLayer(attr,controlAttributos,slider)

# Ocultara el layer en maya.
def displayLayer(attr='l_ojo', ctr='L_EYE_PUPILA_CNT', *args):

    attr = attr + '_VIS'
    print 'DisplayLayer de: ', attr, ctr
    if cmds.objExists(ctr + '.' + attr):
        currentVal = cmds.getAttr(ctr + '.' + attr)
        if currentVal:
            cmds.setAttr(ctr + '.' + attr, 0)
            setKeyNow(ctr, attr)
            print 'Capa apagada y key'
        else:
            cmds.setAttr(ctr + '.' + attr, 1)
            setKeyNow(ctr, attr)
            print 'Capa prendinda y key'


def getFrame(val=0, attr='r_ojo', ctr='L_EYE_PUPILA_CNT', *args):
    # Con esta funcion pregunto si existe el control que le estoy pasando por
    # argumento
    if cmds.objExists(ctr + '.' + attr):
        print 'Existe el control', ctr, attr, val
        currentVal = cmds.getAttr(ctr + '.' + attr)
        # Devuelve el evento que preciono
        mods = cmds.getModifiers()
        setKeyNow(ctr, attr)
        # pregunto si se preciono y es shift y agrego a la seleccion
        if (mods & 1) > 0:
            print 'Estas apretando shift'

            if 'l_' in attr:
                attr = 'r_' + attr.split('l_')[1]
                print 'Se seteo en el opuesto R tambien'
                cmds.setAttr(ctr + '.' + attr, val)
                setKeyNow(ctr, attr)
            elif 'r_' in attr:
                attr = 'l_' + attr.split('r_')[1]
                print 'Se seteo en el opuesto L tambien'
                cmds.setAttr(ctr + '.' + attr, val)
                setKeyNow(ctr, attr)
            else:
                cmds.warning(
                    'No contiene el otro lado de la misma imagen nombrada L_ o R_')
        # de lo contrario solo selecciono
        else:
            print 'No se apreto ningun otro boton'
            cmds.setAttr(ctr + '.' + attr, val)
    else:
        cmds.warning('No existe el atributo o variable ' + attr +
                     ', en el control ' + ctr + ' o necesita de un namespace.')



# Definimos una interfas grafica para el usuario
def botonesUI(directorios='', nameSpace='', sizeButtons=100, parents='', controlAttributos='L_EYE_PUPILA_CNT'):


    # Creo una fila con 3 columnos grandes
    cantButColumFila=7
    # color1=[0.24,0.31,0.24]
    color1 = random.uniform(0.0, 1.0), random.uniform(
        0.0, 1.0), random.uniform(0.0, 1.0)
    color2 = [0.3, 0.3, 0.3]

    # Contengo todo en un solo scroll grande


    rowGeneral2 = cmds.rowLayout(numberOfColumns=2, columnWidth2=(sizeButtons * cantButColumFila,sizeButtons * cantButColumFila),adjustableColumn2=1, columnAttach=[(1, 'left', 0),(2, 'both', 0)],parent=parents)
    cmds.frameLayout(label='CONTROLES', collapsable=False, bgc=color2,parent=rowGeneral2)
    colBtn = cmds.columnLayout(adjustableColumn=True)
    cmds.channelBox()
    f2=cmds.frameLayout(label='FACIALES', width=(sizeButtons * cantButColumFila)*3,height=(100*cantButColumFila),bgc=color2,parent=rowGeneral2)
    scroll = cmds.scrollLayout()
    rowGeneral3 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(sizeButtons * cantButColumFila,sizeButtons * cantButColumFila, sizeButtons * cantButColumFila),
                                adjustableColumn3=1, columnAttach=[(1, 'left', 0),(2, 'both', 0), (3, 'both', 0)])
    colRight = cmds.columnLayout(adjustableColumn=True,parent=rowGeneral3)
    colMid = cmds.columnLayout(adjustableColumn=True,parent=rowGeneral3)
    colLeft = cmds.columnLayout(adjustableColumn=True,parent=rowGeneral3)


    # creo los botones recoriendo el diccionario que creamos
    for key in directorios:
        # Ordeno los frames dependiendo de la letra que contengan las carpetas
        sideFace = key.split('\\')[-1]
        if 'l_' in sideFace:
            sideParent = colLeft
            colaps = False
        elif 'r_' in sideFace:
            sideParent = colRight
            colaps = False
        else:
            sideParent = colMid
            colaps = True

        # Creo una columna para los botones
        cl1 = cmds.columnLayout(adjustableColumn=True,parent=sideParent)
        frameIn = cmds.frameLayout(label=sideFace.upper(), collapsable=True,collapse=colaps, bgc=color1,parent=cl1)
        cl2 = cmds.columnLayout(cal='left', cat=['left', 0], columnOffset=[ 'left', 0],  adjustableColumn=True, parent=frameIn)
        cmds.button(label='DisplayLayer', command=partial( displayLayer, sideFace, controlAttributos))
        cmds.rowColumnLayout(numberOfRows=1,adjustableColumn=True)
        barraRotacion=cmds.floatSlider('barra-'+sideFace,min=-180, max=180, value=0, step=1)
        cmds.floatSlider(barraRotacion,edit=True,changeCommand=partial(rotLayer, sideFace, controlAttributos,barraRotacion),dragCommand=partial( rotLayer, sideFace, controlAttributos,barraRotacion))
        cmds.button( label ='R', bgc=[0.5,0.5,0.4],height=30,width=30,command=partial(resetSlide,sideFace,controlAttributos,0,barraRotacion),annotation='Resetea la rotacion de la capa.')
        cmds.setParent( '..' )

        expres = cmds.frameLayout(  label='Expresiones', collapsable=True, collapse=True)
        scroll2 = cmds.scrollLayout( childResizable=True,height=110,parent=expres)
        rcl1=cmds.rowColumnLayout(numberOfRows=3, bgc=color2)
        # Para diferenciar las carpeas o frames le pongo diferentes colores
        # r,g,b=random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)
        # creo por cada file un boton
        for ctrl in directorios[key]:
            # valFrame=[s.zfill(2) for s in re.findall(r'\b\d+\b', img)]
            val = [int(s) for s in re.findall(r'\b\d+\b', ctrl)][0]
            nameImg=ctrl
            # Solo si existe algo escrito en la variable nameSpace y si es asi
            # le agrego el nameSpace al control.
            if nameSpace is not '':
                ctrl = nameSpace + ctrl
            # Agrego el boton y la funcion, con el nombre del value del
            # diccionario
            cmds.symbolButton(ctrl, image=key + '\\' + nameImg, width=sizeButtons, height=sizeButtons, backgroundColor=color2,
                              annotation='( SHIFT+CLICK setea la misma cara opuesta. )', command=partial(getFrame, val, sideFace, controlAttributos))


    return colBtn


def UI(charName='MILO', directorios={}, nameSpace='', sizeButtons=60, controlAttributo='L_EYE_PUPILA_CNT'):
    # variable que contiene el nombre de dockControl
    WorkspaceName = '2DPICKER_UI-> ' + charName
    # Pregunto si existe la ventana workspaceControl y si existe la borro
    # antes de crearla nuevamente.

    if cmds.workspaceControl(WorkspaceName, exists=True): cmds.deleteUI(WorkspaceName)

    # ejecuto funcion de interfas y la guardo en un dock
    cmds.workspaceControl(WorkspaceName, initialHeight=600, initialWidth=510, floating=True,
                          retain=False,  dtm=('right', 1))
    b=botonesUI(directorios, nameSpace, sizeButtons, WorkspaceName, controlAttributo)
    print 'Se creo la interfaze ', WorkspaceName
    return b


def picker2D(obj, path='c:/coco', rangeV=30, nameUI='MILO', namespace='', sizeButtons=30, ext='png', keyWord='proxy'):
    if namespace:  # si tiene namespace se le agrega al nombre
        obj = namespace + ':' + obj
    # Con esta funcion creo los atributos en el objeto indicado
    UTILITIES.addAttr_FromFolders(obj, path, ext, keyWord, rangeV)

    # Con esta funcion creo la interface dependiendo la cantidad de carpetas y
    # archivos en FACES folder.
    directorios = UTILITIES.dirs_files_dic(path, ext, keyWord)
    # llamo a la funcion la cual ejecuta todo el resto.
    uip=UI(nameUI, directorios, namespace, 30, obj)
    return uip
'''
nameUI = 'MILO' #Nombre que utilizara la interface.
nameSpace = '' #NameSpace del personaje.
#Este es el nombre que le daremos a nuestra interfas el cual tiene que ser diferente por cada personaje
name='GABO_2'
#lista de controles
controles={'L_EYE':['l_Eye_CNT','l_eyelid_sup_CNT','l_eyelid_inf_CNT','l_extras_CNT','l_pupil_CNT'],
           'R_EYE':['r_Eye_CNT','r_eyelid_sup_CNT','r_eyelid_inf_CNT','r_extras_CNT','l_pupil_CNT'],
           'OTROS':['c_Pupils_CNT','extras_CNT'],
           'BOCA':['lengua_CNT','b_diente_CNT','a_diente_CNT','boca_CNT'],
           'CABEZA':['C_head_01_CTRL']}

obj='C_head_01_CTRL' #objeto que contiene los atributos animables.
path = 'O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES' #Carpeta ordenada donde se contiene los arhivos proxys.
rangeVariable=60 #Cantidad maxima de archivos que contiene una carpeta de proxy.
sizeButtons=30 #Tamaño de botonera

pickerUI=Picker2D(obj,path,rangeVariable,nameUI,nameSpace,sizeButtons)#Funcion que contiene toda la programacion necesaria para la UI
pickerBotonera.botonesUI(controles,nameSpace,[100,20],pickerUI)#Picker de controles
'''
