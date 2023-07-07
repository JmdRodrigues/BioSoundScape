# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'intro_loaderGGTvbb.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_LoadingScreen(object):
    def setupUi(self, LoadingScreen):
        if not LoadingScreen.objectName():
            LoadingScreen.setObjectName(u"LoadingScreen")
        LoadingScreen.resize(765, 545)
        self.centralwidget = QWidget(LoadingScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(u"QFrame{\n"
"background-color:rgb(84, 84, 84);\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)
        self.Title = QLabel(self.dropShadowFrame)
        self.Title.setObjectName(u"Title")
        self.Title.setGeometry(QRect(60, 100, 651, 101))
        font = QFont()
        font.setFamily(u"Verdana")
        font.setPointSize(40)
        font.setBold(False)
        font.setWeight(50)
        self.Title.setFont(font)
        self.Title.setStyleSheet(u"color: rgb(235, 235, 235)")
        self.Title.setAlignment(Qt.AlignCenter)
        self.plux_logo = QLabel(self.dropShadowFrame)
        self.plux_logo.setObjectName(u"plux_logo")
        self.plux_logo.setGeometry(QRect(20, 450, 101, 41))
        self.plux_logo.setPixmap(QPixmap(u"images/plux_logo.png"))
        self.plux_logo.setScaledContents(True)
        self.nova_logo = QLabel(self.dropShadowFrame)
        self.nova_logo.setObjectName(u"nova_logo")
        self.nova_logo.setGeometry(QRect(130, 420, 131, 91))
        self.nova_logo.setPixmap(QPixmap(u"images/nova_logo.png"))
        self.nova_logo.setScaledContents(True)
        self.groupBox = QGroupBox(self.dropShadowFrame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(100, 220, 571, 201))
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
        self.comboBox_examples.addItem("")
        self.comboBox_examples.addItem("")
        self.comboBox_examples.setObjectName(u"comboBox_examples")
        self.comboBox_examples.setEnabled(True)
        self.comboBox_examples.setGeometry(QRect(20, 60, 291, 22))
        self.comboBox_examples.setFont(font1)
        self._Examples = QLabel(self.groupBox)
        self._Examples.setObjectName(u"_Examples")
        self._Examples.setGeometry(QRect(80, 30, 171, 20))
        self._Examples.setAlignment(Qt.AlignCenter)
        self.label_samplingRate = QLabel(self.groupBox)
        self.label_samplingRate.setObjectName(u"label_samplingRate")
        self.label_samplingRate.setGeometry(QRect(340, 70, 55, 21))
        self.textEdit_sampling_rate = QTextEdit(self.groupBox)
        self.textEdit_sampling_rate.setObjectName(u"textEdit_sampling_rate")
        self.textEdit_sampling_rate.setEnabled(True)
        self.textEdit_sampling_rate.setGeometry(QRect(500, 60, 51, 31))
        self.label_signalType = QLabel(self.groupBox)
        self.label_signalType.setObjectName(u"label_signalType")
        self.label_signalType.setGeometry(QRect(340, 110, 55, 21))
        self.comboBox_signalType = QComboBox(self.groupBox)
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.addItem("")
        self.comboBox_signalType.setObjectName(u"comboBox_signalType")
        self.comboBox_signalType.setGeometry(QRect(460, 110, 91, 22))
        self.comboBox_signalType.setFont(font1)
        self.label_macAddress = QLabel(self.groupBox)
        self.label_macAddress.setObjectName(u"label_macAddress")
        self.label_macAddress.setGeometry(QRect(340, 20, 55, 21))
        self.textEdit_mac_address = QTextEdit(self.groupBox)
        self.textEdit_mac_address.setObjectName(u"textEdit_mac_address")
        self.textEdit_mac_address.setEnabled(True)
        self.textEdit_mac_address.setGeometry(QRect(400, 20, 151, 31))
        self.pushButton_Launch = QPushButton(self.groupBox)
        self.pushButton_Launch.setObjectName(u"pushButton_Launch")
        self.pushButton_Launch.setGeometry(QRect(190, 110, 93, 28))
        self.pushButton_Stop = QPushButton(self.groupBox)
        self.pushButton_Stop.setObjectName(u"pushButton_Stop")
        self.pushButton_Stop.setEnabled(False)
        self.pushButton_Stop.setGeometry(QRect(60, 110, 93, 28))
        self.label_buffer_size = QLabel(self.groupBox)
        self.label_buffer_size.setObjectName(u"label_buffer_size")
        self.label_buffer_size.setGeometry(QRect(340, 160, 81, 21))
        self.textEdit_buffer_size = QTextEdit(self.groupBox)
        self.textEdit_buffer_size.setObjectName(u"textEdit_buffer_size")
        self.textEdit_buffer_size.setEnabled(True)
        self.textEdit_buffer_size.setGeometry(QRect(500, 150, 51, 31))

        self.verticalLayout.addWidget(self.dropShadowFrame)

        LoadingScreen.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(LoadingScreen)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 765, 26))
        LoadingScreen.setMenuBar(self.menuBar)

        self.retranslateUi(LoadingScreen)

        QMetaObject.connectSlotsByName(LoadingScreen)
    # setupUi

    def retranslateUi(self, LoadingScreen):
        LoadingScreen.setWindowTitle(QCoreApplication.translate("LoadingScreen", u"MainWindow", None))
        self.Title.setText(QCoreApplication.translate("LoadingScreen", u"<strong>Bio</strong>SoundScape", None))
        self.plux_logo.setText("")
        self.nova_logo.setText("")
        self.groupBox.setTitle("")
        self.comboBox_examples.setItemText(0, QCoreApplication.translate("LoadingScreen", u"Experience 1", None))
        self.comboBox_examples.setItemText(1, QCoreApplication.translate("LoadingScreen", u"Experience 2", None))
        self.comboBox_examples.setItemText(2, QCoreApplication.translate("LoadingScreen", u"Experience 3", None))
        self.comboBox_examples.setItemText(3, QCoreApplication.translate("LoadingScreen", u"Experience 4", None))
        self.comboBox_examples.setItemText(4, QCoreApplication.translate("LoadingScreen", u"Experience 5", None))
        self.comboBox_examples.setItemText(5, QCoreApplication.translate("LoadingScreen", u"Experience 6", None))
        self.comboBox_examples.setItemText(6, QCoreApplication.translate("LoadingScreen", u"Experience 7", None))

        self._Examples.setText(QCoreApplication.translate("LoadingScreen", u"Select Example", None))
        self.label_samplingRate.setText(QCoreApplication.translate("LoadingScreen", u"SR", None))
        self.textEdit_sampling_rate.setHtml(QCoreApplication.translate("LoadingScreen", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1000</p></body></html>", None))
        self.textEdit_sampling_rate.setPlaceholderText(QCoreApplication.translate("LoadingScreen", u"sampling rate", None))
        self.label_signalType.setText(QCoreApplication.translate("LoadingScreen", u"Signal", None))
        self.comboBox_signalType.setItemText(0, QCoreApplication.translate("LoadingScreen", u"ECG", None))
        self.comboBox_signalType.setItemText(1, QCoreApplication.translate("LoadingScreen", u"EMG", None))
        self.comboBox_signalType.setItemText(2, QCoreApplication.translate("LoadingScreen", u"ACC_X", None))
        self.comboBox_signalType.setItemText(3, QCoreApplication.translate("LoadingScreen", u"ACC_Y", None))
        self.comboBox_signalType.setItemText(4, QCoreApplication.translate("LoadingScreen", u"ACC_Z", None))
        self.comboBox_signalType.setItemText(5, QCoreApplication.translate("LoadingScreen", u"Force", None))
        self.comboBox_signalType.setItemText(6, QCoreApplication.translate("LoadingScreen", u"EDA", None))

        self.label_macAddress.setText(QCoreApplication.translate("LoadingScreen", u"MAC", None))
        self.textEdit_mac_address.setHtml(QCoreApplication.translate("LoadingScreen", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">00:07:80:8C:AD:C9</p></body></html>", None))
        self.textEdit_mac_address.setPlaceholderText(QCoreApplication.translate("LoadingScreen", u"mac address...", None))
        self.pushButton_Launch.setText(QCoreApplication.translate("LoadingScreen", u"Launch", None))
        self.pushButton_Stop.setText(QCoreApplication.translate("LoadingScreen", u"Stop", None))
        self.label_buffer_size.setText(QCoreApplication.translate("LoadingScreen", u"Buffer Size", None))
        self.textEdit_buffer_size.setHtml(QCoreApplication.translate("LoadingScreen", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">512</p></body></html>", None))
        self.textEdit_buffer_size.setPlaceholderText(QCoreApplication.translate("LoadingScreen", u"sampling rate", None))
    # retranslateUi

