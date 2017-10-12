import maya.cmds as cmds
from functools import partial
import random
import sys
path=r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\UTIL'
path2=r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\PICKER_2DFACES'
if not path in sys.path:
	sys.path.append(path)
	sys.path.append(path2)
try:
    import UTILITYES
    reload(UTILITYES)
except (RuntimeError, TypeError, NameError,IOError):
    print 'NO SE PUDO IMPORTAR EL MODULO'

name='MILO'
nameSpace=''

mypath = 'O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES'
directorios = UTILITYES.dirs_files_dic(mypath, 'jpg', 'proxy')
print directorios

def getFrame(val=000, attr='', ctr='C_head_01_CTRL'):
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
def botonesUI(directorios='', nameSpace=''):
    # creo los botones recoriendo el diccionario que creamos
    for key in directorios:
        # Creo una columna para los botones
        cmds.columnLayout()
        frame=cmds.frameLayout(label=key.split('\\')[-1])
        cmds.gridLayout(numberOfColumns=2,cellWidthHeight=[100,100])

        for ctrl in directorios[key]:
            val=000
            # Solo si existe algo escrito en la variable nameSpace y si es asi
            # le agrego el nameSpace al control.
            if nameSpace is not '':
                ctrl = nameSpace + ctrl
            # Agrego el boton y la funcion, con el nombre del value del
            # diccionario
            cmds.symbolButton(ctrl, image=key +'\\'+ctrl, width=100, height=100,
                              annotation='( SHIFT+CLICK suma seleccion. )', command=partial(getFrame, val, key, ctrl))


def UI(charName, directorios={}, nameSpace=''):
    # variable que contiene el nombre de dockControl
    WorkspaceName = '2DPICKER_UI->' + charName
    # Pregunto si existe la ventana workspaceControl y si existe la borro
    # antes de crearla nuevamente.
    if cmds.workspaceControl(WorkspaceName, exists=True):
        cmds.deleteUI(WorkspaceName)
        print 'Se borro', WorkspaceName
    else:
        # ejecuto funcion de interfas y la guardo en un dock
        cmds.workspaceControl(WorkspaceName, initialHeight=500, floating=False,
                              retain=False, uiScript="botonesUI(directorios,nameSpace)", dtm=('right', 1))
# llamo a la funcion la cual ejecuta todo el resto.
UI(name, directorios, nameSpace)
