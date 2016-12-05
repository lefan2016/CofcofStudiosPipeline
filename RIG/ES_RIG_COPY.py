# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.utils as mUtil
import sys , os
from PySide2 import QtCore, QtGui, QtUiTools
path=r'P:\LOCAL\ES_SCRIPTS\RIG'
if not path in sys.path:
	sys.path.append(path)
import UNREAL_EXPORT_ as urExport
import UTIL.UTILITYES as utl

class RigCopyUI():
    def __init__(self):
        #UI START
        loader = QtUiTools.QUiLoader()
        currentDir = os.path.dirname(__file__)
        uifile = QtCore.QFile(currentDir+'/rigcopy.ui')
        uifile.open(QtCore.QFile.ReadOnly)
        self.UI = loader.load(uifile) # Qt objects are inside ui, so good idea to save the variable to the class, 2nd arg should refer to self
        uifile.close()

        #VARIABLES RIG
        nombreRig='Rig_Copy'
        #SET DE FUNCIONES
        self.UI.agregarBt.clicked.connect(self.setList)
        #self.UI.agregarBt.clicked.connect(lambda: self.setList(seleccion))
        self.UI.copyRigBt.clicked.connect(self.createRig)
        #SET DE OTRAS OPCIONES
        self.UI.lineEdit.setText(nombreRig.upper())
        #ENLISTO AL INICIO LA seleccion
        self.setList()
        #UI SHOW
        self.UI.show()

    def setList(self):
        seleccion=cmds.ls(sl=True)
        if seleccion:
            for sel in seleccion:
                if cmds.nodeType(sel)=='transform':
                    cant=range(len(seleccion))
                    self.UI.wLista.clear()#limpio la lista
                    for i in cant:
                        #filtro solo los mesh
                        if cmds.nodeType(cmds.listRelatives(seleccion[i],children=True)[0])=='mesh':
                            self.UI.wLista.addItem( str(seleccion[i]) )
                        else:
                            cmds.warning(str(seleccion[i])+' no es del tipo mesh.')
        else:
            cmds.warning('Nesecitas seleccionar algun mesh con skin.')

    def getList(self):#para una lista de tipo items
        items =self.UI.wLista.count()
        self.selectedItems=[]
        for i in range(items):
            if self.UI.wLista.isItemSelected(self.UI.wLista.item(i))==True:
                self.selectedItems.append(self.UI.wLista.item(i).text())
        return self.selectedItems

    def createRig(self):#Cuando se llama se piden todos los datos
        selecItems = self.getList()
        nombreRig = self.UI.lineEdit.text()
        bake=self.UI.checkBox.isChecked()
        urExport.skeletalCopy(sources=selecItems, rootName=nombreRig, bake=bake)
