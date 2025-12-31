# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_catalog_dialog.ui'
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
        Dialog.resize(400, 250)
        self.titleEdit = QLineEdit(Dialog)
        self.titleEdit.setObjectName(u"titleEdit")
        self.titleEdit.setGeometry(QRect(9, 120, 381, 22))
        self.cancelButton = QPushButton(Dialog)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setGeometry(QRect(310, 190, 75, 24))
        self.addButton = QPushButton(Dialog)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setGeometry(QRect(210, 190, 75, 24))
        self.labelTitleCategory = QLabel(Dialog)
        self.labelTitleCategory.setObjectName(u"labelTitleCategory")
        self.labelTitleCategory.setGeometry(QRect(10, 90, 72, 16))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTitleCategory.sizePolicy().hasHeightForWidth())
        self.labelTitleCategory.setSizePolicy(sizePolicy)
        self.labelParentCategory = QLabel(Dialog)
        self.labelParentCategory.setObjectName(u"labelParentCategory")
        self.labelParentCategory.setGeometry(QRect(10, 20, 175, 18))
        self.assignParentCategory = QComboBox(Dialog)
        self.assignParentCategory.setObjectName(u"assignParentCategory")
        self.assignParentCategory.setGeometry(QRect(10, 50, 381, 26))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044e", None))
        self.cancelButton.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.addButton.setText(QCoreApplication.translate("Dialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.labelTitleCategory.setText(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.labelParentCategory.setText(QCoreApplication.translate("Dialog", u"\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0430\u044f \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f", None))
    # retranslateUi

