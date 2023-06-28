import copy
import subprocess
import sys
from qtpy.QtCore import Qt, Signal  # type: ignore
from qtpy.QtGui import QAction, QDragEnterEvent, QScreen  # type: ignore
from qtpy.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QMenu,
    QButtonGroup,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QLabel,
    QLineEdit,
    QGridLayout,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)
from toggle import AnimatedToggle
from config import colors, is_display_mode, Color
from color_info import color_info

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

    def reload(self, output_file_path: str):
        print("TableWidget reload")
        self.load_output(output_file_path)

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
            color_info.setIndices(10, 20, 30, len_column)
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
        ranges = self.selectedRanges()
        selected_rows: set[int] = set()
        for r in ranges:
            selected_rows.update(range(r.topRow(), r.bottomRow() + 1))

        # Narrow down the color options
        if color_info.index_info["inactive"][0] in selected_rows:
            core_action = QAction(colors.core_message, self)
            core_action.triggered.connect(lambda: self.change_background_color(colors.core))
            menu.addAction(core_action)
        if color_info.index_info["core"][1] in selected_rows or color_info.index_info["active"][0] in selected_rows:
            inactive_action = QAction(colors.inactive_message, self)
            inactive_action.triggered.connect(lambda: self.change_background_color(colors.inactive))
            menu.addAction(inactive_action)
        if color_info.index_info["inactive"][1] in selected_rows or color_info.index_info["secondary"][0] in selected_rows:
            active_action = QAction(colors.active_message, self)
            active_action.triggered.connect(lambda: self.change_background_color(colors.active))
            menu.addAction(active_action)
        if color_info.index_info["active"][1] in selected_rows:
            secondary_action = QAction(colors.secondary_message, self)
            secondary_action.triggered.connect(lambda: self.change_background_color(colors.secondary))
            menu.addAction(secondary_action)
        menu.exec(self.viewport().mapToGlobal(position))

    def change_selected_rows_background_color(self, row, color):
        for column in range(self.columnCount()):
            self.item(row, column).setBackground(color)

    def change_background_color(self, color):
        indexes = self.selectedIndexes()
        rows = set([index.row() for index in indexes])
        for row in rows:
            self.change_selected_rows_background_color(row, color)
        self.colorChanged.emit()

    def update_color(self, prev_color: Color):
        for row in range(self.rowCount()):
            color = self.item(row, 0).background().color()
            print(color, row)
            if color == prev_color.core:
                self.change_selected_rows_background_color(row, colors.core)
            elif color == prev_color.inactive:
                self.change_selected_rows_background_color(row, colors.inactive)
            elif color == prev_color.active:
                self.change_selected_rows_background_color(row, colors.active)
            elif color == prev_color.secondary:
                self.change_selected_rows_background_color(row, colors.secondary)


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
        self.toggle_button = AnimatedToggle(pulse_checked_color="#D3E8EB", pulse_unchecked_color="#D5ECD4")
        self.toggle_button.setFixedSize(50, 40)
        self.addWidget(self.toggle_button, 2, 0, 1, 4)
        # ボタンの右に"spinor mode"というラベルを追加
        self.spinor_mode_label = QLabel("spinor mode")
        self.addWidget(self.spinor_mode_label, 2, 1, 10, 10)
        # If the toggle button is clicked, flip the display mode
        self.toggle_button.clicked.connect(self.flip_display_mode)

    def flip_display_mode(self):
        print(f"flip display mode, {is_display_mode.get_display_mode()}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Add drag and drop functionality
        self.setAcceptDrops(True)
        # Show the header bar
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        self.open_action_dirac = QAction("Open with DIRAC output", self)
        self.open_action_dirac.triggered.connect(self.selectFileDirac)
        self.file_menu.addAction(self.open_action_dirac)
        self.open_action_dfcoef = QAction("Open with sum_dirac_dfcoef output", self)
        self.open_action_dfcoef.triggered.connect(self.selectFileDFCOEF)
        self.file_menu.addAction(self.open_action_dfcoef)

        self.file_menu = self.menu_bar.addMenu("Settings")
        self.color_action = QAction("Color settings", self)
        self.color_action.triggered.connect(self.openColorSettings)
        self.file_menu.addAction(self.color_action)

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

    def colorSettingsChanged(self, button):
        prev_color = copy.deepcopy(colors)
        selected_button = self.buttonGroup.checkedButton()
        color_info = selected_button.text()
        colors.change_color_templates(color_info)
        if prev_color != colors:
            self.table_widget.update_color(prev_color)

    def openColorSettings(self):
        # 3つの選択肢を持つQInputDialogを作成
        # ラジオボタンで実装
        self.buttonGroup = QButtonGroup(self)
        self.default_button = QRadioButton("default", self)
        self.default_button.setChecked(True)
        self.red_green_button = QRadioButton("For red-green color blindness", self)
        self.green_yellow_button = QRadioButton("For green-yellow color blindness", self)
        self.buttonGroup.addButton(self.default_button)
        self.buttonGroup.addButton(self.red_green_button)
        self.buttonGroup.addButton(self.green_yellow_button)
        self.buttonGroup.setExclusive(True)
        self.buttonGroup.buttonClicked.connect(self.colorSettingsChanged)

        # Add the radio buttons to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.default_button)
        layout.addWidget(self.red_green_button)
        layout.addWidget(self.green_yellow_button)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Show the widget as a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Color Settings")
        dialog.setLayout(layout)
        dialog.exec_()

    def selectFileDirac(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "SELECT A DIRAC OUTPUT FILE", "", "Output file (*.out)")
        if file_path:
            molecule_name, ok = self.questionMolecule()
            if not ok:
                return
            # Run sum_dirac_defcoef subprocess
            self.runSumDiracDFCOEF(file_path, molecule_name)
            self.reloadTable(molecule_name + ".out")

    def selectFileDFCOEF(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "SELECT A sum_dirac_dfcoef OUTPUT FILE", "", "Output file (*.out)")
        if file_path:
            self.reloadTable(file_path)

    def questionMolecule(self):
        # Show a question message box that allow the user to write the molecule name
        molecule_name, ok = QInputDialog.getText(
            self,
            "Molecule name",
            "Enter the molecule name that you calculated using DIRAC:",
        )
        return molecule_name, ok

    def runSumDiracDFCOEF(self, file_path, molecule_name):
        command = f"sum_dirac_dfcoef -i {file_path} -m {molecule_name} -d 3 -c"
        process = subprocess.run(
            command,
            shell=True,
        )
        # Check the status of the subprocess named process
        if process.returncode != 0:
            QMessageBox.critical(
                self,
                "Error",
                f"An error has ocurred while running the sum_dirac_dfcoef program. Please, check the output file. path: {file_path}\nExecuted command: {command}",
            )

    def reloadTable(self, output_path: str):
        try:
            if self.table_widget:
                self.table_widget.reload(output_path)
        except AttributeError:
            self.table_widget = TableWidget()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            event.accept()

    def dropEvent(self, event="") -> None:
        # Get the file path
        filepath = event.mimeData().text()[8:]
        self.reloadTable(filepath)


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
            color = self.table_widget.item(row, 0).background()
            if color == colors.core:
                color_count[0] += 2
            elif color == colors.inactive:
                color_count[1] += 2
            elif color == colors.active:
                color_count[2] += 2
            elif color == colors.secondary:
                color_count[3] += 2
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
    width, height = int(QScreen.availableGeometry(QApplication.primaryScreen()).width() * (2 / 3)), int(QScreen.availableGeometry(QApplication.primaryScreen()).height() * (2 / 3))
    window.resize(width, height)
    window.show()
    sys.exit(app.exec())
