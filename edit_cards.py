from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QListWidgetItem, \
    QMessageBox
from sqlalchemy import select, update, insert

from models import Card, Category
from ui.edit_ui import Ui_MainWindow
from dialogs import EditCardDialog, UpdateCardDialog
from session import session


class EditCardsWindow(QMainWindow):
    exitButtonClicked = QtCore.Signal()

    def __init__(self):
        super(EditCardsWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_catalog()
        self.load_cards()
        self.ui.comboBox.currentIndexChanged.connect(self.load_cards)
        self.ui.buttonAdd.clicked.connect(self.on_buttonAdd_click)
        self.ui.buttonRemove.clicked.connect(self.on_buttonRemove_click)
        self.ui.buttonEdit.clicked.connect(self.on_buttonEdit_click)
        self.ui.buttonExit.clicked.connect(self.on_buttonExit_click)

    def load_cards(self):
        category_id = self.ui.comboBox.currentData().id
        self.ui.listWidget.clear()

        with session as s:
            query = select(Card).where(Card.category_id == category_id)
            result = s.execute(query)
            rows = result.scalars().all()
            for r in rows:
                category_name = self.categories[r.category_id].name
                item = QListWidgetItem(
                    f"{r.id}  {r.title}  {r.preview_image_url or 'empty'} "
                    f"{r.video_url} {category_name}")
                item.setData(QtCore.Qt.ItemDataRole.UserRole, r)
                self.ui.listWidget.addItem(item)

    def load_catalog(self):
        self.ui.comboBox.clear()
        self.categories = {}
        with session as s:
            #ToDo повторяющееся выборка категорий
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
        item = self.ui.listWidget.currentItem()
        card = item.data(QtCore.Qt.ItemDataRole.UserRole)

        result = QMessageBox.question(self, "Подтверждение",
                                      "Точно хотите удалить карточку?")

        if result == QMessageBox.StandardButton.No:
            return

        with session as s:
            s.delete(card)
            s.commit()

        self.load_cards()

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
        dialog = UpdateCardDialog(self.categories, init_data)
        result = dialog.exec()
        if result == 0:
            return
        data = dialog.get_data()
        with session as s:
            query = update(Card).where(Card.id.in_([init_data.id]))
            s.execute(query, data)
            s.commit()
        self.load_cards()

    def on_buttonExit_click(self):
        self.exitButtonClicked.emit()
        self.close()


if __name__ == '__main__':
    print("Edit cards")
