import sys

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, \
    QPushButton, QLabel, QGridLayout, QScrollArea, QListWidget, QMenu, \
    QMenuBar, QListWidgetItem
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize

from edit_cards import EditCardsWindow
from edit_catalog import EditCatalogWindow
from models import Card, Category
from player import Player
from session import session


class MainWindow(QWidget):

    PATH_PLAY_ICON = "./images/play.png"
    PATH_BLANK_IMG = "./images/blank.png"

    def __init__(self):
        super().__init__()
        self.categories = {}
        self.opened_windows = []

        self.setWindowTitle("Планировщик тренировок")
        self.setGeometry(100, 100, 800, 600)

        self.menuBar = QMenuBar()
        self.addCardMenu = QMenu("Редактирование")
        self.menuBar.addMenu(self.addCardMenu)
        self.addCardMenu.addAction("Карточки", self.edit_menu_cards)
        self.addCardMenu.addAction("Категории", self.edit_menu_categories)

        self.layout = QHBoxLayout()
        # Список категорий
        self.category = QListWidget(self)
        self.category.setMaximumWidth(180)

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
        category_id = None
        current_row = self.category.currentItem()

        if not current_row:
            category_id = session.query(Category).first().id
        else:
            data = current_row.data(Qt.DisplayRole)
            for key in self.categories.keys():
                if data in self.categories[key]:
                    category_id = key
                    break

        self.clear_layout(self.grid_layout)
        cards = session.query(Card).filter(Card.category_id == category_id).all()
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
        self.category.clear()
        categories = session.query(Category).all()
        for category in categories:
            self.categories[category.id] = category.name
            item = QListWidgetItem(f"{category.name}")
            item.setData(Qt.ItemDataRole.UserRole, category)
            self.category.addItem(item)


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
