import maya.cmds as cmds
#Variables para las dinamicas
global datos
datos={}
#Selecciona los controles del snail
def selSnail(char='SNAIL'):
    cnts=cmds.ls('*_'+char+'_*_CNT*',type='transform')
    print 'Seleccionastes todos los cnts de ' + char
    cmds.select(cnts)

#Resetea las transformaciones de la seleccion
def reset_TRS(cnts=[cmds.ls(sl=1,type='transform')]):
    for axi in ['x','y','z']:
    	[cmds.setAttr(o+'.t'+axi,0) for o in cnts]
    	[cmds.setAttr(o+'.r'+axi,0) for o in cnts]
    	for o in cnts:
            try:
                cmds.setAttr(o+'.s'+axi,1)
            except:
                pass

#Resetea todas las dinamicas si tenes algo seleccionado solo resetea eso
def resDinamics(char='SNAIL'):
    global datos
    cnts=cmds.ls('*_'+char+'_*_CNT*',type='transform')
    sel=cmds.ls(sl=1)
    if sel:
        for cnt in sel:
            datos[cnt]=cmds.listAttr(cnt,keyable=True)
    else:
        for cnt in cnts:
            datos[cnt]=cmds.listAttr(cnt,keyable=True)

    for obj,attrs in datos.items():
        defValue=[]
        for attr in attrs:
            defValue.append([attr,cmds.attributeQuery(attr,node=obj,listDefault=True)[0]])
        datos[obj]=defValue

    for obj,attrs in datos.items():
        for attr in attrs:
            try:
                cmds.setAttr(str(obj)+'.'+str(attr[0]),attr[1])
            except:
                pass
                
#Key en las transformaciones en la capa de animacion que estas parado
def keySel(cnts=cmds.ls(sl=1,type='transform')):
    cTime=cmds.currentTime(query=True)
    for axi in ['x','y','z']:
        [cmds.setKeyframe(o, attribute='t'+axi, t=[cTime] ) for o in cnts]
        [cmds.setKeyframe(o, attribute='r'+axi, t=[cTime] ) for o in cnts]
        [cmds.setKeyframe(o, attribute='s'+axi, t=[cTime] ) for o in cnts]

#Key solo en las propiedades que no tiene transformacion en este caso las dinamicas
def keyDinamicas(cnts=cmds.ls(sl=1,type='transform')):
    missAttr=['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility']
    global datos
    cTime=cmds.currentTime(query=True)
    for cnt in cnts:
        datos[cnt]=cmds.listAttr(cnt,keyable=True)
    for obj,attrs in datos.items():
        for attr in attrs:
            if not attr in missAttr:
                cmds.setKeyframe(str(obj), attribute=str(attr), t=[cTime] )
