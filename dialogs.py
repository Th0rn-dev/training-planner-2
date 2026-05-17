import os.path
import shutil

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox, QLineEdit

from constants import PATH_VIDEO, PATH_IMAGES, PATH_BLANK_IMG
from player import Player
from ui.edit_dialog_ui import Ui_Dialog as Ui_EditCardDialog
from ui.edit_catalog_dialog_ui import Ui_Dialog as Ui_EditCatalogDialog
from utils import dir_scan, now_formated


class EditCardDialog(QDialog):
    """Диалог добавления карточки"""

    def __init__(self, categories, current_category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_image = None
        self.categories = categories
        self.current_category = current_category
        self.opened_windows = []
        self.player = None
        self.ui = Ui_EditCardDialog()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)
        self.ui.addVideoButton.clicked.connect(self.add_video_file)
        self.ui.addImageButton.clicked.connect(self.add_img_file)
        self.ui.labelForPreview.setPixmap(QPixmap(PATH_BLANK_IMG))
        self.ui.playButton.clicked.connect(lambda checked: self.open_player())
        self.ui.closeButton.clicked.connect(self.close_player)

        for c in self.categories.values():
            self.ui.cmbCategory.addItem(c.name, c)

        if current_category is not None:
            name = self.categories[self.current_category].name
            index = self.ui.cmbCategory.findText(name)
            if index > -1:
                self.ui.cmbCategory.setCurrentIndex(index)

    def get_data(self):
        return {
            "title": self.ui.titleEdit.text(),
            "preview_image_url": self.ui.linkImgEdit.text(),
            "video_url": self.ui.linkVideoEdit.text(),
            "category_id": self.ui.cmbCategory.currentData().id,
            "invisible": self.ui.checkBox.isChecked(),
            "description": self.ui.descriptionEdit.toPlainText(),
        }

    def add_video_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open Video File', "",
                                              'Media Files (*.mp4 *.mkv *.amv *.m4v *.mov)')
        self.validate_not_empty(path, self.ui.linkVideoEdit)
        file_name = os.path.basename(path)
        now = now_formated()
        dir_list = dir_scan(PATH_VIDEO)
        video_dir = os.path.join(PATH_VIDEO, now)
        if now not in dir_list:
            os.makedirs(video_dir)
        full_path = os.path.join(video_dir, file_name)
        shutil.copy(path, full_path)
        self.ui.linkVideoEdit.setText(full_path.replace("\\", "/"))

    def add_img_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', "",
                                              'Media Files (*.jpg *.jpeg *.png *.gif)')
        self.validate_not_empty(path, self.ui.linkImgEdit)
        file_name = os.path.basename(path)
        self.original_image = QPixmap(path)
        cropped_size = QSize(150, 150)
        scaled = self.original_image.scaled(
            cropped_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        now = now_formated()
        dir_list = dir_scan(PATH_IMAGES)
        image_dir = os.path.join(PATH_IMAGES, now)
        if now not in dir_list:
            os.makedirs(image_dir)
        full_path = os.path.join(image_dir, file_name)
        scaled.save(full_path)
        self.ui.labelForPreview.setPixmap(scaled)
        self.ui.labelForPreview.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.ui.linkImgEdit.setText(full_path.replace("\\", "/"))

    def validate_not_empty(self, path: str, edit_field: QLineEdit):
        if not path and not edit_field.text():
            QMessageBox.warning(self, "Выбор файла", "Файл не выбран")

    def open_player(self):
        """Запуск плеера для предпросмотра видео, установленного в карточке"""
        if self.player is None or not self.player.isVisible():
            self.player = Player()
            self.player.setWindowTitle("Предварительный просмотр")
            video_path = self.get_data()["video_url"]
            self.player.player.setSource(video_path)

            self.player.show()
            self.player.player.play()

    def close_player(self):
        """Закрываем плеер программно"""
        if self.player and self.player.isVisible():
            self.player.close()  # Это вызовет closeEvent в классе Player
            self.player = None


class UpdateCardDialog(EditCardDialog):

    def __init__(self, categories, current_category, init_data, *args, **kwargs):
        super().__init__(categories, current_category, *args, **kwargs)
        category_name = categories[current_category].name
        self.ui.addButton.setText("Изменить")
        self.ui.cmbCategory.setCurrentText(category_name)
        self.ui.titleEdit.setText(str(init_data["title"]))
        self.ui.linkImgEdit.setText(str(init_data["preview_image_url"]))
        self.ui.linkVideoEdit.setText(str(init_data["video_url"]))
        self.ui.checkBox.setChecked(init_data["invisible"])
        self.ui.descriptionEdit.appendPlainText(init_data["description"])
        self.ui.labelForPreview.setPixmap(QPixmap(init_data["preview_image_url"] or PATH_BLANK_IMG))


class EditCatalogDialog(QDialog):
    """Диалог добавления категории"""

    def __init__(self, categories, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = categories
        self.ui = Ui_EditCatalogDialog()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)
        self.ui.assignParentCategory.addItem("", None)
        for c in self.categories.values():
            self.ui.assignParentCategory.addItem(c.name, c)

    def get_data(self):
        try:
            parent_id = self.ui.assignParentCategory.currentData().id
        except AttributeError:
            parent_id = None
        return {
            "name": self.ui.titleEdit.text(),
            "parent_id": parent_id
        }


class UpdateCatalogDialog(EditCatalogDialog):
    """Диалог изменения категории"""

    def __init__(self, categories, init_data, *args, **kwargs):
        super().__init__(categories, *args, **kwargs)
        category_name = init_data.name
        category_parent = init_data.parent_id
        if category_parent is not None:
            name = categories[category_parent].name
        else:
            name = None
        self.ui.addButton.setText("Изменить")
        self.ui.titleEdit.setText(category_name)
        self.ui.assignParentCategory.setCurrentText(name)


if __name__ == '__main__':
    print("Dialogs")
