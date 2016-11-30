# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import sys
from PySide2 import QtCore, QtGui, QtUiTools
path=r'P:\LOCAL\ES_SCRIPTS\RIG'
if not path in sys.path:
	sys.path.append(path)
import UNREAL_EXPORT_ as urExport
import UTIL.UTILITYES as utl

class snailUI():
    def __init__(self):
        #UI START
        self.dir=r'P:/LOCAL/ES_SCRIPTS/RIG/SNAIL/'
        self.fileui='snailUI.ui'
        self.uiFile=self.dir+self.fileui
        loader = QtUiTools.QUiLoader()
        #loader.registerCustomWidget(snailTools)
        self.rwin = loader.load(self.uiFile)

        #VARIABLES RIG
        self.nombreRig=''

        #USO DE FUNCIONES
        self.rwin.agregarBt.clicked.connect(self.setMesh())
        self.rwin.copyRigBt.clicked.connect(self.createRig())

        #UI SHOW
        self.rwin.show()

    def setMesh(self):
        self.seleccion=cmds.ls(sl=1)
        self.selectGeo=[]
        selectGeo=cmds.listRelatives(self.seleccion ,children=True,fullPath=True)
        for obj in selectGeo:
            self.rwin.listView.setText(str(obj))

    def createRig(self):
        #seleccion=self.rwin.listView.clicked.connect(setMesh)
        urExport.skeletalCopy(sources=seleccion, rootName=nombreRig, bake=False)
