from pathlib import Path

from dcaspt2_input_generator.components.data import (
    Color,
    ColorPopupInfo,
    Eigenvalues,
    MOData,
    SpinorNumber,
    colors,
    table_data,
)
from dcaspt2_input_generator.utils.utils import debug_print
from qtpy.QtCore import Qt, Signal  # type: ignore
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QAction, QMenu, QTableWidget, QTableWidgetItem  # type: ignore


# TableWidget is the widget that displays the output data
# It is a extended class of QTableWidget
# It has the following features:
# 1. Load the output data from the file "data.out"
# 2. Reload the output data
# 3. Show the context menu when right click
# 4. Change the background color of the selected cells
# 5. Emit the color_changed signal when the background color is changed
# Display the output data like the following:
# gerade/ungerade    no. of spinor    energy (a.u.)    percentage 1    AO type 1    percentage 2    AO type 2    ...
# E1u                1                -9.631           33.333          B3uArpx      33.333          B2uArpy      ...
# E1u                2                -9.546           50.000          B3uArpx      50.000          B2uArpy      ...
# ...
class TableWidget(QTableWidget):
    color_changed = Signal()

    def __init__(self):
        debug_print("TableWidget init")
        super().__init__()

        # Set the context menu policy to custom context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # QTableWidget.ContiguousSelection: Multiple ranges selection is impossible.
        # https://doc.qt.io/qt-6/qabstractitemview.html#SelectionMode-enum
        self.setSelectionMode(QTableWidget.SelectionMode.ContiguousSelection)

        # Initialize the index information and the color found information
        self.idx_info = {
            "core": {"start": -1, "end": -1},
            "inactive": {"start": -1, "end": -1},
            "secondary": {"start": -1, "end": -1},
        }
        self.color_found: dict[str, bool] = {"core": False, "inactive": False, "secondary": False}

    def reload(self, output_file_path: Path):
        debug_print("TableWidget reload")
        self.load_output(output_file_path)

    def update_index_info(self):
        # Reset information
        self.color_found = {"core": False, "inactive": False, "secondary": False}
        self.idx_info = {
            "core": {"start": -1, "end": -1},
            "inactive": {"start": -1, "end": -1},
            "secondary": {"start": -1, "end": -1},
        }

        # Update information
        for row in range(self.rowCount()):
            row_color = self.item(row, 0).background().color()
            color_info = colors.get_color_info(row_color)
            if color_info.name not in self.color_found.keys():
                # active, ras1, ras3 are not included because their context menu (right click menu) is always shown
                # and they are not needed to store the index information
                # therefore, skip them
                continue
            elif not self.color_found[color_info.name]:
                self.color_found[color_info.name] = True
                self.idx_info[color_info.name]["start"] = row
                self.idx_info[color_info.name]["end"] = row
            else:
                self.idx_info[color_info.name]["end"] = row

    def create_table(self):
        debug_print("TableWidget create_table")
        active_start = 10
        secondary_start = 20
        self.clear()
        rows = table_data.mo_data
        self.setRowCount(len(rows))
        self.setColumnCount(table_data.column_max_len)
        for row_idx, row in enumerate(rows):
            color_info: ColorPopupInfo = (
                colors.inactive
                if row_idx < active_start
                else colors.active
                if row_idx < secondary_start
                else colors.secondary
            )
            color: QColor = color_info.color
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

        self.update_index_info()

    def load_output(self, file_path: Path):
        def create_row_dict(row: "list[str]") -> MOData:
            mo_symmetry = row[0]
            mo_number_dirac = int(row[1])
            mo_energy = float(row[2])
            ao_type = [row[i] for i in range(3, len(row), 2)]
            ao_percentage = [float(row[i]) for i in range(4, len(row), 2)]
            return MOData(
                mo_number=mo_number_dirac,
                mo_symmetry=mo_symmetry,
                energy=mo_energy,
                ao_type=ao_type,
                percentage=ao_percentage,
                ao_len=len(ao_type),
            )

        def read_eigenvalues_info(row: "list[str]") -> Eigenvalues:
            eigenvalues = Eigenvalues()
            idx = 0
            while idx + 7 <= len(row):
                # E1g closed 6 open 0 virtual 0
                # eigenvalues_type _ closed_shell _ open_shell _ virtual_orbitals
                eigenvalues_type = row[idx]
                closed_shell = int(row[idx + 2])
                open_shell = int(row[idx + 4])
                virtual_orbitals = int(row[idx + 6])
                spinor_number = SpinorNumber(closed_shell, open_shell, virtual_orbitals)
                eigenvalues.data[eigenvalues_type] = spinor_number
                idx += 7

        def set_table_data():
            table_data.reset()
            rows = [line.split() for line in out]
            table_data.mo_data = []
            try:
                for idx, row in enumerate(rows):
                    if idx == 0:
                        eigenvalues = read_eigenvalues_info(row)
                    row_dict = create_row_dict(row)
                    table_data.mo_data.append(row_dict)
                    table_data.column_max_len = max(table_data.column_max_len, len(row))
            except ValueError as e:
                msg = "The output file is not correct, ValueError"
                raise ValueError(msg) from e
            except IndexError as e:
                msg = "The output file is not correct, IndexError"
                raise IndexError(msg) from e
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

        self.color_changed.emit()

    def show_context_menu(self, position):
        menu = QMenu()
        ranges = self.selectedRanges()
        selected_rows: "list[int]" = []
        for r in ranges:
            selected_rows.extend(range(r.topRow(), r.bottomRow() + 1))

        top_row = selected_rows[0]
        bottom_row = selected_rows[-1]
        is_action_shown: dict[str, bool] = {"core": True, "inactive": True, "secondary": True}
        # core action
        if (self.color_found["inactive"] and top_row > self.idx_info["inactive"]["start"]) or (
            self.color_found["secondary"] and top_row > self.idx_info["secondary"]["start"]
        ):
            is_action_shown["core"] = False

        # inactive action
        if (self.color_found["core"] and bottom_row < self.idx_info["core"]["end"]) or (
            self.color_found["secondary"] and top_row > self.idx_info["secondary"]["start"]
        ):
            is_action_shown["inactive"] = False

        # secondary action
        if (self.color_found["core"] and bottom_row < self.idx_info["core"]["end"]) or (
            self.color_found["inactive"] and bottom_row < self.idx_info["inactive"]["end"]
        ):
            is_action_shown["secondary"] = False

        # Show the core action
        if is_action_shown["core"]:
            core_action = QAction(colors.core.message)
            core_action.triggered.connect(lambda: self.change_background_color(colors.core.color))
            menu.addAction(core_action)
        # Show the inactive action
        if is_action_shown["inactive"]:
            inactive_action = QAction(colors.inactive.message)
            inactive_action.triggered.connect(lambda: self.change_background_color(colors.inactive.color))
            menu.addAction(inactive_action)

        # Show the secondary action
        if is_action_shown["secondary"]:
            secondary_action = QAction(colors.secondary.message)
            secondary_action.triggered.connect(lambda: self.change_background_color(colors.secondary.color))
            menu.addAction(secondary_action)

        # Show the active action
        ras1_action = QAction(colors.ras1.message)
        ras1_action.triggered.connect(lambda: self.change_background_color(colors.ras1.color))
        menu.addAction(ras1_action)

        active_action = QAction(colors.active.message)
        active_action.triggered.connect(lambda: self.change_background_color(colors.active.color))
        menu.addAction(active_action)

        ras3_action = QAction(colors.ras3.message)
        ras3_action.triggered.connect(lambda: self.change_background_color(colors.ras3.color))
        menu.addAction(ras3_action)
        menu.exec(self.viewport().mapToGlobal(position))

    def change_selected_rows_background_color(self, row, color: QColor):
        for column in range(self.columnCount()):
            self.item(row, column).setBackground(color)

    def change_background_color(self, color):
        indexes = self.selectedIndexes()
        rows = {index.row() for index in indexes}
        for row in rows:
            self.change_selected_rows_background_color(row, color)
        self.update_index_info()
        self.color_changed.emit()

    def update_color(self, prev_color: Color):
        debug_print("update_color")
        color_mappping = {
            prev_color.core.color.name(): colors.core.color,
            prev_color.inactive.color.name(): colors.inactive.color,
            prev_color.ras1.color.name(): colors.ras1.color,
            prev_color.active.color.name(): colors.active.color,
            prev_color.ras3.color.name(): colors.ras3.color,
            prev_color.secondary.color.name(): colors.secondary.color,
        }

        for row in range(self.rowCount()):
            color = self.item(row, 0).background().color()
            new_color = color_mappping.get(color.name())
            if new_color:
                self.change_selected_rows_background_color(row, new_color)
        self.color_changed.emit()
