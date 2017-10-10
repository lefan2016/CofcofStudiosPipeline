# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'P:\LOCAL\ES_SCRIPTS\RIG\ES_AUTORIG\autoRigUI.ui'
#
# Created: Tue Aug 23 15:25:12 2016
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui

class Ui_autoRigUI(object):
    def setupUi(self, autoRigUI):
        autoRigUI.setObjectName("autoRigUI")
        autoRigUI.resize(651, 498)
        self.buttonBoxOk = QtGui.QDialogButtonBox(autoRigUI)
        self.buttonBoxOk.setGeometry(QtCore.QRect(460, 440, 151, 32))
        self.buttonBoxOk.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxOk.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBoxOk.setCenterButtons(False)
        self.buttonBoxOk.setObjectName("buttonBoxOk")

        self.retranslateUi(autoRigUI)
        QtCore.QObject.connect(self.buttonBoxOk, QtCore.SIGNAL("accepted()"), autoRigUI.accept)
        QtCore.QObject.connect(self.buttonBoxOk, QtCore.SIGNAL("rejected()"), autoRigUI.reject)
        QtCore.QMetaObject.connectSlotsByName(autoRigUI)

    def retranslateUi(self, autoRigUI):
        autoRigUI.setWindowTitle(QtGui.QApplication.translate("autoRigUI", "AUTO RIG - COFCOF STUDIOS", None, QtGui.QApplication.UnicodeUTF8))
