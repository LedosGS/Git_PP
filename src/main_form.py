# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QCheckBox, QLabel,
    QMainWindow, QMenuBar, QSizePolicy, QSlider,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(873, 543)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(30, 80, 541, 401))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ph = QCheckBox(self.verticalLayoutWidget)
        self.ph.setObjectName(u"ph")
        font = QFont()
        font.setPointSize(22)
        self.ph.setFont(font)

        self.verticalLayout.addWidget(self.ph)

        self.checkBox_3 = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setFont(font)

        self.verticalLayout.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setFont(font)

        self.verticalLayout.addWidget(self.checkBox_4)

        self.checkBox_5 = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setFont(font)

        self.verticalLayout.addWidget(self.checkBox_5)

        self.checkBox_6 = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setFont(font)

        self.verticalLayout.addWidget(self.checkBox_6)

        self.checkBox_8 = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_8.setObjectName(u"checkBox_8")
        self.checkBox_8.setFont(font)

        self.verticalLayout.addWidget(self.checkBox_8)

        self.checkBox_7 = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setFont(font)

        self.verticalLayout.addWidget(self.checkBox_7)

        self.checkBox_2 = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setFont(font)

        self.verticalLayout.addWidget(self.checkBox_2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 20, 461, 61))
        font1 = QFont()
        font1.setPointSize(22)
        font1.setBold(True)
        font1.setItalic(True)
        font1.setUnderline(True)
        self.label.setFont(font1)
        self.calendarWidget = QCalendarWidget(self.centralwidget)
        self.calendarWidget.setObjectName(u"calendarWidget")
        self.calendarWidget.setGeometry(QRect(600, 70, 256, 411))
        self.verticalSlider = QSlider(self.centralwidget)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setGeometry(QRect(580, 80, 22, 401))
        self.verticalSlider.setOrientation(Qt.Orientation.Vertical)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 873, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ph.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0438\u043b\u043e\u0441\u043e\u0444\u0438\u044f", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u0442\u043e\u0440\u0438\u044f", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043a\u043b\u0430\u0434\u043d\u043e\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0422\u0426\u041f", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0438\u0444\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0435 \u0443\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u044f", None))
        self.checkBox_8.setText(QCoreApplication.translate("MainWindow", u"\u0410\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a", None))
        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043e\u0440\u0438\u044f \u0441\u0438\u0441\u0442\u0435\u043c \u0438 \u0441\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0439 \u0430\u043d\u0430\u043b\u0438\u0437", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u0442\u0435\u0445\u043d\u0438\u043a\u0430", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0438\u0441\u043e\u043a \u0434\u043e\u043c\u0430\u0448\u043d\u0435\u0433\u043e \u0437\u0430\u0434\u0430\u043d\u0438\u044f", None))
    # retranslateUi

