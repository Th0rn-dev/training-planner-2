from PySide6.QtMultimediaWidgets import QVideoWidget


class CustomVideoWidget(QVideoWidget):
    def mouseDoubleClickEvent(self, event):
        if self.isFullScreen():
            self.setFullScreen(False)
        else:
            self.setFullScreen(True)
        event.accept()