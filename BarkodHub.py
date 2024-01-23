from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import cv2
from pyzbar.pyzbar import decode
import sqlite3

# Global variable to store barcode data
barcodeData = ""

def database():
    con = sqlite3.connect("SQLiteTrial.db")
    cursor = con.cursor()

    def create_table():
        cursor.execute("CREATE TABLE IF NOT EXISTS library (barcode INTEGER, name TEXT, description TEXT)")
        con.commit()

    create_table()

    def add_data(barcode, name, description):
        cursor.execute("INSERT INTO library VALUES(?,?,?)", (barcode, name, description))
        con.commit()

    barcode = int(input("Barcode: "))
    name = input("Name: ")
    description = input("Description: ")

    add_data(barcode, name, description)


def camera():
    global barcodeData  # Use the global variable
    barcode_list = []
    b = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        success, img = cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode("utf-8")
            print(myData)
            barcode_list.append(myData)
            barcodeData = str(myData)
            print(barcodeData)

            if len(barcode_list) >= 1:
                b = 1
                break

        cv2.imshow("Camera", img)
        if b == 1:
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


class Ui_Project():
    def setupUi(self, Project):
        Project.setObjectName("Project")
        Project.resize(1000, 775)

        self.tableWidget = QtWidgets.QTableWidget(Project)
        self.tableWidget.setGeometry(QtCore.QRect(460, 50, 431, 421))
        self.tableWidget.setRowCount(30)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")

        self.widget = QtWidgets.QWidget(Project)
        self.widget.setGeometry(QtCore.QRect(80, 510, 821, 131))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.btnQuery = QtWidgets.QPushButton(self.widget)
        self.btnQuery.setObjectName("btnQuery")
        self.btnQueryP = BtnQueryP()
        self.btnQuery.clicked.connect(self.btnQueryP.show)
        self.horizontalLayout.addWidget(self.btnQuery)

        self.btnAdd = QtWidgets.QPushButton(self.widget)
        self.btnAdd.setObjectName("btnAdd")
        self.btnAddP = BtnAddP()
        self.btnAdd.clicked.connect(self.btnAddP.show)
        self.horizontalLayout.addWidget(self.btnAdd)

        self.btnDelete = QtWidgets.QPushButton(self.widget)
        self.btnDelete.setObjectName("btnDelete")
        self.btnDeleteP = BtnDeleteP()
        self.btnDelete.clicked.connect(self.btnDeleteP.show)
        self.horizontalLayout.addWidget(self.btnDelete)

        self.retranslateUi(Project)
        QtCore.QMetaObject.connectSlotsByName(Project)

    def retranslateUi(self, Project):
        _translate = QtCore.QCoreApplication.translate
        Project.setWindowTitle(_translate("Project", "Project"))
        self.btnQuery.setText(_translate("Project", "Query Barcode"))
        self.btnAdd.setText(_translate("Project", "Add Barcode"))
        self.btnDelete.setText(_translate("Project", "Delete Barcode"))


class BtnQueryP(QtWidgets.QDialog):
    def __init__(self):
        super(BtnQueryP, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("Query Barcode")


class BtnAddP(QtWidgets.QDialog):
    def __init__(self):
        super(BtnAddP, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("Add Barcode")

        self.h_box = QtWidgets.QHBoxLayout(self)

        cameraBtn = self.pushButton = QtWidgets.QPushButton(self)
        cameraBtn.setText("Camera")
        cameraBtn.clicked.connect(self.clickCamera)
        self.h_box.addWidget(cameraBtn)

        saveBtn = self.pushButton = QtWidgets.QPushButton(self)
        saveBtn.setText("Save")
        self.h_box.addWidget(saveBtn)

        self.line = QtWidgets.QLineEdit(self)
        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.line.setText(barcodeData)

    def clickCamera(self):
        camera()


class BtnDeleteP(QtWidgets.QDialog):
    def __init__(self):
        super(BtnDeleteP, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("Delete Barcode")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Project = QtWidgets.QDialog()
    ui = Ui_Project()
    ui.setupUi(Project)
    Project.show()
    sys.exit(app.exec_())
