from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6 import QtWidgets
from sqlalchemy import select, insert, update

from models import Category
from ui.edit_catalog_ui import Ui_MainWindow
from session import session
from dialogs import EditCatalogDialog, UpdateCatalogDialog


class ItemsModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def setItems(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def rowCount(self, *args, **kwargs) -> int:
        return len(self.items)

    def columnCount(self, *args, **kwargs) -> int:
        return 2

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt.ItemDataRole):
        if not index.isValid():
            return

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            info = self.items[index.row()]
            col = index.column()
            if col == 0:
                return f"{index.row() + 1}"
            if col == 1:
                return f"{info.name}"

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation,
                   role: QtCore.Qt.ItemDataRole):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return {
                    0: "Id",
                    1: "Название категории"
                }.get(section)


class EditCatalogWindow(QMainWindow):
    exitButtonClicked = QtCore.Signal()

    def __init__(self):
        super(EditCatalogWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = ItemsModel()
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)

        self.ui.buttonAdd.clicked.connect(self.on_buttonAdd_click)
        self.ui.buttonRemove.clicked.connect(self.on_buttonRemove_click)
        self.ui.buttonEdit.clicked.connect(self.on_buttonEdit_click)
        self.ui.buttonExit.clicked.connect(self.on_buttonExit_click)
        self.rows = []

        self.load_catalog()

    def load_catalog(self):
        self.ui.tableView.model().items.clear()
        self.categories = {}
        with session as s:
            query = select(Category)
            result = s.execute(query)
            rows = result.scalars().all()
            for r in rows:
                self.categories[r.id] = r

        for category in self.categories.values():
            self.rows.append(category)
        self.model.setItems(self.rows)

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
            query = insert(Category)
            s.execute(query, data)
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

        with session as s:
            query = update(Category).where(Category.id.in_([init_data.id]))
            s.execute(query, data)
            s.commit()
        self.load_catalog()


if __name__ == '__main__':
    print("Edit catalog")
