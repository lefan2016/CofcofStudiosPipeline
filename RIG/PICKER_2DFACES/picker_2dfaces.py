# @Date:   2017-10-10T11:13:42-03:00
# @Last modified time: 2017-10-23T01:20:37-03:00

import random
import re
import sys
from functools import partial

import maya.cmds as cmds

path = r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\UTIL'
path2 = r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\PICKER_2DFACES'
if not (path or path2) in sys.path:
    sys.path.append(path)
    sys.path.append(path2)
try:
    import UTILITIES
    reload(UTILITIES)
except (RuntimeError, TypeError, NameError, IOError):
    print 'NO SE PUDO IMPORTAR EL MODULO'

name = 'MILO'
nameSpace = ''
cabezaControl = 'L_EYE_PUPILA_CNT'
mypath = 'O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES'
directorios = UTILITIES.dirs_files_dic(mypath, 'png', 'proxy')

def setKeyNow(obj='L_EYE_PUPILA_CNT',attr='r_ojo'):
    currentTimeX=cmds.currentTime( query=True )
    cmds.setKeyframe( obj, attribute=attr, t=[currentTimeX,currentTimeX] )
    cmds.keyTangent(obj, at=attr, itt='linear', ott='linear')
    print 'KEY en: ',obj,attr
#Ocultara el layer en maya.
def displayLayer(attr='l_ojo', ctr='L_EYE_PUPILA_CNT', *args):

    attr=attr+'_VIS'
    print 'DisplayLayer de: ',attr, ctr
    if cmds.objExists(ctr + '.' + attr):
        currentVal = cmds.getAttr(ctr + '.' + attr)
        if currentVal:
            cmds.setAttr(ctr + '.' + attr, 0)
            setKeyNow(ctr,attr)
            print 'Capa apagada y key'
        else:
            cmds.setAttr(ctr + '.' + attr, 1)
            setKeyNow(ctr,attr)
            print 'Capa prendinda y key'


def getFrame(val=0, attr='r_ojo', ctr='L_EYE_PUPILA_CNT', *args):

    # Con esta funcion pregunto si existe el control que le estoy pasando por
    # argumento
    if cmds.objExists(ctr + '.' + attr):
        print 'Existe el control',ctr,attr, val
        currentVal = cmds.getAttr(ctr + '.' + attr)
        # Devuelve el evento que preciono
        mods = cmds.getModifiers()
        setKeyNow(ctr,attr)
        # pregunto si se preciono y es shift y agrego a la seleccion
        if (mods & 1) > 0:
            print 'Estas apretando shift'

            if 'l_' in attr:
                attr='r_'+attr.split('l_')[1]
                print 'Se seteo en el opuesto R tambien'
                cmds.setAttr(ctr + '.' + attr, val)
                setKeyNow(ctr,attr)
            elif 'r_' in attr:
                attr='l_'+attr.split('r_')[1]
                print 'Se seteo en el opuesto L tambien'
                cmds.setAttr(ctr + '.' + attr, val)
                setKeyNow(ctr,attr)
            else:
                cmds.warning('No contiene el otro lado de la misma imagen nombrada L_ o R_')
        # de lo contrario solo selecciono
        else:
            print 'No se apreto ningun otro boton'
            cmds.setAttr(ctr + '.' + attr, val)
    else:
        cmds.warning('No existe el atributo o variable '+attr+', en el control '+ctr+ ' o necesita de un namespace.')

# Definimos una interfas grafica para el usuario
def botonesUI(directorios='', nameSpace='',sizeButtons=100,parents='',controlAttributos='L_EYE_PUPILA_CNT'):

    # Contengo todo en un solo scroll grande
    scroll=cmds.scrollLayout( 'scrollLayout', parent=parents)
    # Creo una fila con 3 columnos grandes
    rowGeneral=cmds.rowLayout( numberOfColumns=3, columnWidth3=(sizeButtons*6, sizeButtons*6, sizeButtons*6), adjustableColumn3=1, columnAlign=(1, 'right'), columnAttach=[(1, 'left', 0), (2, 'both', 0), (3, 'left', 0)] )
    colRight=cmds.columnLayout(adjustableColumn=True,parent=rowGeneral)
    colMid=cmds.columnLayout(adjustableColumn=True,parent=rowGeneral)
    colLeft=cmds.columnLayout(adjustableColumn=True,parent=rowGeneral)
    #color1=[0.24,0.31,0.24]
    color1=random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)
    color2=[0.3,0.3,0.3]

    # creo los botones recoriendo el diccionario que creamos
    for key in directorios:
        # Ordeno los frames dependiendo de la letra que contengan las carpetas
        sideFace=key.split('\\')[-1]
        if 'l_' in sideFace:
            sideParent=colLeft
            colaps=False
        elif 'r_' in sideFace:
            sideParent=colRight
            colaps=False
        else:
            sideParent=colMid
            colaps=True

        # Creo una columna para los botones
        cl1=cmds.columnLayout(adjustableColumn=True,parent=sideParent)

        frameIn=cmds.frameLayout(label=sideFace.upper(),collapsable=True,parent=cl1,bgc=color1)
        cl2=cmds.columnLayout( cal='right',cat=['both',0], columnOffset = ['both', 0] ,  adjustableColumn=True , parent = frameIn )

        cmds.button(label='DisplayLayer', command= partial(displayLayer,sideFace,controlAttributos))

        expres=cmds.frameLayout(label='Expresiones',collapsable=True,collapse=colaps)
        cmds.rowColumnLayout( numberOfRows=4,bgc=color2)
        # Para diferenciar las carpeas o frames le pongo diferentes colores
        #r,g,b=random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)
        # creo por cada file un boton
        for ctrl in directorios[key]:
            # valFrame=[s.zfill(2) for s in re.findall(r'\b\d+\b', img)]
            val=[int(s) for s in re.findall(r'\b\d+\b', ctrl)][0]

            # Solo si existe algo escrito en la variable nameSpace y si es asi
            # le agrego el nameSpace al control.
            if nameSpace is not '':
                ctrl = nameSpace + ctrl
            # Agrego el boton y la funcion, con el nombre del value del
            # diccionario
            cmds.symbolButton(ctrl, image=key +'\\'+ctrl, width=sizeButtons, height=sizeButtons, backgroundColor=color2 ,
                              annotation='( SHIFT+CLICK setea la misma cara opuesta. )', command=partial(getFrame, val, sideFace, controlAttributos))


def UI(charName='MILO', directorios={}, nameSpace='', sizeButtons=60,controlAttributo='L_EYE_PUPILA_CNT'):
    # variable que contiene el nombre de dockControl
    WorkspaceName = '2DPICKER_UI_' + charName
    # Pregunto si existe la ventana workspaceControl y si existe la borro
    # antes de crearla nuevamente.

    if cmds.workspaceControl(WorkspaceName, exists=True):
        cmds.deleteUI(WorkspaceName)
        print 'Se borro', WorkspaceName
    # ejecuto funcion de interfas y la guardo en un dock
    cmds.workspaceControl(WorkspaceName, initialHeight=500,initialWidth=500, floating=False,
                          retain=False,  dtm=('right', 1))
    botonesUI( directorios, nameSpace,sizeButtons,WorkspaceName,controlAttributo)

# llamo a la funcion la cual ejecuta todo el resto.
UI(name, directorios, nameSpace,30,cabezaControl)
