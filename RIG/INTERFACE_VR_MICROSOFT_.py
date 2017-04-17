# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
nameCamera='BEARDGUY_RIG_:BEARDGUY_FACE_UI_CAM'
nameSpaceGeo='BEARDGUY_GEO_'
nameSpaceRig='BEARDGUY_RIG_'
'''
import maya.cmds
import sys
path=r'F:\Repositores\GitHub\ES_SCRIPTS\RIG'
if not path in sys.path:
	sys.path.append(path)
import INTERFACE_VR_MICROSOFT_
reload(INTERFACE_VR_MICROSOFT_)
import INTERFACE_VR_MICROSOFT_
INTERFACE_VR_MICROSOFT_.win()
'''

CHAR1_GEO=['BEARDGUY_BEARD_MSH',
             'BEARDGUY_HEAD_MSH',
             'BEARDGUY_HAT_MSH',
             'BEARDGUY_BEARD_RING_MSH',
             'BEARDGUY_SHOULDER_UP_MSH',
             'BEARDGUY_CAPE_UP_MSH','BEARDGUY_L_EYE_MSH',
             'BEARDGUY_R_EYE_MSH', 'BEARDGUY_EYEBROWS_MSH',
             'C_TEETH_UP_MSH','C_TEETH_DN_MESH', 'C_GUM_UP_MSH', 'C_GUM_DN_MSH', 'C_TONGUE_MSH']

CHAR1_CNT=[ 'C_BEARDGUY_HAT_CNT',
             'L_BEARDGUY_SHOULDERUP_CNT',
             'R_BEARDGUY_SHOULDERUP_CNT',
             'C_BEARDGUY_CAP0_CNT','C_BEARDGUY_CAP1_CNT',
             'C_BEARDGUY_CAP2_CNT','C_BEARDGUY_CAP3_CNT',
             'C_BEARDGUY_CAP4_CNT','C_BEARDGUY_CAP5_CNT',
             'C_BEARDGUY_CAP6_CNT','C_BEARDGUY_CAP7_CNT',
             'C_BEARDGUY_CAP8_CNT',
             'L_HEAD_JAW0_CNT','C_BEARDGUY_BEARD0_CNT',
             'C_BEARDGUY_BEARD1_CNT','C_BEARDGUY_BEARD2_CNT',
             'C_BEARDGUY_BEARD3_CNT']

CHAR2_GEO=['BEARDSAMURAI_HELMET_MSH',
             'BEARDSAMURAI_HEAD_MSH',
             'BEARDSAMURAI_NECK_MSH',
             'BEARDSAMURAI_MASK_MSH',
             'BEARDSAMURAI_LACE_MSH',
             'BEARDSAMURAI_SHOULDER_PADS_MSH',
             'BEARDSAMURAI_SAMURAI_SKIRT_MSH',
             'BEARDGUY_SHOULDER_UP_MSH']

CHAR2_CNT=['L_BEARDGUY_SHOULDERUP_CNT', 'R_BEARDGUY_SHOULDERUP_CNT',
            'L_BEARDSAMURAI_SAMURAI_SKIRT1_CNT', 'L_BEARDSAMURAI_SAMURAI_SKIRT0_CNT', 'R_BEARDSAMURAI_SAMURAI_SKIRT1_CNT',
            'R_BEARDSAMURAI_SAMURAI_SKIRT0_CNT', 'C_SAMURAYGUY_LACE0_CNT', 'C_SAMURAYGUY_LACE1_CNT', 'C_SAMURAYGUY_LACE2_CNT', 'C_SAMURAYGUY_LACE3_CNT']

CHAR3_GEO=['BEARDGUY_MEXICAN_HAT_MSH',
             'BEARDGUY_PONCHO_MSH',
             'BEARDGUY_HEAD_MSH',
             'BEARDGUY_BEARD_MSH',
             'BEARDGUY_SHOULDER_UP_MSH','BEARDGUY_L_EYE_MSH',
             'BEARDGUY_R_EYE_MSH', 'BEARDGUY_EYEBROWS_MSH',
             'BEARDGUY_BEARD_RING_MSH','C_TEETH_UP_MSH','C_TEETH_DN_MESH', 'C_GUM_UP_MSH', 'C_GUM_DN_MSH', 'C_TONGUE_MSH']

CHAR3_CNT=['L_BEARDGUY_MEXICAN_HATBALL_A_CNT','L_BEARDGUY_MEXICAN_HATBALL_B_CNT',
             'L_BEARDGUY_MEXICAN_HATBALL_C_CNT','L_BEARDGUY_MEXICAN_HATBALL_D_CNT',
             'L_BEARDGUY_MEXICAN_HATBALL_E_CNT','L_BEARDGUY_MEXICAN_HATBALL_F_CNT',
             'R_BEARDGUY_MEXICAN_HATBALL_A_CNT','R_BEARDGUY_MEXICAN_HATBALL_B_CNT',
             'R_BEARDGUY_MEXICAN_HATBALL_C_CNT','R_BEARDGUY_MEXICAN_HATBALL_D_CNT',
             'R_BEARDGUY_MEXICAN_HATBALL_E_CNT','R_BEARDGUY_MEXICAN_HATBALL_F_CNT',
             'L_HEAD_JAW0_CNT', 'C_BEARDGUY_BEARD0_CNT', 'C_BEARDGUY_BEARD1_CNT', 'C_BEARDGUY_BEARD2_CNT',
             'C_BEARDGUY_BEARD3_CNT','C_BEARDGUY_HAT_CNT','L_BEARDGUY_SHOULDERUP_CNT',
             'R_BEARDGUY_SHOULDERUP_CNT']



def agregarnameSpace(lista=[],nameSpace=''):
    newList=[]
    for obj in lista:
        if nameSpace in obj:
            raise cmds.warning('Ya existe el namespace '+ nameSpace + ' en ' + obj)
            newList.append(obj)
        else:
            obj=nameSpace+':'+str(obj)
            newList.append(obj)
    return newList



def comprobarObj(lista=[]):
    #lista=bearGuy
    for obj in lista:
        if not cmds.ls(obj):
            cmds.error('No se encontro el '+obj+', verificar y volver a probar.')

def onOffVisibility(listaAprender=[], listaApagar=[] ):
    #para la lista principal hacer esto
    for obj in listaAprender:
        cmds.setAttr(obj+'.v',1)
    #para las demas listas hacer esto
    for obj in listaApagar:
        if obj not in listaAprender:
            cmds.setAttr(obj+'.v',0)



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

#Prende bearGuy
def char1(*args):
    onOffVisibility(CHAR1_GEO,CHAR2_GEO)
    onOffVisibility(CHAR1_GEO,CHAR3_GEO)
    onOffVisibility(CHAR1_CNT,CHAR2_CNT)
    onOffVisibility(CHAR1_CNT,CHAR3_CNT)

#Prende samurai
def char2(*args):
    onOffVisibility(CHAR2_GEO,CHAR1_GEO)
    onOffVisibility(CHAR2_GEO,CHAR3_GEO)
    onOffVisibility(CHAR2_CNT,CHAR1_CNT)
    onOffVisibility(CHAR2_CNT,CHAR3_CNT)
#Prende mexican
def char3(*args):
    onOffVisibility(CHAR3_GEO,CHAR1_GEO)
    onOffVisibility(CHAR3_GEO,CHAR2_GEO)
    onOffVisibility(CHAR3_CNT,CHAR1_CNT)
    onOffVisibility(CHAR3_CNT,CHAR2_CNT)

def dinamicasOnOffMexico(onOff=False):
    list=cmds.ls(nameSpaceRig+':*_BEARDGUY_MEXICAN_HATBALL_*HSYMShape')
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
def dinOnOff():
    global onOff
    onOff=dinamicasOnOffMexico((onOff==False))

def win(namespace='',camera=''):

    if cmds.window('facialUi', ex=True):
        cmds.deleteUI('facialUi')
    win = cmds.window('facialUi', title='FACIAL UI - '+ camera, widthHeight=[400,700] )
    FacialGUI = cmds.formLayout()
    panel=cmds.modelPanel()
    FacialPanel=cmds.modelPanel(panel,edit=True,camera= camera)
    cmds.formLayout(FacialGUI, e=True,
                    attachForm=[
                        (FacialPanel, "top", 0),
                        (FacialPanel, "left", 0),
                        (FacialPanel, "bottom", 0),
                        (FacialPanel, "right", 0)])

    column = cmds.rowLayout(numberOfColumns=4)
    cmds.symbolButton("char1", command=char1,image = "beardguy_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    cmds.symbolButton("char2", command=char2,image = "samurai_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    cmds.symbolButton("char3", command=char3,image = "mexican_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    column = cmds.rowLayout(numberOfColumns=1)
    cmds.checkBox("dinamicCheckBox", label = "Dinamic_Mexican_Hat", onCommand = 'dinamicasOnOffMexico(True)', offCommand = "dinamicasOnOffMexico(False)", value = 0)

    cmds.showWindow(win)

win(nameSpaceRig,nameCamera)
