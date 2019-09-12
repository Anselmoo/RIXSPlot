# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subwindow_RIXS.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RIXS(object):
    def setupUi(self, RIXS):
        RIXS.setObjectName("RIXS")
        RIXS.resize(1200, 720)
        RIXS.setMinimumSize(QtCore.QSize(1200, 720))
        RIXS.setMaximumSize(QtCore.QSize(1200, 720))
        RIXS.setAutoFillBackground(False)
        self.line = QtWidgets.QFrame(RIXS)
        self.line.setGeometry(QtCore.QRect(-10, 840, 1221, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(RIXS)
        self.line_2.setGeometry(QtCore.QRect(0, 60, 1201, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(RIXS)
        self.line_3.setGeometry(QtCore.QRect(0, 10, 1201, 21))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.pushCLEAR = QtWidgets.QPushButton(RIXS)
        self.pushCLEAR.setGeometry(QtCore.QRect(1110, 850, 74, 32))
        self.pushCLEAR.setObjectName("pushCLEAR")
        self.pushLegend = QtWidgets.QPushButton(RIXS)
        self.pushLegend.setGeometry(QtCore.QRect(1020, 850, 88, 32))
        self.pushLegend.setObjectName("pushLegend")
        self.splitter = QtWidgets.QSplitter(RIXS)
        self.splitter.setGeometry(QtCore.QRect(810, 0, 234, 32))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.Legend_Button = QtWidgets.QPushButton(self.splitter)
        self.Legend_Button.setObjectName("Legend_Button")
        self.Clear_Button = QtWidgets.QPushButton(self.splitter)
        self.Clear_Button.setObjectName("Clear_Button")
        self.Save_Button = QtWidgets.QPushButton(self.splitter)
        self.Save_Button.setObjectName("Save_Button")
        self.pushCLEAR.raise_()
        self.pushLegend.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.line_3.raise_()
        self.splitter.raise_()

        self.retranslateUi(RIXS)
        QtCore.QMetaObject.connectSlotsByName(RIXS)

    def retranslateUi(self, RIXS):
        _translate = QtCore.QCoreApplication.translate
        RIXS.setWindowTitle(_translate("RIXS", "RIXS Map"))
        self.pushCLEAR.setText(_translate("RIXS", "Clear"))
        self.pushLegend.setText(_translate("RIXS", "Legend"))
        self.Legend_Button.setText(_translate("RIXS", "Legend"))
        self.Clear_Button.setText(_translate("RIXS", "Clear"))
        self.Save_Button.setText(_translate("RIXS", "Save"))
