# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.utils as mUtil
import sys , os
from PySide2 import QtCore, QtGui, QtUiTools
from math import sqrt
import maya.OpenMaya as OpenMaya

'''
import maya.cmds
import sys
path=r'F:\Repositores\GitHub\ES_SCRIPTS\RIG'
if not path in sys.path:
	sys.path.append(path)
import puntaApuntaRig as paprig
reload(paprig)
UI2=paprig.puntaApunta()
UI2.win()

'''
class puntaApunta():

    def __init__(self):
        self.nombreRig = 'L_FINGER_RING'
        self.locNumber = 3
        self.listaLocators=[]
        self.sLocator=None
        self.eLocator=None
        self.grp=None

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

        self.grp=cmds.group(em=True, n=nombreRig + '_GRP')
        cmds.parent([self.sLocator,self.eLocator],self.grp)

        return self.sLocator,self.eLocator

    def crearLocsIntermedios(self):
        #Cantidad de intermedios
        self.locNumber = self.UI.spinBox.value()
        #Nombre del rig a colocar se toma de la UI
        nombreRig=self.UI.lineEdit.text()
        self.sLocator=nombreRig+"START"+'_LOC'
        self.eLocator=nombreRig+"END"+'_LOC'
        # UI Options
        if cmds.objExists(nombreRig+"START"+'_LOC') and cmds.objExists(nombreRig+"END"+'_LOC'):
            print 'funca2'
            self.listaLocators=[]
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
            for i in range(self.locNumber):
                newPoint = mVectorResult * distMultiplier
                finalPoint = mVectorStart + newPoint
                distMultiplier = distMultiplier + avgDist
                locator = cmds.spaceLocator(n=nombreRig+str(i)+'_LOC')
                cmds.move( finalPoint.x, finalPoint.y, finalPoint.z, locator[0], rpr=True )
                self.listaLocators.append( locator[0] )
                cmds.parent( locator[0],self.grp )
            self.listaLocators.insert( 0, self.sLocator )
            self.listaLocators.insert( len(self.listaLocators), self.eLocator )
            print self.listaLocators
            return self.listaLocators
        else:
            cmds.warning('No concuerda con start y ends')

    def createJoints(self):
        print 'joint si'
        jointsList=[]
        nombreRig=self.UI.lineEdit.text()
        if not self.listaLocators:
            self.listaLocators=cmds.ls(nombreRig+'*_LOC', type='transform')
            self.listaLocators.remove(nombreRig+'END_LOC')
            self.listaLocators.remove(nombreRig+'START_LOC')
            self.listaLocators.sort()
            self.listaLocators.insert(0,nombreRig+'START_LOC')
            self.listaLocators.append(nombreRig+'END_LOC')

        if self.listaLocators:
            print 'entro'
            for loc in range(len(self.listaLocators)):
                pos = cmds.xform(self.listaLocators[loc], q=True, ws=True,m=True)
                joint = cmds.joint(n=nombreRig+str(loc)+'_JNT')
                cmds.xform(joint,m=1)
                if str(self.listaLocators[loc])==nombreRig+'START'+'_LOC':
                    #copiar orientacion primer loc
                    ocnt=cmds.orientConstraint(self.listaLocators[loc],joint)
                    cmds.delete(ocnt)
                jointsList.append(joint)
            #cmds.listRelatives( jointsList[0] )
            try:
                #emparento al mundo el primer joint
                cmds.parent(jointsList[0],world=True)
                #emparento todo al grupo para ordenar
                cmds.parent( jointsList[0],self.grp )
            except:
                pass
            #Orientar el joint
            cmds.joint(jointsList[0],edit=True, orientJoint='xyz', secondaryAxisOrient='yup',children=True, zeroScaleOrient=True)
        else:
            self.listaLocators.append( cmds.ls(nombreRig+'*_LOC')[0] )
            self.createJoint
            return jointsList
