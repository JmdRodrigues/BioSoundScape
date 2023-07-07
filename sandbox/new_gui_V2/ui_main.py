# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainhHAbRw.ui'
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
        MainWindow.resize(1358, 1050)
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
        self.graphBiosignalThumbnail = QWidget(self.frame)
        self.graphBiosignalThumbnail.setObjectName(u"graphBiosignalThumbnail")
        self.graphBiosignalThumbnail.setGeometry(QRect(990, 60, 291, 150))
        self.graphSound = QWidget(self.frame)
        self.graphSound.setObjectName(u"graphSound")
        self.graphSound.setGeometry(QRect(120, 230, 841, 141))
        self.graphSpectral = QWidget(self.frame)
        self.graphSpectral.setObjectName(u"graphSpectral")
        self.graphSpectral.setGeometry(QRect(120, 400, 841, 381))
        self.graphBiosignal = QWidget(self.frame)
        self.graphBiosignal.setObjectName(u"graphBiosignal")
        self.graphBiosignal.setGeometry(QRect(120, 60, 841, 150))
        self.graphAudio_Thumbnail = QWidget(self.frame)
        self.graphAudio_Thumbnail.setObjectName(u"graphAudio_Thumbnail")
        self.graphAudio_Thumbnail.setGeometry(QRect(990, 230, 291, 141))

        self.verticalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1358, 21))
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
    # retranslateUi

