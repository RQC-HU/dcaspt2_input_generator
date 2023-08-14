from qtpy.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QAction  # type: ignore
from qtpy.QtCore import Qt, Signal  # type: ignore
from qtpy.QtGui import QColor

from components.data import colors, Color
from components.data import table_data, MOData


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
        # QTableWidget.ContiguousSelection: Multiple ranges selection is impossible.
        # https://doc.qt.io/qt-6/qabstractitemview.html#SelectionMode-enum
        self.setSelectionMode(QTableWidget.ContiguousSelection)  # type: ignore

    def reload(self, output_file_path: str):
        print("TableWidget reload")
        self.load_output(output_file_path)

    def create_table(self):
        print("TableWidget create_table")
        inactive_start = 10
        active_start = 20
        secondary_start = 30
        self.clear()
        rows = table_data.mo_data
        self.setRowCount(len(rows))
        self.setColumnCount(table_data.column_max_len)
        for row_idx, row in enumerate(rows):
            color: QColor = (
                colors.core.color if row_idx < inactive_start else colors.inactive.color if row_idx < active_start else colors.active.color if row_idx < secondary_start else colors.secondary.color
            )
            # mo_symmetry
            self.setItem(row_idx, 0, QTableWidgetItem(row.mo_symmetry))
            # mo_number_dirac
            self.setItem(row_idx, 1, QTableWidgetItem(str(row.mo_number)))
            # mo_energy
            self.setItem(row_idx, 2, QTableWidgetItem(str(row.energy)))
            # percentage, ao_type
            column_before_ao_percentage = 3
            for idx in range(table_data.column_max_len - column_before_ao_percentage):
                try:
                    ao_type = QTableWidgetItem(row.ao_type[idx])
                    ao_percentage = QTableWidgetItem(str(row.percentage[idx]))
                except IndexError:
                    ao_type = QTableWidgetItem("")
                    ao_percentage = QTableWidgetItem("")
                ao_type.setBackground(color)
                ao_percentage.setBackground(color)
                ao_type_column = column_before_ao_percentage + 2 * idx
                ao_percentage_column = ao_type_column + 1
                self.setItem(row_idx, ao_type_column, ao_type)
                self.setItem(row_idx, ao_percentage_column, ao_percentage)

            for idx in range(table_data.column_max_len):
                self.item(row_idx, idx).setBackground(color)

    def load_output(self, file_path):
        def create_row_dict(row: list[str]) -> MOData:
            mo_symmetry = row[0]
            mo_number_dirac = int(row[1])
            mo_energy = float(row[2])
            ao_type = [row[i] for i in range(3, len(row), 2)]
            ao_percentage = [float(row[i]) for i in range(4, len(row), 2)]
            return MOData(mo_number=mo_number_dirac, mo_symmetry=mo_symmetry, energy=mo_energy, ao_type=ao_type, percentage=ao_percentage, ao_len=len(ao_type))

        def set_table_data():
            table_data.reset()
            rows = [line.split() for line in out]
            table_data.mo_data = []
            try:
                for idx, row in enumerate(rows):
                    row_dict = create_row_dict(row)
                    table_data.mo_data.append(row_dict)
                    table_data.column_max_len = max(table_data.column_max_len, len(row))

            except ValueError:
                raise ValueError("The output file is not correct, ValueError")
            except IndexError:
                raise IndexError("The output file is not correct, IndexError")
            len_row = len(rows)
            len_column = max(len(row) for row in rows) if len_row > 0 else 0

            # Header data
            header_data = ["gerade/ungerade", "no. of spinor", "energy (a.u.)"]
            init_header_len = len(header_data)
            additional_header = []
            for idx in range(init_header_len, len_column):
                if idx % 2 == 0:
                    additional_header.append(f"percentage {(idx-init_header_len)//2 + 1}")
                else:
                    additional_header.append(f"AO type {(idx-init_header_len)//2 + 1}")
            header_data.extend(additional_header)
            self.setHorizontalHeaderLabels(header_data)

        with open(file_path, newline="") as output:
            out = output.readlines()
            # output is space separated file
            set_table_data()
            self.create_table()

        self.colorChanged.emit()

    def show_context_menu(self, position):
        menu = QMenu()
        ranges = self.selectedRanges()
        selected_rows: set[int] = set()
        for r in ranges:
            selected_rows.update(range(r.topRow(), r.bottomRow() + 1))
        selected_colors: list[QColor] = list()
        for row in selected_rows:
            selected_colors.append(self.item(row, 0).background().color())
        # core action
        if colors.inactive in selected_colors:
            core_action = QAction(colors.core.message, self)
            core_action.triggered.connect(lambda: self.change_background_color(colors.core.color))
            menu.addAction(core_action)
        # inactive action
        if colors.active in selected_colors or colors.core in selected_colors:
            inactive_action = QAction(colors.inactive.message, self)
            inactive_action.triggered.connect(lambda: self.change_background_color(colors.inactive.color))
            menu.addAction(inactive_action)

        # secondary action
        if colors.active in selected_colors:
            secondary_action = QAction(colors.secondary.message, self)
            secondary_action.triggered.connect(lambda: self.change_background_color(colors.secondary.color))
            menu.addAction(secondary_action)

        # active action

        ras1_action = QAction(colors.ras1.message, self)
        ras1_action.triggered.connect(lambda: self.change_background_color(colors.ras1.color))
        menu.addAction(ras1_action)

        active_action = QAction(colors.active.message, self)
        active_action.triggered.connect(lambda: self.change_background_color(colors.active.color))
        menu.addAction(active_action)

        ras3_action = QAction(colors.ras3.message, self)
        ras3_action.triggered.connect(lambda: self.change_background_color(colors.ras3.color))
        menu.addAction(ras3_action)
        menu.exec(self.viewport().mapToGlobal(position))

    def change_selected_rows_background_color(self, row, color: QColor):
        for column in range(self.columnCount()):
            self.item(row, column).setBackground(color)

    def change_background_color(self, color):
        indexes = self.selectedIndexes()
        rows = set([index.row() for index in indexes])
        for row in rows:
            self.change_selected_rows_background_color(row, color)
        self.colorChanged.emit()

    def update_color(self, prev_color: Color):
        print("update_color")

        for row in range(self.rowCount()):
            color = self.item(row, 0).background().color()
            if color == prev_color.core.color:
                self.change_selected_rows_background_color(row, colors.core.color)
            elif color == prev_color.inactive.color:
                self.change_selected_rows_background_color(row, colors.inactive.color)
            elif color == prev_color.ras1.color:
                self.change_selected_rows_background_color(row, colors.ras1.color)
            elif color == prev_color.active.color:
                self.change_selected_rows_background_color(row, colors.active.color)
            elif color == prev_color.ras3.color:
                self.change_selected_rows_background_color(row, colors.ras3.color)
            elif color == prev_color.secondary.color:
                self.change_selected_rows_background_color(row, colors.secondary.color)
