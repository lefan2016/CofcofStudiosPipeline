# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.utils as mUtil
import sys , os
from PySide2 import QtCore, QtGui, QtUiTools
from math import sqrt
import maya.OpenMaya as OpenMaya

#RIG FINGER
class puntaApunta():

    def __init__(self):
        self.namefield = 'C_SPINE_SPINE'
        self.locNumber = 2
        self.listaLocators=[]
        self.sLocator=None
        self.eLocator=None
        #UI START
        loader = QtUiTools.QUiLoader()
        currentDir = os.path.dirname(__file__)
        uifile = QtCore.QFile(currentDir+'/puntaApuntaRig.ui')
        uifile.open(QtCore.QFile.ReadOnly)
        self.UI = loader.load(uifile) # Qt objects are inside ui, so good idea to save the variable to the class, 2nd arg should refer to self
        uifile.close()

        #VARIABLES RIG
        nombreRig='puntaApuntaRig'
        #SET DE FUNCIONES
        self.UI.startEndBt.clicked.connect(self.crearLocatorsStartEnd)
        self.UI.locatorsBt.clicked.connect(lambda: self.crearLocsIntermedios)
        #self.UI.locatorsBt.clicked.connect(self.crearLocsIntermedios)
        self.UI.jointsBt.clicked.connect(self.createJoints)
        #SET DE OTRAS OPCIONES
        self.UI.lineEdit.setText(nombreRig.upper())
        #UI SHOW
        self.UI.show()

    #########################################
    def startLocator(self):
        nombreRig=self.UI.lineEdit.text()
        nameLoc=nombreRig+"START"+'_LOC'
        if cmds.objExists(nameLoc):
            cmds.warning('Porfavor elija un nombre que no exista.')
        else:
            locator=cmds.spaceLocator(n=nameLoc)[0]
            cmds.move(0,0,0,locator)
            print 'star creado'
            return locator

    def endLocator(self):
        nombreRig=self.UI.lineEdit.text()
        endLocatorName=nombreRig+"END"+'_LOC'
        if cmds.objExists(endLocatorName):
            cmds.warning('Porfavor elija un nombre que no exista.')
        else:
            locator=cmds.spaceLocator(n=endLocatorName)[0]
            cmds.move(0,7,0,locator)
            print 'end creado'
            return locator

    def crearLocatorsStartEnd(self):
        print 'Funca'
        #Nombre del rig a colocar se toma de la UI
        nombreRig=self.UI.lineEdit.text()
        #Creo los locators y guardo en unas variables los nombres
        self.sLocator=self.startLocator()
        self.eLocator=self.endLocator()
        return self.sLocator,self.eLocator

    def crearLocsIntermedios(self):
        locatorslist=[]
        #Cantidad de intermedios
        self.locNumber = self.UI.spinBox.value()
        #Nombre del rig a colocar se toma de la UI
        nombreRig=self.UI.lineEdit.text()
        # UI Options
        if cmds.objExists(nombreRig+"START"+'_LOC') and cmds.objExists(nombreRig+"END"+'_LOC'):
            print 'funca2'
            avgDist = 1.0 / (self.locNumber + 1)
            # Start/End points
            startPoint = cmds.xform(self.sLocator, q=True, ws=True, rp=True)
            endPoint = cmds.xform(self.eLocator, q=True, ws=True, rp=True)
            # Use maya API vector class
            mVectorStart = OpenMaya.MVector(startPoint[0], startPoint[1], startPoint[2])
            mVectorEnd = OpenMaya.MVector(endPoint[0], endPoint[1], endPoint[2])
            mVectorResult = mVectorEnd - mVectorStart
            # Create a locator per joint number
            distMultiplier = avgDist
            self.listaLocators=[]
            for i in range(self.locNumber):
                newPoint = mVectorResult * distMultiplier
                finalPoint = mVectorStart + newPoint
                distMultiplier = distMultiplier + avgDist

                locator=cmds.spaceLocator(n=nombreRig+str(i)+'_LOC')
                cmds.move(finalPoint.x, finalPoint.y, finalPoint.z, locator[0], rpr=True)
                self.listaLocators.append(locator)
            self.listaLocators.insert(0, startLocator)
            self.listaLocators.insert(len(self.listaLocators), endLocator)
        else:
            cmds.warning('No concuerda con start y ends')
        return self.listaLocators

    def createJoints(self):
        jointsList=[]
        if self.listaLocators:
            for loc in range(len(self.listaLocators)):
                pos = cmds.xform(self.listaLocators[loc], q=True, ws=True, rp=True)
                joint=cmds.joint(n=str(self.namefield)+str(loc)+'_JNT')
                cmds.move(pos[0],pos[1],pos[2], joint, rpr=True)
                jointsList.append(joint)
            #emparento al mundo el primer joint
            cmds.parent(jointsList[0],world=True)
            #Orientar el joint
            cmds.joint(jointsList[0],edit=True, orientJoint='xyz', secondaryAxisOrient='yup',children=True, zeroScaleOrient=True)
