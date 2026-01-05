import sys

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, \
    QPushButton, QLabel, QGridLayout, QScrollArea, QMenu, \
    QMenuBar, QTreeView
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize, QAbstractItemModel, QModelIndex

from edit_cards import EditCardsWindow
from edit_catalog import EditCatalogWindow
from models import Card, Category
from player import Player
from session import session

class CategoryTreeModel(QAbstractItemModel):
    def __init__(self, root_categories=None, parent=None):
        super().__init__(parent)
        self.root_items = root_categories or []

    def columnCount(self, parent=QModelIndex()):
        return 1

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            parent_item = parent.internalPointer()
            return len(parent_item.children)
        return len(self.root_items)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            item = index.internalPointer()
            return item.name
        return None

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if parent.isValid():
            parent_item = parent.internalPointer()
            child_item = parent_item.children[row]
        else:
            child_item = self.root_items[row]

        return self.createIndex(row, column, child_item)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        item = index.internalPointer()
        if item.parent is None:
            return QModelIndex()

        # Находим индекс родителя в его родительском списке
        parent_item = item.parent
        if parent_item.parent is None:
            row = self.root_items.index(parent_item)
        else:
            row = parent_item.parent.children.index(parent_item)

        return self.createIndex(row, 0, parent_item)


    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return super().flags(index) & ~Qt.ItemFlag.ItemIsEditable

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            item = index.internalPointer()
            item.name = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def addCategory(self, category, parent_index=QModelIndex()):
        parent_item = parent_index.internalPointer() if parent_index.isValid() else None

        if parent_item:
            parent_item.children.append(category)
        else:
            self.root_items.append(category)

        self.layoutChanged.emit()

    def removeCategory(self, index):
        item = index.internalPointer()
        parent = item.parent

        if parent:
            parent.children.remove(item)
        else:
            self.root_items.remove(item)

        self.layoutChanged.emit()

    def getCategory(self, index):
        if index.isValid():
            return index.internalPointer()
        return None


class MainWindow(QWidget):

    PATH_PLAY_ICON = "./images/play.png"
    PATH_BLANK_IMG = "./images/blank.png"

    def __init__(self):
        super().__init__()
        self.categories = {}
        self.opened_windows = []

        self.setWindowTitle("Планировщик тренировок")
        self.setGeometry(100, 100, 900, 700)

        self.menuBar = QMenuBar()
        self.addCardMenu = QMenu("Редактирование")
        self.menuBar.addMenu(self.addCardMenu)
        self.addCardMenu.addAction("Карточки", self.edit_menu_cards)
        self.addCardMenu.addAction("Категории", self.edit_menu_categories)

        self.layout = QHBoxLayout()
        # Список категорий
        self.category = QTreeView(self)
        self.category.setHeaderHidden(True)
        self.category.setSelectionMode(QTreeView.SingleSelection)
        self.category.setSelectionBehavior(QTreeView.SelectRows)
        self.category.setMaximumWidth(250)
        self.category_model = CategoryTreeModel(self)
        self.category.setModel(self.category_model)
        self.layout.addWidget(self.category)
        self.category.clicked.connect(self.load_cards)

        self.scroll_area = QScrollArea(self)
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)

        self.layout.addWidget(self.scroll_area)
        self.layout.setMenuBar(self.menuBar)
        self.setLayout(self.layout)

        self.play_icon = QIcon(self.PATH_PLAY_ICON)

        self.load_categories()
        self.load_cards()

    def load_cards(self):
        current_index = self.category.currentIndex()
        if current_index.isValid():
            category_id = current_index.internalPointer().id
        else:
            category_id = session.query(Category).first().id

        self.clear_layout(self.grid_layout)
        cards = session.query(Card).filter(Card.category_id == category_id, Card.invisible != True).all()
        row = 0
        col = 0
        for card in cards:
            title = QLabel(card.title)
            title.setAlignment(Qt.AlignCenter)
            preview = QLabel()
            pixmap = QPixmap( card.preview_image_url or self.PATH_BLANK_IMG)

            preview.setPixmap(
                pixmap.scaled(150, 150, Qt.AspectRatioMode.IgnoreAspectRatio))
            preview.setAlignment(Qt.AlignCenter)
            preview.setToolTip(card.description)

            button = QPushButton()
            button.setIcon(self.play_icon)
            button.clicked.connect(lambda checked, title=card.title,
                                          video_url=card.video_url: self.open_video(title, video_url))
            button.setMaximumWidth(50)
            button.setIconSize(QSize(40, 20))
            button.setFlat(True)
            self.grid_layout.addWidget(title, row, col)
            self.grid_layout.addWidget(preview, row + 1, col)
            self.grid_layout.addWidget(button, row + 2, col)

            col += 1
            if col == 3:
                col = 0
                row += 3

    def load_categories(self):
        self.categories = {}
        categories = session.query(Category).all()
        root_categories = [cat for cat in categories if cat.parent_id is None]
        for category in categories:
            self.categories[category.id] = category.name
            self._build_children(category, categories)
        # Обновляем модель
        self.category_model = CategoryTreeModel(root_categories)
        self.category.setModel(self.category_model)
        self.category.expandAll()

    def _build_children(self, parent, categories):
        """Рекурсивно собираем все категории"""
        children = [cat for cat in categories if cat.parent_id == parent.id]
        parent.children = children
        for child in children:
            self._build_children(child, categories)

    def open_video(self, title, video_url):
        self.player = Player()
        self.player.setWindowTitle(title)
        self.player.player.setSource(video_url)
        self.player.show()
        self.player.player.play()
        self.opened_windows.append(self.player)

    def closeEvent(self, event):
        for window in self.opened_windows:
            window.close()
        event.accept()

    def edit_menu_cards(self):
        self.edit_card = EditCardsWindow()
        self.edit_card.exitButtonClicked.connect(self.on_exitButton_click)
        self.edit_card.show()
        self.opened_windows.append(self.edit_card)

    def edit_menu_categories(self):
        self.edit_categories = EditCatalogWindow()
        self.edit_categories.exitButtonClicked.connect(self.on_exitButton_click)
        self.edit_categories.show()
        self.opened_windows.append(self.edit_categories)

    def on_exitButton_click(self):
        #ToDo тут еще надо понимать из какой категории пришли или
        # в какую добавили, на той и открыть карточки в основном окне
        # (логично сразу увидеть результат добавления, может быть что-то нужно будет поправить)
        self.load_categories()
        self.load_cards()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())
            layout.removeItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
