# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'intro_loaderrQLuBr.ui'
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
        LoadingScreen.resize(680, 400)
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
        self.Title.setGeometry(QRect(10, 80, 651, 101))
        font = QFont()
        font.setFamily(u"Verdana")
        font.setPointSize(40)
        font.setBold(False)
        font.setWeight(50)
        self.Title.setFont(font)
        self.Title.setStyleSheet(u"color: rgb(235, 235, 235)")
        self.Title.setAlignment(Qt.AlignCenter)
        self.Subtitle = QLabel(self.dropShadowFrame)
        self.Subtitle.setObjectName(u"Subtitle")
        self.Subtitle.setGeometry(QRect(0, 170, 651, 31))
        font1 = QFont()
        font1.setFamily(u"Verdana")
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setWeight(50)
        self.Subtitle.setFont(font1)
        self.Subtitle.setStyleSheet(u"color:rgb(145, 155, 222)")
        self.Subtitle.setAlignment(Qt.AlignCenter)
        self.plux_logo = QLabel(self.dropShadowFrame)
        self.plux_logo.setObjectName(u"plux_logo")
        self.plux_logo.setGeometry(QRect(10, 330, 101, 41))
        self.plux_logo.setPixmap(QPixmap(u"images/plux_logo.png"))
        self.plux_logo.setScaledContents(True)
        self.nova_logo = QLabel(self.dropShadowFrame)
        self.nova_logo.setObjectName(u"nova_logo")
        self.nova_logo.setGeometry(QRect(120, 300, 131, 91))
        self.nova_logo.setPixmap(QPixmap(u"images/nova_logo.png"))
        self.nova_logo.setScaledContents(True)

        self.verticalLayout.addWidget(self.dropShadowFrame)

        LoadingScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoadingScreen)

        QMetaObject.connectSlotsByName(LoadingScreen)
    # setupUi

    def retranslateUi(self, LoadingScreen):
        LoadingScreen.setWindowTitle(QCoreApplication.translate("LoadingScreen", u"MainWindow", None))
        self.Title.setText(QCoreApplication.translate("LoadingScreen", u"<strong>Bio</strong>SoundScape", None))
        self.Subtitle.setText(QCoreApplication.translate("LoadingScreen", u"Making Sound", None))
        self.plux_logo.setText("")
        self.nova_logo.setText("")
    # retranslateUi

