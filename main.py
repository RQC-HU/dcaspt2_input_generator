import os
import subprocess
import sys
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QDragEnterEvent, QScreen
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QMenu,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QLabel,
    QLineEdit,
    QGridLayout,
    QVBoxLayout,
    QWidget,
)
from toggle import AnimatedToggle
from config import colors

# import qt_material


# TableWidget is the widget that displays the output data
# It is a subclass of QTableWidget
# It has the following features:
# 1. Load the output data from the file "data.out"
# 2. Reload the output data
# 3. Show the context menu when right click
# 4. Change the background color of the selected cells
# 5. Emit the colorChanged signal when the background color is changed
# Display the output data like the following:
# gerade/ungerade    no. of spinor    energy (a.u.)    percentage 1    AO type 1    percentage 2    AO type 2    ...
# E1u                1                -9.631           33.333          B3uArpx      33.333          B2uArpy      ...
# E1u                2                -9.546           50.000          B3uArpx      50.000          B2uArpy      ...
# ...
class TableWidget(QTableWidget):
    colorChanged = Signal()

    def __init__(self):
        print("TableWidget init")
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # type: ignore
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # type: ignore

    def reload(self):
        print("TableWidget reload")
        self.load_output("data.out")

    def load_output(self, file_path):
        with open(file_path, newline="") as output:
            out = output.readlines()
            # output is space separated file
            rows = [line.split() for line in out]
            len_row = len(rows)
            len_column = max(len(row) for row in rows) if len_row > 0 else 0
            self.setRowCount(len_row)
            self.setColumnCount(len_column)

            # Table data
            for row in range(len_row):
                for column in range(len_column):
                    try:
                        text = rows[row][column]
                    except IndexError:
                        text = ""
                    item = QTableWidgetItem(text)
                    self.setItem(row, column, item)
                    if row < 10:
                        self.item(row, column).setBackground(colors.core)
                    elif row < 20:
                        self.item(row, column).setBackground(colors.inactive)
                    elif row < 30:
                        self.item(row, column).setBackground(colors.active)
                    else:
                        self.item(row, column).setBackground(colors.secondary)
            # Header data
            header_data = ["gerade/ungerade", "no. of spinor", "energy (a.u.)"]
            for idx in range(len(header_data), len_column):
                if idx % 2 == 0:
                    header_data.append(f"percentage {(idx-len(header_data))//2 + 1}")
                else:
                    header_data.append(f"AO type {(idx-len(header_data))//2 + 1}")
            self.setHorizontalHeaderLabels(header_data)
        self.colorChanged.emit()

    def show_context_menu(self, position):
        menu = QMenu()
        pale_blue_action = QAction(colors.core_message, self)
        pale_green_action = QAction(colors.inactive_message, self)
        pale_pink_action = QAction(colors.active_message, self)
        pale_yellow_action = QAction(colors.secondary_message, self)
        pale_blue_action.triggered.connect(
            lambda: self.change_background_color(colors.core)
        )
        pale_green_action.triggered.connect(
            lambda: self.change_background_color(colors.inactive)
        )
        pale_pink_action.triggered.connect(
            lambda: self.change_background_color(colors.active)
        )
        pale_yellow_action.triggered.connect(
            lambda: self.change_background_color(colors.secondary)
        )
        menu.addAction(pale_blue_action)
        menu.addAction(pale_green_action)
        menu.addAction(pale_pink_action)
        menu.addAction(pale_yellow_action)
        menu.exec(self.viewport().mapToGlobal(position))

    def change_background_color(self, color):
        indexes = self.selectedIndexes()
        rows = set([index.row() for index in indexes])
        for row in rows:
            for column in range(self.columnCount()):
                self.item(row, column).setBackground(color)
        self.colorChanged.emit()


# InputLayout provides the layout for the input data
# like the following: ([ ] = line edit)
# core   inactive    active    secondary
# [  ]     [  ]       [  ]       [ ]
class InputLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create the labels
        self.core_label = QLabel("core")
        self.inactive_label = QLabel("inactive")
        self.active_label = QLabel("active")
        self.secondary_label = QLabel("secondary")

        # Create the line edits
        self.core_line_edit = QLineEdit()
        self.inactive_line_edit = QLineEdit()
        self.active_line_edit = QLineEdit()
        self.secondary_line_edit = QLineEdit()

        # Add the labels and line edits to the layout
        self.addWidget(self.core_label, 0, 0)
        self.addWidget(self.inactive_label, 0, 1)
        self.addWidget(self.active_label, 0, 2)
        self.addWidget(self.secondary_label, 0, 3)
        self.addWidget(self.core_line_edit, 1, 0)
        self.addWidget(self.inactive_line_edit, 1, 1)
        self.addWidget(self.active_line_edit, 1, 2)
        self.addWidget(self.secondary_line_edit, 1, 3)

        # Add toggle button
        self.toggle_button = AnimatedToggle(
            pulse_checked_color="#D3E8EB", pulse_unchecked_color="#D5ECD4"
        )
        self.addWidget(self.toggle_button, 2, 0, 1, 4)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Add drag and drop functionality
        self.setAcceptDrops(True)
        # Show the header bar
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.selectFile)
        self.file_menu.addAction(self.open_action)

        # Create an instance of InputLayout
        # self.input_layout = InputLayout()
        self.input_layout = InputLayout()
        self.table_widget = TableWidget()

        self.widget_controller = WidgetController(self.input_layout, self.table_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addLayout(self.input_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def selectFile(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "SELECT A DIRAC OUTPUT FILE", "", "Output file (*.out)"
        )
        if file_path:
            molecule_name, ok = self.questionMolecule()
            if not ok:
                return
            # Run sum_dirac_defcoef subprocess
            self.runSumDiracDFCOEF(file_path, molecule_name)
            self.reloadTable()

    def questionMolecule(self):
        # Show a question message box that allow the user to write the molecule name
        molecule_name, ok = QInputDialog.getText(
            self,
            "Molecule name",
            "Enter the molecule name that you calculated using DIRAC:",
        )
        return molecule_name, ok

    def runSumDiracDFCOEF(self, file_path, molecule_name):
        current_dir = os.getcwd()
        process = subprocess.run(
            f"sum_dirac_dfcoef -i {file_path} -m {molecule_name} -d 3 -c > data.out",
            shell=True,
        )
        # Check the status of the subprocess named process
        if process.returncode != 0:
            QMessageBox.critical(
                self,
                "Error",
                f"An error has ocurred while running the sum_dirac_dfcoef program. Please, check the output file. path: {file_path}\nExecuted command: {sum_dirac_defcoef_path} -i {file_path} -m {molecule_name} -d 3 -c",
            )

    def reloadTable(self):
        try:
            if self.table_widget:
                self.table_widget.reload()
        except AttributeError:
            self.table_widget = TableWidget()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            event.accept()

    def dropEvent(self, event="") -> None:
        self.reloadTable()


class WidgetController:
    def __init__(self, input_layout: InputLayout, table_widget: TableWidget):
        self.input_layout = input_layout
        self.table_widget = table_widget

        # Connect signals and slots
        # change_background_color is a slot
        self.table_widget.colorChanged.connect(self.onTableWidgetColorChanged)

    def onTableWidgetColorChanged(self):
        color_count = [0, 0, 0, 0]  # core, inactive, active, secondary
        for row in range(self.table_widget.rowCount()):
            if self.table_widget.item(row, 0).background() == colors.core:
                color_count[0] += 1
            elif self.table_widget.item(row, 0).background() == colors.inactive:
                color_count[1] += 1
            elif self.table_widget.item(row, 0).background() == colors.active:
                color_count[2] += 1
            elif self.table_widget.item(row, 0).background() == colors.secondary:
                color_count[3] += 1
        self.input_layout.core_line_edit.setText(str(color_count[0]))
        self.input_layout.core_line_edit.update()

        self.input_layout.inactive_line_edit.setText(str(color_count[1]))
        self.input_layout.active_line_edit.setText(str(color_count[2]))
        self.input_layout.secondary_line_edit.setText(str(color_count[3]))
        # Reload the input
        self.input_layout.inactive_line_edit.update()
        self.input_layout.active_line_edit.update()
        self.input_layout.secondary_line_edit.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # qt_material.apply_stylesheet(app, theme='dark_teal.xml') # 'dark_teal.xml
    # stylesheet = app.styleSheet()
    # app.setStyleSheet(stylesheet + "QTableView {background-color: #514;}")
    window = MainWindow()
    width, height = int(
        QScreen.availableGeometry(QApplication.primaryScreen()).width() * (2 / 3)
    ), int(QScreen.availableGeometry(QApplication.primaryScreen()).height() * (2 / 3))
    window.resize(width, height)
    window.show()
    sys.exit(app.exec())
