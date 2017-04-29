# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
'''
#Lista objetos para array
cnts=cmds.ls(sl=True)
list=[]
for o in cnts:
    obj=str(o)
    if ':' in o:
        o=str(o.split(':')[-1])
        print "'"+o+"',"
    else:
        print "'"+o+"',"
    list.append(obj)
'''
nameCamera='HELMETGIRL_FACE_UI_CAM'
nameSpaceGeo='HELMETGIRL_GEO_'
nameSpaceRig='HELMETGIRL_RIG_'

CHAR1_GEO=['C_HELMETGIRL_A_SKIRT',
'C_HELMETGIRL_A_HELMET',
'C_HELMETGIRL_A_BELT',
'C_HELMETGIRL_A_BOOTS',
'C_HELMETGIRL_A_HANDS',
'C_HELMETGIRL_A_SPHERES',
'C_HELMETGIRL_A_HEAD',
'C_HELMETGIRL_A_BODY',
'C_HELMETGIRL_A_HAIR',]

BOCA=['C_HELMETGIRL_A_GUMUP',
'C_HELMETGIRL_A_GUMDN',
'C_HELMETGIRL_A_TONGUE',
'C_HELMETGIRL_A_TEETHUP',
'C_HELMETGIRL_A_TEETH',]

CHAR2_GEO=['C_HELMETGIRL_B_BUNNYH',
'C_HELMETGIRL_B_HAT',
'C_HELMETGIRL_B_BODY',
'C_HELMETGIRL_B_HEAD',
'C_HELMETGIRL_B_SPHERES',
'C_HELMETGIRL_B_HANDS',
'C_HELMETGIRL_B_BOOTS',
'C_HELMETGIRL_B_BELT',
'C_HELMETGIRL_B_SKIRT',]

CHAR3_GEO=[
'C_HELMETGIRL_A_TEETHUP',
'C_HELMETGIRL_A_GUMUP',
'C_HELMETGIRL_A_GUMDN',
'C_HELMETGIRL_A_TONGUE',
'C_HELMETGIRL_A_TEETH',
'C_HELMETGIRL_C_NECK',
'L_HELMETGIRL_C_EARRING',
'R_HELMETGIRL_C_EARRING',
'C_HELMETGIRL_C_HAIR',
'C_HELMETGIRL_C_BODY',
'C_HELMETGIRL_C_HEAD',
'C_HELMETGIRL_C_SPHERES',
'C_HELMETGIRL_C_HANDS',
'C_HELMETGIRL_C_BOOTS',
'C_HELMETGIRL_C_BELT',
'C_HELMETGIRL_C_SKIRT',]

CHAR1_CNT=[]

CHAR2_CNT=['L_HELMETGIRL_HEADBUNNY0_CNT',
'L_HELMETGIRL_HEADBUNNY1_CNT',
'L_HELMETGIRL_HEADBUNNY2_CNT',
'L_HELMETGIRL_HEADBUNNY3_CNT',
'L_HELMETGIRL_HEADBUNNY4_CNT',
'L_HELMETGIRL_HEADBUNNY5_CNT',
'C_HELMETGIRL_B_HAT_CNT',
'R_HELMETGIRL_HEADBUNNY0_CNT',
'R_HELMETGIRL_HEADBUNNY1_CNT',
'R_HELMETGIRL_HEADBUNNY2_CNT',
'R_HELMETGIRL_HEADBUNNY3_CNT',
'R_HELMETGIRL_HEADBUNNY4_CNT',
'R_HELMETGIRL_HEADBUNNY5_CNT',]

CHAR3_CNT=['L_HELMETGIRL_EARRING0_CNT',
'L_HELMETGIRL_EARRING1_CNT',
'L_HELMETGIRL_EARRING2_CNT',
'L_HELMETGIRL_EARRING3_CNT',
'L_HELMETGIRL_EARRING4_CNT',
'R_HELMETGIRL_EARRING0_CNT',
'R_HELMETGIRL_EARRING1_CNT',
'R_HELMETGIRL_EARRING2_CNT',
'R_HELMETGIRL_EARRING3_CNT',
'R_HELMETGIRL_EARRING4_CNT',]



def agregarnameSpace(lista=[],nameSpace=''):
    newList=[]
    for obj in lista:
        if not nameSpace=='':
            if nameSpace in obj:
                raise cmds.warning('Ya existe el namespace '+ nameSpace + ' en ' + obj)
                newList.append(obj)
            else:
                obj=nameSpace+':'+str(obj)
                newList.append(obj)
        else:
            newList.append(obj)
    return newList



def comprobarObj(lista=[]):
    #lista=bearGuy
    for obj in lista:
        if not cmds.ls(obj):
            cmds.error('No se encontro el '+obj+', verificar y volver a probar.')

def onOffVisibility(listaAprender=[], listaApagar=[],prender=False):
    if not prender:
        #para la lista principal hacer esto
        for obj in listaAprender:
            cmds.setAttr(obj+'.v',1)
        #para las demas listas hacer esto
        for obj in listaApagar:
            if obj not in listaAprender:
                cmds.setAttr(obj+'.v',0)
    else:
        for obj in listaAprender:
            cmds.setAttr(obj+'.v', 1)




#Agrega el namespace si lo necesita
CHAR1_GEO=agregarnameSpace(CHAR1_GEO,nameSpaceRig+':'+nameSpaceGeo)
CHAR1_CNT=agregarnameSpace(CHAR1_CNT,nameSpaceRig)
comprobarObj(CHAR1_GEO)
comprobarObj(CHAR1_CNT)

CHAR2_GEO=agregarnameSpace(CHAR2_GEO,nameSpaceRig+':'+nameSpaceGeo)
CHAR2_CNT=agregarnameSpace(CHAR2_CNT,nameSpaceRig)
comprobarObj(CHAR2_GEO)
comprobarObj(CHAR2_CNT)

CHAR3_GEO=agregarnameSpace(CHAR3_GEO,nameSpaceRig+':'+nameSpaceGeo)
CHAR3_CNT=agregarnameSpace(CHAR3_CNT,nameSpaceRig)
comprobarObj(CHAR3_GEO)
comprobarObj(CHAR3_CNT)

#
BOCA=agregarnameSpace(BOCA,nameSpaceGeo)
BOCA=agregarnameSpace(BOCA,nameSpaceRig)
comprobarObj(BOCA)



#Prende 1
def char1(*args):
    onOffVisibility(CHAR1_GEO,CHAR2_GEO)
    onOffVisibility(CHAR1_GEO,CHAR3_GEO)
    onOffVisibility(BOCA,prender=True)
    onOffVisibility(CHAR1_CNT,CHAR2_CNT)
    onOffVisibility(CHAR1_CNT,CHAR3_CNT)

#Prende 2
def char2(*args):
    onOffVisibility(CHAR2_GEO,CHAR1_GEO)
    onOffVisibility(CHAR2_GEO,CHAR3_GEO)
    onOffVisibility(CHAR2_CNT,CHAR1_CNT)
    onOffVisibility(CHAR2_CNT,CHAR3_CNT)
#Prende 3
def char3(*args):
    onOffVisibility(CHAR3_GEO,CHAR1_GEO)
    onOffVisibility(CHAR3_GEO,CHAR2_GEO)
    onOffVisibility(CHAR3_CNT,CHAR1_CNT)
    onOffVisibility(CHAR3_CNT,CHAR2_CNT)

def dinamicasOnOffMexico(onOff=False,nameSpace=''):
    list=cmds.ls(nameSpace+':*_BEARDGUY_MEXICAN_HATBALL_*HSYM')
    for o in list:
        o=cmds.listRelatives(o)[0]
        if onOff==False:
            mel.eval("setAttr "+str(o)+".simulationMethod 0")
            print 'Dinamicas mexicanas OFF'
            return False
        if onOff==True:
            mel.eval("setAttr "+str(o)+".simulationMethod 3")
            print 'Dinamicas mexicanas ON'
            return True

def win(namespace='',cameraName=''):
    winDate='facialUi'+namespace
    if cmds.window(winDate, ex=True):
        cmds.deleteUI(winDate)
    win = cmds.window(winDate, title='FACIAL UI - '+ namespace, widthHeight=[300,700] )
    FacialGUI = cmds.formLayout()
    panel=cmds.modelPanel()

    FacialPanel=cmds.modelPanel(panel,edit=True,camera=namespace + ':' + cameraName)
    cmds.formLayout(FacialGUI, e=True,
                    attachForm=[
                        (FacialPanel, "top", 0),
                        (FacialPanel, "left", 0),
                        (FacialPanel, "bottom", 0),
                        (FacialPanel, "right", 0)])

    column = cmds.rowLayout(numberOfColumns=4)
    cmds.symbolButton("char1", command=char1,image = "helmetgirl_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    cmds.symbolButton("char2", command=char2,image = "helmetgirl_a_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    cmds.symbolButton("char3", command=char3,image = "helmetgirl_b_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    column = cmds.rowLayout(numberOfColumns=1)
    #cmds.checkBox("dinamicCheckBox", label = "Dinamic_Mexican_Hat", onCommand = 'dinamicasOnOffMexico(True,nameSpaceRig)', offCommand = "dinamicasOnOffMexico(False,nameSpaceRig)", value = 0)

    cmds.showWindow(win)

win(nameSpaceRig,nameCamera)
