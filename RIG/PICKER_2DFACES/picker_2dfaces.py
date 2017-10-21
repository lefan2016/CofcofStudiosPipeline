import maya.cmds as cmds
from functools import partial
import random
import sys
import re
path=r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\UTIL'
path2=r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\PICKER_2DFACES'
if not (path or path2) in sys.path:
	sys.path.append(path)
	sys.path.append(path2)
try:
    import UTILITIES
    reload(UTILITIES)
except (RuntimeError, TypeError, NameError,IOError):
    print 'NO SE PUDO IMPORTAR EL MODULO'

name='MILO'
nameSpace=''
cabezaControl='L_EYE_PUPILA_CNT'
mypath = 'O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES'
directorios = UTILITIES.dirs_files_dic(mypath, 'png', 'proxy')
print directorios

def getFrame(val='', attr='', ctr='C_head_01_CTRL',*args):
  	print 'Frame: '+ str(val)
	print 'Control: ' + ctr
	print 'NameAttr: ' + attr
	# Con esta funcion pregunto si existe el control que le estoy pasando por
	# argumento
	if cmds.objExists(ctr):
		currentVal = cmds.getAttr(ctr + '.' + str(attr))
		# Devuelve el evento que preciono
		mods = cmds.getModifiers()
		# pregunto si se preciono y es shift y agrego a la seleccion
		if (mods & 1) > 0:
			cmds.setAttr(ctr + '.' + str(attr), val)
		# de lo contrario solo selecciono
		else:
			cmds.setAttr(ctr + '.' + str(attr), currentVal)
	else:
		cmds.warning('No existe el control %s o existen dos iguales o necesita un namespace.' % (ctr))

# Definimos una interfas grafica para el usuario
def botonesUI(directorios='', nameSpace='',sizeButtons=100,parents='',controlAttributos='L_EYE_PUPILA_CNT'):
    #Contengo todo en un solo scroll grande
    scroll=cmds.scrollLayout( 'scrollLayout', childResizable=True,parent=parents)
    #Creo una fila con 3 columnos grandes
    rowGeneral=cmds.rowLayout( numberOfColumns=3, columnWidth3=(sizeButtons*5, sizeButtons*6, sizeButtons*5), adjustableColumn3=1, columnAlign=(1, 'right'), columnAttach=[(1, 'left', 0), (2, 'both', 0), (3, 'left', 0)] )
    colRight=cmds.columnLayout(adjustableColumn=True,parent=rowGeneral)
    colMid=cmds.columnLayout(adjustableColumn=True,parent=rowGeneral)
    colLeft=cmds.columnLayout(adjustableColumn=True,parent=rowGeneral)

    # creo los botones recoriendo el diccionario que creamos
    for key in directorios:

        #Ordeno los frames dependiendo de la letra que contengan las carpetas
        sideFace=key.split('\\')[-1]
        if 'l_' in sideFace:
            sideParent=colLeft
        elif 'r_' in sideFace:
            sideParent=colRight
        else:
            sideParent=colMid


        # Creo una columna para los botones
        cl1=cmds.columnLayout(adjustableColumn=True,parent=sideParent)

        frameIn=cmds.frameLayout(label=sideFace,labelAlign='center',collapsable=True,parent=cl1)
        cl2=cmds.columnLayout( bgc=[0.4,0.4,0.6],cal='center',columnOffset=['both', 0],parent=frameIn)
        cmds.text(label='DisplayLayer',align='center',parent=cl2)
        cmds.checkBox(label='sideFace',parent=cl2)

        cmds.frameLayout(label='Expresiones',labelAlign='center',collapsable=True)
        cmds.rowColumnLayout( numberOfRows=4,bgc=[0.2,0.2,0.2])
        #Para diferenciar las carpeas o frames le pongo diferentes colores
        r,g,b=random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)
        #creo por cada file un boton
        for ctrl in directorios[key]:
            #valFrame=[s.zfill(2) for s in re.findall(r'\b\d+\b', img)]
            val=[int(s) for s in re.findall(r'\b\d+\b', ctrl)][0]

            # Solo si existe algo escrito en la variable nameSpace y si es asi
            # le agrego el nameSpace al control.
            if nameSpace is not '':
                ctrl = nameSpace + ctrl
            # Agrego el boton y la funcion, con el nombre del value del
            # diccionario
            cmds.symbolButton(ctrl, image=key +'\\'+ctrl, width=sizeButtons, height=sizeButtons, backgroundColor=[r,g,b] ,
                              annotation='( SHIFT+CLICK suma seleccion. )', command=partial(getFrame, val, sideFace, controlAttributos))


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
    botonesUI( directorios, nameSpace,sizeButtons,WorkspaceName,)

# llamo a la funcion la cual ejecuta todo el resto.
UI(name, directorios, nameSpace,60,cabezaControl)
