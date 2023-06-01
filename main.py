from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem
import csv
from qt_material import apply_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table_view = QTableView()
        self.setCentralWidget(self.table_view)

        # Create a model to hold the table data
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)

        # Load and display CSV data
        self.load_csv_data('data.csv')

    def load_csv_data(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Set the number of rows and columns in the model
        self.model.setRowCount(len(data))
        self.model.setColumnCount(len(data[0]))

        style_sheet = """
            QTableView {
                background-color: #D3E8EB;
                selection-background-color: #A3C4C7;
            }

            QTableView::item {
                border: 1px solid #D3E8EB;
                color: #333;
                padding-left: 5px;
                padding-right: 5px;
            }

        """
        self.table_view.setStyleSheet(style_sheet)
        # Don't allow editing of cells
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)  # type: ignore

        # Set the data in each cell of the model
        for row, row_data in enumerate(data):
            for column, cell_data in enumerate(row_data):
                item = QStandardItem(cell_data)
                self.model.setItem(row, column, item)

                # Set the alignment for each cell
                alignCenter = getattr(Qt, 'AlignCenter')
                item.setTextAlignment(alignCenter)

        # Resize the columns to fit the content
        self.table_view.resizeColumnsToContents()

        # 1st column width requires more space
        self.table_view.setColumnWidth(0, 50)

    def cell_clicked(self, row, column):
        row = self.model.item(row)
        column = self.model.item(column)
        cell_data = row.text()
        # Show a message box with the cell text
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Cell Clicked")
        msg_box.setText(f"Clicked Cell: {cell_data}")
        msg_box.setStandardButtons(QMessageBox.Ok)  # type: ignore
        msg_box.setParent(self)
        msg_box.setWindowModality(Qt.WindowModal)  # type: ignore
        msg_box.setGeometry(self.geometry().center().x() - 150, self.geometry().center().y() - 75, 300, 150)
        msg_box.exec()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    # window size is 1280x720
    window.resize(1280, 720)
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    app.exec()
