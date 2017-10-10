from os import listdir
from os.path import isfile, join
mypath='O:\EMPRESAS\RIG_FACE2D\ScriptingGuideRig\Maps'
os.listdir(mypath)
onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
nameSpace=''
from os import walk
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(dirnames)
    break
len(onlyfiles)
#Defino la funcion para seleccionar los objetos por nombre
def setFrame(attr='',control='C_head_01_CTRL',*args):
    #Con esta funcion pregunto si existe el control que le estoy pasando por argumento
    if cmds.objExists(ctr):
        #Devuelve el evento que preciono
        mods = cmds.getModifiers()
        #pregunto si se preciono y es shift y agrego a la seleccion
        if (mods & 1) > 0:
            cmds.select(ctr,add=True)
        #de lo contrario solo selecciono
        else:
            cmds.select(ctr)
    else:
        cmds.warning('No existe el control %s o existen dos iguales o necesita un namespace.'%(ctr))

#Definimos una interfas grafica para el usuario
def botonesUI(imagenes='',nameSpace=''):
    #Creo una columna para los botones
    cmds.columnLayout(adjustableColumn = True,columnOffset=['both',5])
    #creo los botones recoriendo el diccionario que creamos
    for key in imagenes:
        #Colores alateorios para distingir mejor los controles
        r,g,b=random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)
        #Agrego el titulo desde el key del diccionario
        cmds.text( label='>'+key+'<', align='left',font='boldLabelFont',highlightColor=[r,g,b])
        for ctrl in controles[key]:
            #Solo si existe algo escrito en la variable nameSpace y si es asi le agrego el nameSpace al control.
            if nameSpace is not '':
                ctrl= nameSpace + ctrl
            #Agrego el boton y la funcion, con el nombre del value del diccionario
            cmds.symbolButton( label=ctrl,img=mypath+key,width=50, height=50,annotation='( SHIFT+CLICK suma seleccion. )', command=partial(seleccion,ctrl))

def UI(charName,controles={},nameSpace=''):
    #variable que contiene el nombre de dockControl
    WorkspaceName='PICKER_UI->'+charName
    #Pregunto si existe la ventana workspaceControl y si existe la borro antes de crearla nuevamente.
    if cmds.workspaceControl(WorkspaceName,exists=True):
        cmds.deleteUI(WorkspaceName)
        print 'Se borro',WorkspaceName
    else:
        #ejecuto funcion de interfas y la guardo en un dock
        cmds.workspaceControl(WorkspaceName,initialHeight=500, floating=False, retain=False, uiScript="botonesUI(onlyfiles,nameSpace)",dtm=('right', 1));
UI(name,controles,nameSpace)#llamo a la funcion la cual ejecuta todo el resto.
