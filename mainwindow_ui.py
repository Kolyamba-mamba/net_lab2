# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(958, 629)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setObjectName("mainLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.CalcBtn = QtWidgets.QPushButton(self.centralwidget)
        self.CalcBtn.setObjectName("CalcBtn")
        self.verticalLayout.addWidget(self.CalcBtn)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.queueLengthSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.queueLengthSpinBox.setObjectName("queueLengthSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.queueLengthSpinBox)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.inputStreamSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.inputStreamSpinBox.setObjectName("inputStreamSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inputStreamSpinBox)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.workStreamSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.workStreamSpinBox.setObjectName("workStreamSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.workStreamSpinBox)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.countRequestSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.countRequestSpinBox.setObjectName("countRequestSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.countRequestSpinBox)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.verticalLayout.addLayout(self.formLayout)
        self.mainLayout.addLayout(self.verticalLayout)
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.graphLayout.setObjectName("graphLayout")
        self.firstWdg = QtWidgets.QWidget(self.centralwidget)
        self.firstWdg.setObjectName("firstWdg")
        self.graphLayout.addWidget(self.firstWdg)
        self.secondWdg = QtWidgets.QWidget(self.centralwidget)
        self.secondWdg.setObjectName("secondWdg")
        self.graphLayout.addWidget(self.secondWdg)
        self.thirdWdg = QtWidgets.QWidget(self.centralwidget)
        self.thirdWdg.setObjectName("thirdWdg")
        self.graphLayout.addWidget(self.thirdWdg)
        self.mainLayout.addLayout(self.graphLayout)
        self.gridLayout.addLayout(self.mainLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 958, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.CalcBtn.setText(_translate("MainWindow", "Calculate"))
        self.label.setText(_translate("MainWindow", "Длина очереди"))
        self.label_2.setText(_translate("MainWindow", "Интенсивность входного потока"))
        self.label_3.setText(_translate("MainWindow", "Интенсивность обслуживания"))
        self.label_4.setText(_translate("MainWindow", "Количество требований"))
        self.label_5.setText(_translate("MainWindow", "Закон поступления"))
        self.label_6.setText(_translate("MainWindow", "Закон обслуживания"))


