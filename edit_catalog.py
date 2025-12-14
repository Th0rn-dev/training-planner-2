from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtWidgets import QMainWindow, QMessageBox, QAbstractItemView
from PySide6 import QtWidgets
from sqlalchemy import select, insert, update

from models import Category
from ui.edit_catalog_ui import Ui_MainWindow
from session import session
from dialogs import EditCatalogDialog, UpdateCatalogDialog


class ItemsModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.headers = ["Номер", "Название категории"]

    def setItems(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def rowCount(self, *args, **kwargs) -> int:
        return len(self.items)

    def columnCount(self, *args, **kwargs) -> int:
        return len(self.headers)

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            info = self.items[index.row()]
            col = index.column()
            if col == 0:
                return f"{index.row() + 1}"
            if col == 1:
                return f"{info.name}"

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
                return self.headers[section]

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole.EditRole):
        if not index.isValid() and role == Qt.ItemDataRole.EditRole:
            category = self.items[index.row()]
            col = index.column()
            if col == 1:
                category.name = value
            return True
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable


    def removeRows(self, row):
        if 0 <= row < len(self.items):
            self.items.pop(row)
            self.layoutChanged.emit()


class EditCatalogWindow(QMainWindow):
    exitButtonClicked = Signal()

    def __init__(self):
        super(EditCatalogWindow, self).__init__()
        self.categories = {}
        self.rows = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = ItemsModel()
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.buttonAdd.clicked.connect(self.on_buttonAdd_click)
        self.ui.buttonRemove.clicked.connect(self.on_buttonRemove_click)
        self.ui.buttonEdit.clicked.connect(self.on_buttonEdit_click)
        self.ui.buttonExit.clicked.connect(self.on_buttonExit_click)
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
        selected = self.ui.tableView.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для удаления!")
            return

        row = selected[0].row()
        category_id = self.ui.tableView.model().items[row].id
        if not category_id:
            return

        result = (QMessageBox
                  .question(self, "Подтверждение",
                            "Точно ли хотите удалить пункт категории?"))
        if result == QMessageBox.StandardButton.No:
            return

        with session as s:
            category = self.categories[category_id]
            s.delete(category)
            s.commit()
        self.load_catalog()

    def on_buttonEdit_click(self):
        selected = self.ui.tableView.selectedIndexes()

        if not selected:
            QMessageBox.warning(
                self,
                "Редактирование карточки",
                "Не выбрано ни одной карточки",
                QMessageBox.StandardButton.Yes
            )
            return

        row = selected[0].row()
        item = self.ui.tableView.model().items[row]
        if not item:
            return

        dialog = UpdateCatalogDialog(item)
        result = dialog.exec()
        if result == 0:
            return

        data = dialog.get_data()
        with session as s:
            query = update(Category).where(Category.id.in_([item.id]))
            s.execute(query, data)
            s.commit()
        self.load_catalog()


if __name__ == '__main__':
    print("Edit catalog")
