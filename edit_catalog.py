from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem
from sqlalchemy import select, insert, update

from models import Category
from ui.edit_catalog_ui import Ui_MainWindow
from session import session
from dialogs import EditCatalogDialog, UpdateCatalogDialog


class EditCatalogWindow(QMainWindow):
    exitButtonClicked = QtCore.Signal()

    def __init__(self):
        super(EditCatalogWindow, self).__init__()
        self.categories = {}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.buttonAdd.clicked.connect(self.on_buttonAdd_click)
        self.ui.buttonRemove.clicked.connect(self.on_buttonRemove_click)
        self.ui.buttonEdit.clicked.connect(self.on_buttonEdit_click)
        self.ui.buttonExit.clicked.connect(self.on_buttonExit_click)

        self.load_catalog()

    def load_catalog(self):
        self.ui.listWidget.clear()
        self.categories = {}
        with session as s:
            query = select(Category)
            result = s.execute(query)
            rows = result.scalars().all()
            for r in rows:
                self.categories[r.id] = r

        for category in self.categories.values():
            item = QListWidgetItem()
            item.setText(category.name)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, category)
            self.ui.listWidget.addItem(item)

    def on_buttonExit_click(self):
        # пульнуть главному окну сигнал обновить контент
        self.exitButtonClicked.emit()
        self.close()

    def on_buttonAdd_click(self):
        dialog = EditCatalogDialog()
        result = dialog.exec()

        if result == 0:
            return
        data = dialog.get_data()

        with session as s:
            query = insert(Category).values(name = data["name"])
            s.execute(query)
            s.commit()
        self.load_catalog()

    def on_buttonRemove_click(self):
        item = self.ui.listWidget.currentItem()
        data = item.data(QtCore.Qt.ItemDataRole.UserRole)
        result = (QMessageBox
                  .question(self, "Подтверждение",
                            "Точно ли хотите удалить пункт категории?"))

        if result == QMessageBox.StandardButton.No:
            return

        with session as s:
            session.delete(data)
            s.commit()

        self.load_catalog()

    def on_buttonEdit_click(self):
        item = self.ui.listWidget.currentItem()
        if not item:
            QMessageBox.warning(
                self,
                "Редактирование карточки",
                "Не выбрано ни одной карточки",
                QMessageBox.StandardButton.Yes
            )
            return
        init_data = item.data(QtCore.Qt.ItemDataRole.UserRole)
        dialog = UpdateCatalogDialog(init_data)
        result = dialog.exec()
        if result == 0:
            return
        data = dialog.get_data()

        with (session as s):
            query = update(Category).where(Category.id.in_([init_data.id])).values(name=data["name"])
            s.execute(query)
            s.commit()
        self.load_catalog()


if __name__ == '__main__':
    print("Edit catalog")
