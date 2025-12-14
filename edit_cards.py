from PySide6.QtCore import Qt, QModelIndex, QAbstractTableModel, Signal
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow, \
    QMessageBox
from sqlalchemy import select, update, insert

from models import Card, Category
from ui.edit_ui import Ui_MainWindow
from dialogs import EditCardDialog, UpdateCardDialog
from session import session


class ItemsModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.headers = ["Номер", "Название", "Ссылка не превью", "Ссылка на видео"]

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
                return f"{info.title}"
            if col == 2:
                return f"{info.preview_image_url}" or "empty"
            if col == 3:
                return f"{info.video_url}"
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole.UserRole):
        if not index.isValid() and role == Qt.ItemDataRole.UserRole:
            card = self.items[index.row()]
            col = index.column()
            if col == 1:
                card.title = value
            if col == 2:
                card.preview_image_url = value
            if col == 3:
                card.video_url = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def removeRow(self, row):
        if 0 <= row < len(self.items):
            self.items.pop(row)
            self.layoutChanged.emit()


class EditCardsWindow(QMainWindow):
    exitButtonClicked = Signal()

    def __init__(self):
        super(EditCardsWindow, self).__init__()
        self.categories = {}
        self.rows = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = ItemsModel()
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.load_catalog()
        self.load_cards()
        self.ui.comboBox.currentIndexChanged.connect(self.load_cards)
        self.ui.buttonAdd.clicked.connect(self.on_buttonAdd_click)
        self.ui.buttonRemove.clicked.connect(self.on_buttonRemove_click)
        self.ui.buttonEdit.clicked.connect(self.on_buttonEdit_click)
        self.ui.buttonExit.clicked.connect(self.on_buttonExit_click)

    def load_cards(self):
        self.ui.tableView.model().items.clear()
        category_id = self.ui.comboBox.currentData().id
        with session as s:
            query = select(Card).where(Card.category_id == category_id)
            result = s.execute(query)
            rows = result.scalars().all()
            for r in rows:
                self.rows.append(r)
            self.model.setItems(self.rows)

    def load_catalog(self):
        self.ui.comboBox.clear()
        self.categories = {}
        with session as s:
            # ToDo повторяющееся выборка категорий
            query = select(Category)
            result = s.execute(query)
            rows = result.scalars().all()
            for r in rows:
                self.categories[r.id] = r

        for category in self.categories.values():
            self.ui.comboBox.addItem(category.name, category)

    def on_buttonAdd_click(self):
        dialog = EditCardDialog(self.categories)
        result = dialog.exec()

        if result == 0:
            return
        data = dialog.get_data()

        with session as s:
            query = insert(Card)
            s.execute(query, data)
            s.commit()
        self.load_cards()

    def on_buttonRemove_click(self):
        selected = self.ui.tableView.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите карточку для удаления!")
            return

        row = selected[0].row()
        card_id = self.ui.tableView.model().items[row].id
        if not card_id:
            return

        result = QMessageBox.question(self, "Подтверждение",
                                      "Точно хотите удалить карточку?")
        if result == QMessageBox.StandardButton.No:
            return

        with session as s:
            card = self.rows[row]
            s.delete(card)
            s.commit()

        self.load_cards()

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

        dialog = UpdateCardDialog(self.categories, item)

        result = dialog.exec()
        if result == 0:
            return
        data = dialog.get_data()
        with session as s:
            query = update(Card).where(Card.id.in_([item.id]))
            s.execute(query, data)
            s.commit()
        self.load_cards()

    def on_buttonExit_click(self):
        self.exitButtonClicked.emit()
        self.close()


if __name__ == '__main__':
    print("Edit cards")
