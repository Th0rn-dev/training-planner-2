# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(461, 328)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(9, 9, 57, 16))
        self.cmbCategory = QComboBox(Dialog)
        self.cmbCategory.setObjectName(u"cmbCategory")
        self.cmbCategory.setGeometry(QRect(9, 55, 69, 22))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(9, 83, 53, 16))
        self.titleEdit = QLineEdit(Dialog)
        self.titleEdit.setObjectName(u"titleEdit")
        self.titleEdit.setGeometry(QRect(9, 110, 439, 21))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(9, 157, 44, 16))
        self.linkImgEdit = QLineEdit(Dialog)
        self.linkImgEdit.setObjectName(u"linkImgEdit")
        self.linkImgEdit.setGeometry(QRect(9, 180, 371, 21))
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(9, 220, 93, 16))
        self.linkVideoEdit = QLineEdit(Dialog)
        self.linkVideoEdit.setObjectName(u"linkVideoEdit")
        self.linkVideoEdit.setGeometry(QRect(9, 240, 371, 21))
        self.addButton = QPushButton(Dialog)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setGeometry(QRect(280, 280, 75, 24))
        self.cancelButton = QPushButton(Dialog)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setGeometry(QRect(370, 280, 75, 24))
        self.addVideoButton = QPushButton(Dialog)
        self.addVideoButton.setObjectName(u"addVideoButton")
        self.addVideoButton.setGeometry(QRect(390, 240, 51, 21))
        self.addImageButton = QPushButton(Dialog)
        self.addImageButton.setObjectName(u"addImageButton")
        self.addImageButton.setGeometry(QRect(390, 180, 51, 21))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u041f\u0440\u0435\u0432\u044c\u044e", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0432\u0438\u0434\u0435\u043e", None))
        self.addButton.setText(QCoreApplication.translate("Dialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.cancelButton.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.addVideoButton.setText(QCoreApplication.translate("Dialog", u"Video", None))
        self.addImageButton.setText(QCoreApplication.translate("Dialog", u"Image", None))
    # retranslateUi

