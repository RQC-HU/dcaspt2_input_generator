import os
import subprocess
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction, QDragEnterEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMenu, QFileDialog, QMessageBox, QInputDialog
import qt_material


class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.load_output("data.out")

    def load_output(self, file_path):
        with open(file_path, newline='') as output:
            out = output.readlines()
            # output is space separated file
            rows = [line.split() for line in out]
            len_row = len(rows)
            len_column = max(len(row) for row in rows) if len_row > 0 else 0
            self.setRowCount(len_row)
            self.setColumnCount(len_column)
            for row in range(len_row):
                for column in range(len_column):
                    try:
                        text = rows[row][column]
                    except IndexError:
                        text = ""
                    item = QTableWidgetItem(text)
                    self.setItem(row, column, item)

    def show_context_menu(self, position):
        menu = QMenu()
        pale_blue_action = QAction("Pale Blue", self)
        pale_green_action = QAction("Pale Green", self)
        pale_pink_action = QAction("Pale Pink", self)
        pale_yellow_action = QAction("Pale Yellow", self)
        pale_blue_action.triggered.connect(lambda: self.change_background_color(QColor("#D3E8EB")))
        pale_green_action.triggered.connect(lambda: self.change_background_color(QColor("#D5ECD4")))
        pale_pink_action.triggered.connect(lambda: self.change_background_color(QColor("#F4D9D9")))
        pale_yellow_action.triggered.connect(lambda: self.change_background_color(QColor("#FDF4CD")))
        menu.addAction(pale_blue_action)
        menu.addAction(pale_green_action)
        menu.addAction(pale_pink_action)
        menu.addAction(pale_yellow_action)
        menu.exec(self.viewport().mapToGlobal(position))

    def change_background_color(self, color):
        indexes = self.selectedIndexes()
        rows = set()
        for index in indexes:
            rows.add(index.row())
        for row in rows:
            for column in range(self.columnCount()):
                self.item(row, column).setBackground(color)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Add drag and drop functionality
        self.setAcceptDrops(True)
        # Show the header bar
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.select_file)
        self.file_menu.addAction(self.open_action)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "SELECT A DIRAC OUTPUT FILE", "", "Output file (*.out)")
        if file_path:
            molecule_name, ok = self.question_molecule(file_path)
            if not ok:
                return
            # Run sum_dirac_defcoef subprocess
            self.run_sum_dirac_defcoef(file_path, molecule_name)
            self.dropEvent()

    def question_molecule(self, file_path):
        # Show a question message box that allow the user to write the molecule name
        molecule_name, ok = QInputDialog.getText(self, "Molecule name", "Enter the molecule name that you calculated using DIRAC:")
        return molecule_name, ok

    def run_sum_dirac_defcoef(self, file_path, molecule_name):
        current_dir = os.getcwd()
        sum_dirac_defcoef_path = os.path.join(current_dir, "summarize_dirac_dfcoef_coefficients", "sum_dirac_dfcoef")
        process = subprocess.run(f"python {sum_dirac_defcoef_path} -i {file_path} -m {molecule_name} -d 3 -c > data.out", shell=True)
        # Check the status of the subprocess named process
        if process.returncode != 0:
            QMessageBox.critical(self, "Error", f"An error has ocurred while running the sum_dirac_dfcoef program. Please, check the output file. path: {file_path}\nExecuted command: {sum_dirac_defcoef_path} -i {file_path} -m {molecule_name} -d 3 -c")

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if (event.mimeData().hasText()):
            event.accept()

    def dropEvent(self, event="") -> None:
        self.table_widget = TableWidget()
        self.setCentralWidget(self.table_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # qt_material.apply_stylesheet(app, theme='dark_teal.xml') # 'dark_teal.xml
    # stylesheet = app.styleSheet()
    # app.setStyleSheet(stylesheet + "QTableView {background-color: #514;}")
    window = MainWindow()
    window.resize(1280, 720)
    window.show()
    sys.exit(app.exec())
