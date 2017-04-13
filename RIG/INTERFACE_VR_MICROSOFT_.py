import maya.cmds as cmds


bearGuy=['BEARDGUY_BEARD_MSH',
             'BEARDGUY_HEAD_MSH',
             'BEARDGUY_HAT_MSH',
             'BEARDGUY_BEARD_RING_MSH',
             'BEARDGUY_SHOULDER_UP_MSH',
             'BEARDGUY_CAPE_UP_MSH',
             'L_BEARDGUY_HAT_ZTR']

samurai=['BEARDSAMURAI_HELMET_MSH',
             'BEARDSAMURAI_HEAD_MSH',
             'BEARDSAMURAI_NECK_MSH',
             'BEARDSAMURAI_MASK_MSH',
             'BEARDSAMURAI_LACE_MSH',
             'BEARDSAMURAI_SHOULDER_PADS_MSH',
             'BEARDSAMURAI_SAMURAI_SKIRT_MSH',
             'BEARDGUY_SHOULDER_UP_MSH']

mexican=['BEARDGUY_MEXICAN_HAT_MSH',
             'BEARDGUY_PONCHO_MSH',
             'BEARDGUY_HEAD_MSH',
             'BEARDGUY_BEARD_MSH',
             'BEARDGUY_SHOULDER_UP_MSH',
             'BEARDGUY_BEARD_RING_MSH']



def agregarnameSpace(lista=[],nameSpace=''):
    newList=[]
    for obj in lista:
        if cmds.namespace()
        if nameSpace in obj:
            cmds.warning('Ya existe el namespace '+ nameSpace)
        else:
            obj=nameSpace+':'+str(obj)
        newList.append(obj)
    return newList

def comprobarObj(lista=[]):
    #lista=bearGuy
    for obj in lista:
        if cmds.ls(obj):
            print obj + ' existe.'
        else:
            cmds.error('No se encontro el '+obj+', verificar y volver a probar.')


def onOffVisibility(listaAprender=[], listaApagar=[] ):
    #para la lista principal hacer esto
    for obj in listaAprender:
        cmds.setAttr(obj+'.v',1)
    #para las demas listas hacer esto
    for obj in listaApagar:
        if obj not in listaAprender:
            cmds.setAttr(obj+'.v',0)

#Agrega el namespace
bearGuy=agregarnameSpace(bearGuy,'BEARDGUY_GEO_')
mexican=agregarnameSpace(mexican,'BEARDGUY_GEO_')
samurai=agregarnameSpace(samurai,'BEARDGUY_GEO_')
#Check si existen
comprobarObj(bearGuy)
comprobarObj(mexican)
comprobarObj(samurai)

#Prende bearGuy
def bearGuyBtn():
    onOffVisibility(bearGuy,samurai)
    onOffVisibility(bearGuy,mexican)
#Prende samurai
def samuraiBtn():
    onOffVisibility(samurai,bearGuy)
    onOffVisibility(samurai,mexican)
#Prende bearGuy
def mexicanBtn():
    onOffVisibility(mexican,bearGuy)
    onOffVisibility(mexican,samurai)

def win():

    if cmds.window('facialUi', ex=True):
        cmds.deleteUI('facialUi')
    win = cmds.window('facialUi', title='FACIAL UI - BEARDGUY',widthHeight=[320,600])
    cmds.paneLayout()
    mo=cmds.modelPanel(camera='FACE_UI_CAM')
    cmds.modelPanel(mo,edit=True,menuBarVisible=False)
    currState = cmds.grid( toggle=True, q=True )
    cmds.grid('FACE_UI_CAM', toggle=(currState==0) )
    cmds.rowLayout(numberOfColumns=3)
    cmds.symbolButton("bearGuyBtn", command='bearGuyBtn()',image = r"F:\EMPRESAS\2VEINTE\MICROSOFT_VR\ASSETS\CHARS\02_BEARDGUY\beardguy_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2],)
    cmds.symbolButton("samuraiBtn", command='samuraiBtn()',image = r"F:\EMPRESAS\2VEINTE\MICROSOFT_VR\ASSETS\CHARS\02_BEARDGUY\samurai_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    cmds.symbolButton("mexicanBtn", command='mexicanBtn()',image = r"F:\EMPRESAS\2VEINTE\MICROSOFT_VR\ASSETS\CHARS\02_BEARDGUY\mexican_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    cmds.showWindow(win)

win()
