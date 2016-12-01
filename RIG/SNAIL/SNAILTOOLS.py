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
        self.UI = loader.load(self.uiFile)

        #VARIABLES RIG
        nombreRig='snail'
        seleccion=cmds.ls(sl=1)
        if seleccion==None:
            cmds.warning('Nada seleccionado.')
        #SET DE FUNCIONES
        self.UI.agregarBt.clicked.connect(lambda: self.setMesh(seleccion))
        self.UI.copyRigBt.clicked.connect(self.createRig)
        #SET DE OTRAS OPCIONES
        self.UI.textEdit.setText(nombreRig.upper())

        #UI SHOW
        self.UI.show()

    def setMesh(self,seleccion=None):
        if seleccion:
            self.UI.wLista.clear()#limpio la lista
            selectGeo = cmds.listRelatives(seleccion, children=True,type='transform' )
            cant=range(len(selectGeo))
            for i in cant:
                #filtro solo los mesh
                if cmds.nodeType(cmds.listRelatives(selectGeo[i],children=True)[0])=='mesh':
                    self.UI.wLista.addItem( str(selectGeo[i]) )
        else:
            print 'Nada'

    def getList(self):#para una lista de tipo items
        items =self.UI.wLista.count()
        selectedItems=[]
        itemsText=[]
        for i in range(items):
            if self.UI.wLista.isItemSelected(self.UI.wLista.item(i))==True:
                selectedItems.append(self.UI.wLista.item(i).text())
        for i in range(items):
            temp= self.UI.wLista.item(i).text()
            itemsText.append(temp)
        return selectedItems

    def createRig(self):
        selecItems=self.getList()
        nombreRig=self.UI.textEdit.toPlainText()
        print selecItems
        print self.UI.textEdit.toPlainText()
        #urExport.skeletalCopy(sources=selecItems, rootName=nombreRig, bake=False)
