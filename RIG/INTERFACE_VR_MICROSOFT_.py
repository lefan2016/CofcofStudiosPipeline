# -*- coding: utf-8 -*-
import maya.cmds as cmds
nameCharacter='BEARDGUY_GEO_'
bearGuy=['BEARDGUY_BEARD_MSH',
             'BEARDGUY_HEAD_MSH',
             'BEARDGUY_HAT_MSH',
             'BEARDGUY_BEARD_RING_MSH',
             'BEARDGUY_SHOULDER_UP_MSH',
             'BEARDGUY_CAPE_UP_MSH','BEARDGUY_L_EYE_MSH',
             'BEARDGUY_R_EYE_MSH', 'BEARDGUY_EYEBROWS_MSH',
             'C_TEETH_UP_MSH','C_TEETH_DN_MESH', 'C_GUM_UP_MSH', 'C_GUM_DN_MSH', 'C_TONGUE_MSH']

bearGuyCNT=[ 'C_BEARDGUY_HAT_CNT',
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

samurai=['BEARDSAMURAI_HELMET_MSH',
             'BEARDSAMURAI_HEAD_MSH',
             'BEARDSAMURAI_NECK_MSH',
             'BEARDSAMURAI_MASK_MSH',
             'BEARDSAMURAI_LACE_MSH',
             'BEARDSAMURAI_SHOULDER_PADS_MSH',
             'BEARDSAMURAI_SAMURAI_SKIRT_MSH',
             'BEARDGUY_SHOULDER_UP_MSH']

samuraiCNTS=['L_BEARDGUY_SHOULDERUP_CNT', 'R_BEARDGUY_SHOULDERUP_CNT',
            'L_BEARDSAMURAI_SAMURAI_SKIRT1_CNT', 'L_BEARDSAMURAI_SAMURAI_SKIRT0_CNT', 'R_BEARDSAMURAI_SAMURAI_SKIRT1_CNT',
            'R_BEARDSAMURAI_SAMURAI_SKIRT0_CNT', 'C_SAMURAYGUY_LACE0_CNT', 'C_SAMURAYGUY_LACE1_CNT', 'C_SAMURAYGUY_LACE2_CNT', 'C_SAMURAYGUY_LACE3_CNT']

mexican=['BEARDGUY_MEXICAN_HAT_MSH',
             'BEARDGUY_PONCHO_MSH',
             'BEARDGUY_HEAD_MSH',
             'BEARDGUY_BEARD_MSH',
             'BEARDGUY_SHOULDER_UP_MSH','BEARDGUY_L_EYE_MSH',
             'BEARDGUY_R_EYE_MSH', 'BEARDGUY_EYEBROWS_MSH',
             'BEARDGUY_BEARD_RING_MSH','C_TEETH_UP_MSH','C_TEETH_DN_MESH', 'C_GUM_UP_MSH', 'C_GUM_DN_MSH', 'C_TONGUE_MSH']

mexicanCNT=['L_BEARDGUY_MEXICAN_HATBALL_A_CNT','L_BEARDGUY_MEXICAN_HATBALL_B_CNT',
             'L_BEARDGUY_MEXICAN_HATBALL_C_CNT','L_BEARDGUY_MEXICAN_HATBALL_D_CNT',
             'L_BEARDGUY_MEXICAN_HATBALL_E_CNT','L_BEARDGUY_MEXICAN_HATBALL_F_CNT',
             'R_BEARDGUY_MEXICAN_HATBALL_A_CNT','R_BEARDGUY_MEXICAN_HATBALL_B_CNT',
             'R_BEARDGUY_MEXICAN_HATBALL_C_CNT','R_BEARDGUY_MEXICAN_HATBALL_D_CNT',
             'R_BEARDGUY_MEXICAN_HATBALL_E_CNT','R_BEARDGUY_MEXICAN_HATBALL_F_CNT',
             'L_HEAD_JAW0_CNT', 'C_BEARDGUY_BEARD0_CNT', 'C_BEARDGUY_BEARD1_CNT', 'C_BEARDGUY_BEARD2_CNT',
             'C_BEARDGUY_BEARD3_CNT','C_BEARDGUY_HAT_CNT','L_BEARDGUY_SHOULDERUP_CNT',
             'R_BEARDGUY_SHOULDERUP_CNT']

#nameSpace = ''
#sel = mc.ls(sl=True)[0]
#if mc.referenceQuery( sel, isNodeReferenced=True ):
#    nameSpace = sel.split(':')[0] + ':'
#namespaces = cmds.namespaceInfo(lon=True)
#current_namespace = cmds.namespaceInfo(currentNamespace=True)
#references = cmds.ls(type="reference")

def agregarnameSpace(lista=[],nameSpace=''):
    newList=[]
    namespacesScene = cmds.namespaceInfo(lon=True)
    if nameSpace in namespacesScene:
        for obj in lista:
            if nameSpace in obj:
                cmds.warning('Ya existe el namespace '+ nameSpace + ' en ' + obj)
            else:
                obj=nameSpace+':'+str(obj)
                newList.append(obj)
        return newList
    else:
        cmds.warning('No existe en la escena un namespace llamado: ' + nameSpace)
        return lista


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

def dinamicasOnOffMexico(onOff=False):
    list=cmds.ls('*_BEARDGUY_MEXICAN_HATBALL_*_HSYM',r=True)
    for o in list:
        print o
        if onOff==False:
            cmds.setAttr(str(o)+'.simulationMethod', 0)
            return False
        if onOff==True:
            cmds.setAttr(str(o)+'.simulationMethod', 3)
            return True

#Agrega el namespace si lo necesita
bearGuy=agregarnameSpace(bearGuy,nameCharacter)
bearGuyCNT=agregarnameSpace(bearGuyCNT)

samurai=agregarnameSpace(samurai,nameCharacter)
samuraiCNTS=agregarnameSpace(samuraiCNTS)

mexican=agregarnameSpace(mexican,nameCharacter)
mexicanCNT=agregarnameSpace(mexicanCNT)

#Check si existen
comprobarObj(bearGuy)
comprobarObj(bearGuyCNT)

comprobarObj(mexican)
comprobarObj(samurai)

#Prende bearGuy
def bearGuyBtn(*args):
    onOffVisibility(bearGuy,samurai)
    onOffVisibility(bearGuy,mexican)
    onOffVisibility(bearGuyCNT,mexicanCNT)
    onOffVisibility(bearGuyCNT,samuraiCNTS)

#Prende samurai
def samuraiBtn(*args):
    onOffVisibility(samurai,bearGuy)
    onOffVisibility(samurai,mexican)
    onOffVisibility(samuraiCNTS,mexicanCNT)
    onOffVisibility(samuraiCNTS,bearGuyCNT)
#Prende mexican
def mexicanBtn(*args):
    onOffVisibility(mexican,bearGuy)
    onOffVisibility(mexican,samurai)
    onOffVisibility(mexicanCNT,bearGuyCNT)
    onOffVisibility(mexicanCNT,samuraiCNTS)

def win(nameChar=''):

    if cmds.window('facialUi', ex=True):
        cmds.deleteUI('facialUi')
    win = cmds.window('facialUi', title='FACIAL UI - ' + nameChar, widthHeight=[400,700] )
    FacialGUI = cmds.formLayout()
    panel=cmds.modelPanel()

    FacialPanel=cmds.modelPanel(panel,edit=True,camera=nameChar + 'BEARDGUY_FACE_UI_CAM')
    cmds.formLayout(FacialGUI, e=True,
                    attachForm=[
                        (FacialPanel, "top", 0),
                        (FacialPanel, "left", 0),
                        (FacialPanel, "bottom", 0),
                        (FacialPanel, "right", 0)])

    column = cmds.rowLayout(numberOfColumns=4)
    cmds.symbolButton("bearGuyBtn", command=bearGuyBtn,image = r"F:\EMPRESAS\2VEINTE\MICROSOFT_VR\ASSETS\CHARS\02_BEARDGUY\beardguy_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    cmds.symbolButton("samuraiBtn", command=samuraiBtn,image = r"F:\EMPRESAS\2VEINTE\MICROSOFT_VR\ASSETS\CHARS\02_BEARDGUY\samurai_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    cmds.symbolButton("mexicanBtn", command=mexicanBtn,image = r"F:\EMPRESAS\2VEINTE\MICROSOFT_VR\ASSETS\CHARS\02_BEARDGUY\mexican_btn.png", width = 100, height = 100, backgroundColor = [0.2, 0.2, 0.2])
    column = cmds.rowLayout(numberOfColumns=1)
    cmds.checkBox("dinamicCheckBox", label = "Dinamic_Mexican_Hat", onCommand = "dinamicasOnOffMexico(True)", offCommand = "dinamicasOnOffMexico(False)", value = 0)

    cmds.showWindow(win)

win()
