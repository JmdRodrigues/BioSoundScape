# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_maineamzOI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1047, 883)
        icon = QIcon()
        icon.addFile(u"images/plux_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u"images/plux_logo.png", QSize(), QIcon.Normal, QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"QFrame{\n"
"background-color:rgb(84, 84, 84);\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.Title = QLabel(self.frame)
        self.Title.setObjectName(u"Title")
        self.Title.setGeometry(QRect(10, 0, 291, 41))
        font = QFont()
        font.setFamily(u"Verdana")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.Title.setFont(font)
        self.Title.setStyleSheet(u"color: rgb(235, 235, 235)")
        self.Title.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 50, 241, 451))
        font1 = QFont()
        font1.setFamily(u"Verdana")
        self.groupBox.setFont(font1)
        self.groupBox.setStyleSheet(u"color:rgb(255, 255, 255)")
        self.comboBox_examples = QComboBox(self.groupBox)
        self.comboBox_examples.addItem("")
        self.comboBox_examples.addItem("")
        self.comboBox_examples.addItem("")
        self.comboBox_examples.addItem("")
        self.comboBox_examples.addItem("")
        self.comboBox_examples.setObjectName(u"comboBox_examples")
        self.comboBox_examples.setGeometry(QRect(10, 70, 201, 22))
        self.comboBox_examples.setFont(font1)
        self._Examples = QLabel(self.groupBox)
        self._Examples.setObjectName(u"_Examples")
        self._Examples.setGeometry(QRect(10, 40, 171, 20))
        self.label_samplingRate = QLabel(self.groupBox)
        self.label_samplingRate.setObjectName(u"label_samplingRate")
        self.label_samplingRate.setGeometry(QRect(10, 170, 55, 21))
        self.textEdit_sampling_rate = QTextEdit(self.groupBox)
        self.textEdit_sampling_rate.setObjectName(u"textEdit_sampling_rate")
        self.textEdit_sampling_rate.setGeometry(QRect(160, 170, 51, 31))
        self.label_signalType = QLabel(self.groupBox)
        self.label_signalType.setObjectName(u"label_signalType")
        self.label_signalType.setGeometry(QRect(10, 210, 55, 21))
        self.comboBox_signalType = QComboBox(self.groupBox)
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.setObjectName(u"comboBox_signalType")
        self.comboBox_signalType.setGeometry(QRect(120, 210, 91, 22))
        self.comboBox_signalType.setFont(font1)
        self.label_macAddress = QLabel(self.groupBox)
        self.label_macAddress.setObjectName(u"label_macAddress")
        self.label_macAddress.setGeometry(QRect(10, 120, 55, 21))
        self.textEdit_mac_address = QTextEdit(self.groupBox)
        self.textEdit_mac_address.setObjectName(u"textEdit_mac_address")
        self.textEdit_mac_address.setGeometry(QRect(60, 120, 151, 31))
        self.pushButton_Launch = QPushButton(self.groupBox)
        self.pushButton_Launch.setObjectName(u"pushButton_Launch")
        self.pushButton_Launch.setGeometry(QRect(10, 290, 93, 28))
        self.pushButton_Stop = QPushButton(self.groupBox)
        self.pushButton_Stop.setObjectName(u"pushButton_Stop")
        self.pushButton_Stop.setEnabled(False)
        self.pushButton_Stop.setGeometry(QRect(130, 290, 93, 28))
        self.frame_Plots = QFrame(self.frame)
        self.frame_Plots.setObjectName(u"frame_Plots")
        self.frame_Plots.setGeometry(QRect(270, 60, 731, 731))
        self.frame_Plots.setFrameShape(QFrame.StyledPanel)
        self.frame_Plots.setFrameShadow(QFrame.Raised)
        self.graphBiosignal = QWidget(self.frame_Plots)
        self.graphBiosignal.setObjectName(u"graphBiosignal")
        self.graphBiosignal.setGeometry(QRect(20, 20, 680, 150))
        self.graphSound = QWidget(self.frame_Plots)
        self.graphSound.setObjectName(u"graphSound")
        self.graphSound.setGeometry(QRect(20, 190, 680, 150))
        self.graphSpectral = QWidget(self.frame_Plots)
        self.graphSpectral.setObjectName(u"graphSpectral")
        self.graphSpectral.setGeometry(QRect(20, 370, 680, 341))

        self.verticalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1047, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Title.setText(QCoreApplication.translate("MainWindow", u"<strong>Bio</strong>SoundScape", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Configuration", None))
        self.comboBox_examples.setItemText(0, QCoreApplication.translate("MainWindow", u"Example 1", None))
        self.comboBox_examples.setItemText(1, QCoreApplication.translate("MainWindow", u"Example 2", None))
        self.comboBox_examples.setItemText(2, QCoreApplication.translate("MainWindow", u"Example 3", None))
        self.comboBox_examples.setItemText(3, QCoreApplication.translate("MainWindow", u"Example 4", None))
        self.comboBox_examples.setItemText(4, QCoreApplication.translate("MainWindow", u"Example 5", None))

        self._Examples.setText(QCoreApplication.translate("MainWindow", u"Select Example", None))
        self.label_samplingRate.setText(QCoreApplication.translate("MainWindow", u"SR", None))
        self.textEdit_sampling_rate.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1000</p></body></html>", None))
        self.textEdit_sampling_rate.setPlaceholderText(QCoreApplication.translate("MainWindow", u"sampling rate", None))
        self.label_signalType.setText(QCoreApplication.translate("MainWindow", u"Signal", None))
        self.comboBox_signalType.setItemText(0, QCoreApplication.translate("MainWindow", u"ECG", None))
        self.comboBox_signalType.setItemText(1, QCoreApplication.translate("MainWindow", u"EMG", None))
        self.comboBox_signalType.setItemText(2, QCoreApplication.translate("MainWindow", u"ACC_X", None))
        self.comboBox_signalType.setItemText(3, QCoreApplication.translate("MainWindow", u"ACC_Y", None))
        self.comboBox_signalType.setItemText(4, QCoreApplication.translate("MainWindow", u"ACC_Z", None))
        self.comboBox_signalType.setItemText(5, QCoreApplication.translate("MainWindow", u"Force", None))
        self.comboBox_signalType.setItemText(6, QCoreApplication.translate("MainWindow", u"EDA", None))

        self.label_macAddress.setText(QCoreApplication.translate("MainWindow", u"MAC", None))
        self.textEdit_mac_address.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">00:07:80:8C:AD:C9</p></body></html>", None))
        self.textEdit_mac_address.setPlaceholderText(QCoreApplication.translate("MainWindow", u"mac address...", None))
        self.pushButton_Launch.setText(QCoreApplication.translate("MainWindow", u"Launch", None))
        self.pushButton_Stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
    # retranslateUi

