# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog


class PromptWindow(QDialog):
    def __init__(self):
        self.setupUi(self)

    def setupUi(self, Form):
        super(PromptWindow, self).__init__()
        self.decision = True
        self.New_Name = None
        Form.setObjectName("Form")
        Form.resize(350, 164)
        Form.setStyleSheet("QWidget {\n"
                           "   background-color: #383c41;\n"
                           "}\n"
                           "\n"
                           "QTextEdit {\n"
                           "   background-color: aliceblue;\n"
                           "   color: #618b38;\n"
                           "   font-style: italic;\n"
                           "   font-weight: bold;\n"
                           "}\n"
                           "\n"
                           "QLabel {\n"
                           "   background-color: #383c41;\n"
                           "   color: #FFA500;\n"
                           "}\n"
                           "\n"
                           "QPushButton {\n"
                           "   background-color: #FFA500;\n"
                           "   color: #ffffff;\n"
                           "   border-radius: 5px;\n"
                           "   border-style: none;\n"
                           "   height: 25px;\n"
                           "}\n"
                           "QGroupBox {\n"
                           "    color:#ffffff;\n"
                           "}\n"
                           "QComboBox{\n"
                           "   color: #FFA500;\n"
                           "}\n"
                           "\n"
                           "QTabBar::tab{\n"
                           "    color:#ffffff;\n"
                           "}\n"
                           "\n"
                           "QRadioButton{\n"
                           "    color:#ffffff\n"
                           "}\n"
                           )
        self.Btn_Ok = QtWidgets.QPushButton(Form)
        self.Btn_Ok.setGeometry(QtCore.QRect(130, 130, 80, 21))
        self.Btn_Ok.setObjectName("Btn_Ok")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 311, 91))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.RadioButton_Yes = QtWidgets.QRadioButton(self.groupBox)
        self.RadioButton_Yes.setGeometry(QtCore.QRect(10, 30, 151, 20))
        self.RadioButton_Yes.setObjectName("RadioButton_Yes")
        self.RadioButton_Create_New = QtWidgets.QRadioButton(self.groupBox)
        self.RadioButton_Create_New.setGeometry(QtCore.QRect(10, 60, 141, 20))
        self.RadioButton_Create_New.setObjectName("RadioButton_Create_New")
        self.textEdit_New_Profile_Name = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_New_Profile_Name.setGeometry(QtCore.QRect(160, 60, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.textEdit_New_Profile_Name.setFont(font)
        self.textEdit_New_Profile_Name.setObjectName("textEdit_New_Profile_Name")
        self.Btn_Ok.clicked.connect(self.accept)
        self.RadioButton_Yes.setChecked(True)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Btn_Ok.setText(_translate("Form", "Ok"))
        self.groupBox.setTitle(_translate("Form", "Want to overwrite current profile?"))
        self.RadioButton_Yes.setText(_translate("Form", "Yes"))
        self.RadioButton_Create_New.setText(_translate("Form", "No, Create a new profile"))
        self.textEdit_New_Profile_Name.setPlaceholderText(_translate("Form", "New Profile Name"))
