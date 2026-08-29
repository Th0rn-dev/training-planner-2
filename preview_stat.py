from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTreeView, QHeaderView


def build_tree_from_dict(data: dict) -> QStandardItemModel:
    """
    Строит QStandardItemModel из словаря {dir_name: [files...]}.
    Корневой элемент не создаётся (будет пустой корень дерева).
    """
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(["Name"])

    for dir_name, files in data.items():
        dir_item = QStandardItem(dir_name)
        dir_item.setEditable(False)

        for file_name in files:
            file_item = QStandardItem(file_name)
            file_item.setEditable(False)
            dir_item.appendRow(file_item)

        model.appendRow(dir_item)

    return model

class PreviewStatisticWindow(QMainWindow):

    def __init__(self, data: dict):
        super(PreviewStatisticWindow, self).__init__()
        self.setWindowTitle("Files Tree View")
        self.resize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        tree_view = QTreeView()
        tree_view.setAlternatingRowColors(True)
        tree_view.expandAll()  # развернуть все ветки сразу

        model = build_tree_from_dict(data)
        tree_view.setModel(model)

        # опционально: сделать первый столбец растягиваемым
        tree_view.header().setStretchLastSection(False)
        tree_view.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        layout.addWidget(tree_view)


if __name__ == '__main__':
    print("Preview statistics")