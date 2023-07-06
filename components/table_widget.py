from qtpy.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QAction  # type: ignore
from qtpy.QtCore import Qt, Signal  # type: ignore

from components.color_info import color_info
from components.config import colors, Color, spinor_mode
from components.table_data import table_data


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

    def create_table(self):
        self.clear()
        rows = table_data.spinor_data if spinor_mode.get_is_spinor_mode() else table_data.mo_data
        len_column = max(len(row) for row in rows) if len(rows) > 0 else 0
        for row in range(len(rows)):
            for column in range(len_column):
                try:
                    text = rows[row][column]
                except IndexError:
                    text = ""
                item = QTableWidgetItem(text)
                self.setItem(row, column, item)

    def load_output(self, file_path):
        def set_table_data():
            rows = [line.split() for line in out]
            table_data.reset()
            table_data.mo_data = rows
            for row in rows:
                table_data.spinor_data.extend([row, row])

        with open(file_path, newline="") as output:
            out = output.readlines()
            # output is space separated file
            set_table_data()
            rows = table_data.spinor_data if spinor_mode.get_is_spinor_mode() else table_data.mo_data
            len_row = len(rows)
            len_column = max(len(row) for row in rows) if len_row > 0 else 0
            self.setRowCount(len_row)
            self.setColumnCount(len_column)
            self.create_table()

            # Table data
            for row in range(len_row):
                for column in range(len_column):
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
            if color == prev_color.core:
                self.change_selected_rows_background_color(row, colors.core)
            elif color == prev_color.inactive:
                self.change_selected_rows_background_color(row, colors.inactive)
            elif color == prev_color.active:
                self.change_selected_rows_background_color(row, colors.active)
            elif color == prev_color.secondary:
                self.change_selected_rows_background_color(row, colors.secondary)