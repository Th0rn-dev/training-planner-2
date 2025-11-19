import os.path
import shutil
from datetime import datetime

from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox, QLineEdit

from ui.edit_dialog_ui import Ui_Dialog as Ui_EditCardDialog
from ui.edit_catalog_dialog_ui import Ui_Dialog as Ui_EditCatalogDialog
from utils import dir_scan


class EditCardDialog(QDialog):
    """Диалог добавления карточки"""

    PATH_VIDEO = "./video/"
    PATH_IMAGES = "./images/"

    def __init__(self, categories, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = categories
        self.ui = Ui_EditCardDialog()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)
        self.ui.addVideoButton.clicked.connect(self.add_video_file)
        self.ui.addImageButton.clicked.connect(self.add_img_file)

        for c in self.categories.values():
            self.ui.cmbCategory.addItem(c.name, c)

    def get_data(self):
        return {
            "title": self.ui.titleEdit.text(),
            "preview_image_url": self.ui.linkImgEdit.text(),
            "video_url": self.ui.linkVideoEdit.text(),
            "category_id": self.ui.cmbCategory.currentData().id
        }

    def add_video_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open Video File', "",
                                              'Media Files (*.mp4 *.mkv *.amv *.m4v *.mov)')
        self.validate_not_empty(path, self.ui.linkVideoEdit)
        file_name = os.path.basename(path)
        date = datetime.now().date().strftime("%Y-%m-%d")
        dir_list = dir_scan(self.PATH_VIDEO)
        video_dir = os.path.join(self.PATH_VIDEO, date)
        if date not in dir_list:
            os.makedirs(video_dir)
        full_path = os.path.join(video_dir, file_name)
        shutil.copy(path, full_path)
        self.ui.linkVideoEdit.setText(full_path.replace("\\", "/"))

    def add_img_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', "",
                                              'Media Files (*.jpg *.jpeg *.png *.gif)')
        self.validate_not_empty(path, self.ui.linkImgEdit)
        file_name = os.path.basename(path)
        date = datetime.now().date().strftime("%Y-%m-%d")
        dir_list = dir_scan(self.PATH_IMAGES)
        image_dir = os.path.join(self.PATH_IMAGES, date)
        if date not in dir_list:
            os.makedirs(image_dir)
        full_path = os.path.join(image_dir, file_name)
        shutil.copy(path, full_path)
        self.ui.linkImgEdit.setText(full_path.replace("\\", "/"))

    def validate_not_empty(self, path: str, edit_field: QLineEdit):
        if not path and not edit_field.text():
            QMessageBox.warning(self, "Выбор файла", "Файл не выбран")


class UpdateCardDialog(EditCardDialog):

    def __init__(self, categories, init_data, *args, **kwargs):
        super().__init__(categories, *args, **kwargs)
        category_name = categories[init_data.category_id].name
        self.ui.addButton.setText("Изменить")
        self.ui.cmbCategory.setCurrentText(category_name)
        self.ui.titleEdit.setText(str(init_data.title))
        self.ui.linkImgEdit.setText(str(init_data.preview_image_url))
        self.ui.linkVideoEdit.setText(str(init_data.video_url))


class EditCatalogDialog(QDialog):
    """Диалог добавления категории"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_EditCatalogDialog()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)

    def get_data(self):
        return {"name": self.ui.titleEdit.text()}


class UpdateCatalogDialog(EditCatalogDialog):
    """Диалог изменения категории"""

    def __init__(self, init_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_name = init_data.name
        self.ui.addButton.setText("Изменить")
        self.ui.titleEdit.setText(category_name)


if __name__ == '__main__':
    print("Dialogs")
