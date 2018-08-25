# @Date:   2018-04-16T21:50:11-03:00
# @Last modified time: 2018-08-25T19:09:46-03:00
# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.utils as mUtil
import sys , os
from PySide2 import QtCore, QtGui, QtUiTools
from math import sqrt
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as mui
import weakref
import json
import shiboken2
class puntaApunta():

    def __init__(self):
        self.nombreRig = 'L_FINGER_RING'
        self.locNumber = 3
        self.listaLocators=[]
        self.sLocator=None
        self.eLocator=None
        self.grp=None

    #Borro lo que esta en memoria
    def __del__(self):
        print ('salio y borro todo')
        cmds.delete(cmds.select(self.listaLocators))

    def getMayaWindow():
        pointer = mui.MQtUtil.mainWindow()
        return shiboken2.wrapInstance(long(pointer), QtWidgets.QWidget)

    def win(self):
        #UI START
        loader = QtUiTools.QUiLoader()
        currentDir = os.path.dirname(__file__)
        uifile = QtCore.QFile(currentDir+'/puntaApuntaRig.ui')
        uifile.open(QtCore.QFile.ReadOnly)
        self.UI = loader.load(uifile) # Qt objects are inside ui, so good idea to save the variable to the class, 2nd arg should refer to self
        uifile.close()

        #SET DE FUNCIONES
        self.UI.startEndBt.clicked.connect(self.crearLocatorsStartEnd)
        #self.UI.locatorsBt.clicked.connect(lambda: self.crearLocsIntermedios)
        self.UI.locatorsBt.clicked.connect(self.crearLocsIntermedios)
        self.UI.jointsBt.clicked.connect(self.createJoints)
        #Valor inicial del seleccionEdge
        self.UI.spinBox.setValue(self.locNumber)
        #SET DE OTRAS OPCIONES
        self.UI.lineEdit.setText(self.nombreRig.upper())
        #UI SHOW
        self.UI.show()

def saveJSONFile(dataBlock, filePath):
    outputFile = open(filePath, 'w')
    JSONData = json.dumps(dataBlock, sort_keys=True, indent=4)
    outputFile.write(JSONData)
    outputFile.close()


def loadJSONFile(filePath):
    inputFile = open(filePath, 'r')
    JSONData = json.load(inputFile)
    inputFile.close()
    return JSONData


pathFile = 'N:/CLOUDNAS/EMPRESAS/HookUpAnimation/GILG/02_ANIMATION/ESC01/PL001/MOCAP/'
filename = 'gilgameshTest'
ext = '.mocapFace'
nameSpace= 'C01_GilgameshViaje_rig_v025'

def createDataLinkMocap():

    sel=[]
    sel=cmds.ls(sl=True,type=['joint','transform'])
    facePoints={}
    #Orden de seleccion primero el joint luego el punto y guardo en listas.
    jnt=[]
    lct=[]
    for j in range(len(sel)):
        if j%2 == 0:
            jnt.append(sel[j])
        if j%2 == 1:
            lct.append(sel[j])

    #Grabo todo en un diccionario
    for j in jnt:
        if ':' in j: j=j.split(':')[-1]
        for l in lct:
            if ':' in l: l=l.split(':')[-1]
            facePoints[j]=l

    #Leo el diccionario
    for k,v in facePoints.items():
        print (k,'>>>',v)

    #Grabo en archivo
    #utl.saveJSONFile(facePoints,pathFile+filename+ext)

    #cargo los datos del archivos
    datos = loadJSONFile(pathFile+filename+ext)
    return datos

def doLinkMocap(datos={}):
    #Crear links Constraint
    for j,p in datos.items():

        if nameSpace:
            j=nameSpace+':'+j
        #si es un joint sigo
        if cmds.objExists(j) and cmds.nodeType(j)=='joint':
            attrs=cmds.listAttr (j, keyable=1)
            for attr in attrs:
                try:
                    cmds.setAttr (j+"."+attr, lock=0)
                except:
                    pass
            #si no estaba emparentado sigo
            if not cmds.objExists(str(j)+'_PCNS'):
                cmds.parentConstraint(p,j,name=str(j)+'_TLINK_PCNS',maintainOffset=True)
            if not cmds.objExists(str(j)+'_SCNS'):
                cmds.scaleConstraint(p,j,name=str(j)+'_TLINK_SCNS',maintainOffset=True)

def deleteConstraints():
    cnts=cmds.ls('*_TLINK_*',type='constraint',r=1)
    for cnt in cnts:
        if cmds.nodeType(cnt)=='parentConstraints'or'pointConstraints'or'orientConstraints'or'scaleConstraint':
            cmds.delete(cnt)
