import maya.cmds as cmds #libreria de comandos de maya
from functools import partial #libreria para usar funcion partial la cual nos permitira reutilizar argumentos
import random #funciones para aleatoridad
#Este es el nombre que le daremos a nuestra interfas el cual tiene que ser diferente por cada personaje
name='GABO_2'
#Aqui se agrega el nameSpace de nuestra referencia para que empaten bien los controles de nuestro personaje
nameSpace='GABO_PRIMO:'
#lista de controles
controles={'OJOS':['C_CABEZA_OJOS_CNT','R_CABEZA_OJO_CNT','L_CABEZA_OJO_CNT'],
           'PATO':['C_PATO_MASTER_CNT'],
           'LENTES':['C_PATO_MASTER_CNT'],
           'BOTELLA':['C_BOTELLA_MASTER_CNT'],
           'SOMBRERO':['C_SOMBRERO_MASTER_CNT','L_SOMBRERO_SOMBRERO_CNT','R_SOMBRERO_SOMBRERO_CNT','C_SOMBRERO_SOMBRERO_01_CNT','C_SOMBRERO_SOMBRERO_02_CNT','C_SOMBRERO_SOMBRERO_03_CNT'],
           'CAMARA':['C_CAMARA_ROOT_CNT']}
#Defino la funcion para seleccionar los objetos por nombre
def seleccion(ctr='',*args):
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

#Esta funcion se las deje para que se animen a agregarla a su picker si se dan la mañana,
#podran crear el picker de manera que tambien les resete los valores de los controles del boton.
def resetTRF(ctr='',*args):
    atributos = {'sx':1, 'sy':1, 'sz':1, 'rx':0, 'ry':0, 'rz':0, 'tx':0, 'ty':0, 'tz':0}
    for attr in atributos:
        try:
            mc.setAttr('%s.%s'%(crt, attr), atributos[attr])
        except:
            pass

#Definimos una interfas grafica para el usuario
def botonesUI(controles='',nameSpace=''):
    #Creo una columna para los botones
    cmds.columnLayout(adjustableColumn = True,columnOffset=['both',5])
    #creo los botones recoriendo el diccionario que creamos
    for key in controles.keys():
        #Colores alateorios para distingir mejor los controles
        r,g,b=random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)
        #Agrego el titulo desde el key del diccionario
        cmds.text( label='>'+key+'<', align='left',font='boldLabelFont',highlightColor=[r,g,b])
        for ctrl in controles[key]:
            #Solo si existe algo escrito en la variable nameSpace y si es asi le agrego el nameSpace al control.
            if nameSpace is not '':
                ctrl= nameSpace + ctrl
            #Agrego el boton y la funcion, con el nombre del value del diccionario
            cmds.button( label=ctrl,bgc=[r,g,b],height=30,annotation='( SHIFT+CLICK suma seleccion. )', command=partial(seleccion,ctrl))

def UI(charName,controles={},nameSpace=''):
    #variable que contiene el nombre de dockControl
    WorkspaceName='PICKER_UI->'+charName
    #Pregunto si existe la ventana workspaceControl y si existe la borro antes de crearla nuevamente.
    if cmds.workspaceControl(WorkspaceName,exists=True):
        cmds.deleteUI(WorkspaceName)
        print 'Se borro',WorkspaceName
    else:
        #ejecuto funcion de interfas y la guardo en un dock
        cmds.workspaceControl(WorkspaceName,initialHeight=500, floating=False, retain=False, uiScript="botonesUI(controles,nameSpace)",dtm=('right', 1));
UI(name,controles,nameSpace)#llamo a la funcion la cual ejecuta todo el resto.
