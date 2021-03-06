# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from os import path
from PyQt5 import QtCore, QtGui, QtWidgets

from wordreader.scanner import find_in_files
from wordreader.strings_handler import trim_string


class Ui_MainWindow(object):
    def __init__(self):
        self.filenames = set()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Wordreader")
        MainWindow.resize(960, 540)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.filesLayout = QtWidgets.QVBoxLayout()
        self.filesLayout.setObjectName("filesLayout")
        self.filesView = QtWidgets.QListWidget(self.centralwidget)
        self.filesView.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.filesView.setFont(font)
        self.filesView.setObjectName("filesView")
        self.filesLayout.addWidget(self.filesView)
        self.addFilesBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.addFilesBtn.setFont(font)
        self.addFilesBtn.setObjectName("addFilesBtn")
        self.filesLayout.addWidget(self.addFilesBtn)
        self.clearBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.clearBtn.setFont(font)
        self.clearBtn.setObjectName("clearBtn")
        self.filesLayout.addWidget(self.clearBtn)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.filesLayout)
        self.textLayout = QtWidgets.QVBoxLayout()
        self.textLayout.setObjectName("textLayout")
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setObjectName("searchLayout")
        self.searchLine = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.searchLine.setFont(font)
        self.searchLine.setObjectName("searchLine")
        self.searchLayout.addWidget(self.searchLine)
        self.searchBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.searchBtn.setFont(font)
        self.searchBtn.setObjectName("searchBtn")
        self.searchShortcut = QtWidgets.QShortcut(
                QtGui.QKeySequence(QtCore.Qt.Key_Return), 
                self.searchBtn,
            )
        self.searchShortcut.activated.connect(self.search)
        self.searchLayout.addWidget(self.searchBtn)
        self.textLayout.addLayout(self.searchLayout)
        self.foundText = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.foundText.setFont(font)
        self.foundText.setUndoRedoEnabled(False)
        self.foundText.setReadOnly(True)
        self.foundText.setOverwriteMode(True)
        self.foundText.setObjectName("foundText")
        self.textLayout.addWidget(self.foundText)
        self.caseSensitive = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.caseSensitive.setFont(font)
        self.caseSensitive.setObjectName("caseSensitive")
        self.textLayout.addWidget(self.caseSensitive)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.textLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.searchBtn.clicked.connect(self.search)
        self.addFilesBtn.clicked.connect(self.add_files)
        self.clearBtn.clicked.connect(self.clear_files)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Wordreader", "Wordreader"))
        self.addFilesBtn.setText(_translate("Wordreader", "???????????????? ??????????"))
        self.clearBtn.setText(_translate("Wordreader", "????????????????"))
        self.searchBtn.setText(_translate("Wordreader", "????????????"))
        self.caseSensitive.setText(_translate("Wordreader", "?????????????????? ??????????????"))

    def search(self):
        search_word = self.searchLine.text()
        if not search_word:
            return
        search_result = find_in_files(
                search_word, 
                self.filenames,
                self.caseSensitive.isChecked(),
                )
        printed_text = ''
        for filename, lines in search_result.items():
            if not lines:
                continue
            printed_text += '?????????????? ?? ?????????? "{0}" (????????????????????: {1})\n'.format(
                    path.basename(filename), len(lines),
                )
            for line in lines:
                line = trim_string(line, line.find(search_word), 32, 32)
                printed_text += '...{0}...\n'.format(line)
            printed_text += '\n\n'
        self.foundText.setPlainText(printed_text)


    def add_files(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if dialog.exec_():
            filenames = dialog.selectedFiles()
            self.filenames = self.filenames.union(filenames)

            self.filesView.clear()
            for filename in self.filenames:
                self.filesView.addItem(path.basename(filename))

    def clear_files(self):
        self.filenames = set()
        self.filesView.clear()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
