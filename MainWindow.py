# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import  QMainWindow
import main


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(411, 395)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dltRadioBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.dltRadioBtn.setGeometry(QtCore.QRect(30, 230, 82, 21))
        self.dltRadioBtn.setObjectName("dltRadioBtn")
        self.ndltRadioBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.ndltRadioBtn.setGeometry(QtCore.QRect(130, 230, 121, 21))
        self.ndltRadioBtn.setObjectName("ndltRadioBtn")
        self.ndltRadioBtn.setChecked(True)
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(290, 300, 111, 31))
        self.startBtn.setObjectName("startBtn")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 411, 151))
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.openImgBtn = QtWidgets.QPushButton(self.centralwidget)
        self.openImgBtn.setGeometry(QtCore.QRect(290, 230, 111, 31))
        self.openImgBtn.setObjectName("openImgBtn")
        self.widthLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.widthLineEdit.setGeometry(QtCore.QRect(20, 310, 113, 20))
        self.widthLineEdit.setText("")
        self.widthLineEdit.setObjectName("widthLineEdit")
        self.heightLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.heightLineEdit.setGeometry(QtCore.QRect(150, 310, 113, 20))
        self.heightLineEdit.setObjectName("heightLineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 290, 111, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(150, 290, 111, 16))
        self.label_3.setObjectName("label_3")
        self.pathLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.pathLineEdit.setGeometry(QtCore.QRect(20, 180, 371, 20))
        self.pathLineEdit.setObjectName("pathLineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 411, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        # putanja ucitane slike
        self.path = ""

        # Handlovanje dogadjaja
        self.openImgBtn.clicked.connect(self.open_image)
        self.startBtn.clicked.connect(self.execute_image_transformation)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.dltRadioBtn.setText(_translate("MainWindow", "DLT"))
        self.ndltRadioBtn.setText(_translate("MainWindow", "Modifikovani DLT"))
        self.startBtn.setText(_translate("MainWindow", "Pokreni "))
        self.openImgBtn.setText(_translate("MainWindow", "Izaberi sliku"))
        self.label_2.setText(_translate("MainWindow", "Unesite sirinu"))
        self.label_3.setText(_translate("MainWindow", "Unesite visinu"))


    def open_image(self):
        self.path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open image")
        try:
            self.label.setPixmap(QPixmap(self.path))
            self.pathLineEdit.setText(self.path)
        except IOError:
            self.pathLineEdit.setText("Nije izabran nijedan fajl")

    def execute_image_transformation(self):
        try:
            algorithm = "mdlt" if self.ndltRadioBtn.isChecked() else "dlt"
            if self.widthLineEdit.text() == "" or self.heightLineEdit.text() == "":
                main.img_transformation(self.path, algorithm)
            else:
                main.img_transformation(self.path,
                                        algorithm,
                                        int(self.widthLineEdit.text()),
                                        int(self.heightLineEdit.text()))
        except ValueError as err:
            self.pathLineEdit.setText("Nepravilno uneti podaci")
        except Exception as e:
            self.pathLineEdit.setText("Nije izabrana slika")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
