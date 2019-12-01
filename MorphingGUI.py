# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xxx.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(876, 830)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Loadstartbtn = QtWidgets.QPushButton(self.centralwidget)
        self.Loadstartbtn.setGeometry(QtCore.QRect(30, 10, 181, 31))
        self.Loadstartbtn.setObjectName("Loadstartbtn")
        self.Loadendbtn = QtWidgets.QPushButton(self.centralwidget)
        self.Loadendbtn.setGeometry(QtCore.QRect(480, 10, 181, 31))
        self.Loadendbtn.setObjectName("Loadendbtn")
        self.Endimage = QtWidgets.QGraphicsView(self.centralwidget)
        self.Endimage.setGeometry(QtCore.QRect(480, 50, 360, 270))
        self.Endimage.setObjectName("Endimage")
        self.Startimage = QtWidgets.QGraphicsView(self.centralwidget)
        self.Startimage.setGeometry(QtCore.QRect(30, 50, 360, 270))
        self.Startimage.setObjectName("Startimage")
        self.Startinglabel = QtWidgets.QLabel(self.centralwidget)
        self.Startinglabel.setGeometry(QtCore.QRect(110, 330, 161, 31))
        self.Startinglabel.setObjectName("Startinglabel")
        self.Endinglable = QtWidgets.QLabel(self.centralwidget)
        self.Endinglable.setGeometry(QtCore.QRect(580, 330, 161, 31))
        self.Endinglable.setObjectName("Endinglable")
        self.Triangleshow = QtWidgets.QCheckBox(self.centralwidget)
        self.Triangleshow.setGeometry(QtCore.QRect(370, 340, 141, 31))
        self.Triangleshow.setObjectName("Triangleshow")
        self.Linebar = QtWidgets.QSlider(self.centralwidget)
        self.Linebar.setEnabled(True)
        self.Linebar.setGeometry(QtCore.QRect(90, 370, 691, 20))
        self.Linebar.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.Linebar.setMouseTracking(False)
        self.Linebar.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Linebar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.Linebar.setAcceptDrops(False)
        self.Linebar.setMaximum(100)
        self.Linebar.setSingleStep(5)
        self.Linebar.setPageStep(5)
        self.Linebar.setProperty("value", 0)
        self.Linebar.setSliderPosition(0)
        self.Linebar.setTracking(True)
        self.Linebar.setOrientation(QtCore.Qt.Horizontal)
        self.Linebar.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.Linebar.setTickInterval(10)
        self.Linebar.setObjectName("Linebar")
        self.A_label = QtWidgets.QLabel(self.centralwidget)
        self.A_label.setGeometry(QtCore.QRect(40, 370, 41, 17))
        self.A_label.setObjectName("A_label")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 390, 21, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(760, 390, 21, 17))
        self.label_2.setObjectName("label_2")
        self.Alphacof = QtWidgets.QLineEdit(self.centralwidget)
        self.Alphacof.setGeometry(QtCore.QRect(790, 370, 61, 21))
        self.Alphacof.setAlignment(QtCore.Qt.AlignCenter)
        self.Alphacof.setReadOnly(True)
        self.Alphacof.setObjectName("Alphacof")
        self.Morphimage = QtWidgets.QGraphicsView(self.centralwidget)
        self.Morphimage.setGeometry(QtCore.QRect(260, 420, 360, 270))
        self.Morphimage.setObjectName("Morphimage")
        self.Blendinglabel = QtWidgets.QLabel(self.centralwidget)
        self.Blendinglabel.setGeometry(QtCore.QRect(360, 700, 161, 31))
        self.Blendinglabel.setObjectName("Blendinglabel")
        self.Blendbtn = QtWidgets.QPushButton(self.centralwidget)
        self.Blendbtn.setGeometry(QtCore.QRect(360, 750, 161, 31))
        self.Blendbtn.setObjectName("Blendbtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Loadstartbtn.setText(_translate("MainWindow", "Load Starting Image ..."))
        self.Loadendbtn.setText(_translate("MainWindow", "Load Ending Image ..."))
        self.Startinglabel.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Starting Image</span></p></body></html>"))
        self.Endinglable.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Ending Image</span></p></body></html>"))
        self.Triangleshow.setText(_translate("MainWindow", "Show Triangles"))
        self.A_label.setText(_translate("MainWindow", "Alpha"))
        self.label.setText(_translate("MainWindow", "0.0"))
        self.label_2.setText(_translate("MainWindow", "1.0"))
        self.Alphacof.setText(_translate("MainWindow", "0.0"))
        self.Blendinglabel.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Blending Result</span></p></body></html>"))
        self.Blendbtn.setText(_translate("MainWindow", "Blend"))

