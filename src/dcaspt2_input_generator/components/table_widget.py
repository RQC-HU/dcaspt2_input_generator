import copy
from pathlib import Path
from typing import List

from dcaspt2_input_generator.components.data import Color, MOData, SpinorNumber, colors, table_data
from dcaspt2_input_generator.utils.utils import debug_print
from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QAction, QMenu, QTableWidget, QTableWidgetItem


# TableWidget is the widget that displays the output data
# It is a extended class of QTableWidget
# It has the following features:
# 1. Load the output data from the file "data.out"
# 2. Reload the output data
# 3. Show the context menu when right click
# 4. Change the background color of the selected cells
# 5. Emit the color_changed signal when the background color is changed
# Display the output data like the following:
# irrep              no. of spinor    energy (a.u.)    percentage 1    AO type 1    percentage 2    AO type 2    ...
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
            "inactive": {"start": -1, "end": -1},
            "secondary": {"start": -1, "end": -1},
        }
        self.color_found: dict[str, bool] = {"inactive": False, "secondary": False}

    def reload(self, output_file_path: Path):
        debug_print("TableWidget reload")
        self.load_output(output_file_path)

    def update_index_info(self):
        # Reset information
        self.color_found = {"inactive": False, "secondary": False}
        self.idx_info = {
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

    def validate_table_data(self, rows: List[MOData]) -> None:
        keys = table_data.header_info.spinor_num_info.keys()
        cur_idx = {k: 0 for k in keys}
        min_idx = copy.deepcopy(cur_idx)
        # Validate the data and set the min_idx to the minimum index of the mo_number per mo_symmetry
        for row in rows:
            key = row.mo_symmetry
            if key not in keys:
                msg = f"mo_symmetry {key} is not found in the eigenvalues data"
                raise ValueError(msg)
            if cur_idx[key] == 0:
                min_idx[key] = row.mo_number
            cur_idx[row.mo_symmetry] = row.mo_number

        # if v is 4, it means that the number of orbitals that are not included in the output is 3=4-1
        # because 4 means the first orbitals mo_number that is included in the output
        # *2 means that the number of spinors is doubled compared to the number of orbitals
        # therefore, the number of electrons is decreased by 2*(4-1)=6 because 3 orbitals are not included in the output
        table_data.header_info.electron_number -= sum(v - 1 for v in min_idx.values()) * 2

    def create_table(self):
        debug_print("TableWidget create_table")
        self.clear()
        rows = table_data.mo_data
        rows.sort(key=lambda x: (x.energy))
        self.setRowCount(len(rows))
        self.setColumnCount(table_data.column_max_len)
        self.validate_table_data(rows)

        rem_electrons = table_data.header_info.electron_number
        active_cnt = 0

        for row_idx, row in enumerate(rows):
            # Default CAS configuration is CAS(4,8) (4electrons, 8spinors)
            key = row.mo_symmetry
            moltra_info = table_data.header_info.moltra_info[key]
            if not moltra_info.get(row.mo_number, False):
                color_info = colors.not_used  # not in MOLTRA
            elif rem_electrons > 4:
                color_info = colors.inactive
            elif active_cnt < 8:
                active_cnt += 2
                color_info = colors.active
            else:
                color_info = colors.secondary

            rem_electrons -= 2
            color = color_info.color
            self.setItem(row_idx, 0, QTableWidgetItem(row.mo_symmetry))
            self.setItem(row_idx, 1, QTableWidgetItem(str(row.mo_number)))
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

    def set_column_header_items(self):
        header_data = ["irrep", "no. of spinor", "energy (a.u.)"]
        init_header_len = len(header_data)
        additional_header = []
        for idx in range(init_header_len, table_data.column_max_len):
            if idx % 2 == 0:
                additional_header.append(f"percentage {(idx-init_header_len)//2 + 1}")
            else:
                additional_header.append(f"AO type {(idx-init_header_len)//2 + 1}")

        header_data.extend(additional_header)
        self.setHorizontalHeaderLabels(header_data)

    def resize_columns(self):
        self.resizeColumnsToContents()
        for idx in range(table_data.column_max_len):
            if idx == 0:  # irrep
                self.setColumnWidth(idx, self.columnWidth(idx) + 20)
            elif idx == 1 or idx % 2 == 0:  # no. of spinor, percentage
                self.setColumnWidth(idx, self.columnWidth(idx) + 10)
            else:  # energy, AO type
                self.setColumnWidth(idx, self.columnWidth(idx) + 5)

    def load_output(self, file_path: Path):
        def create_row_dict(row: List[str]) -> MOData:
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

        def set_table_data():
            rows = [line.split() for line in out]
            table_data.mo_data = []
            try:
                for idx, row in enumerate(rows):
                    if idx <= 1:
                        continue
                    else:
                        if len(row) == 0:
                            continue
                        row_dict = create_row_dict(row)
                        table_data.mo_data.append(row_dict)
                        table_data.column_max_len = max(table_data.column_max_len, len(row))
            except ValueError as e:
                msg = "The output file is not correct, ValueError"
                raise ValueError(msg) from e
            except IndexError as e:
                msg = "The output file is not correct, IndexError"
                raise IndexError(msg) from e

        table_data.reset()
        with open(file_path) as output:
            # Read the first 2 lines to validate the data
            out = [output.readline() for _ in range(2)]
            rows = [line.split() for line in out]
            try:
                for idx, row in enumerate(rows):
                    if idx == 0:
                        # (e.g.) electron_num 106 E1g 16..85 E1u 11..91
                        table_data.header_info.electron_number = int(row[1])
                        self.read_moltra_info(row)
                    else:
                        # (e.g.) E1g closed 6 open 0 virtual 30 E1u closed 10 open 0 virtual 40 point_group C2v
                        # => table_data.header_info.spinor_num_info = {"E1g": SpinorNumber(6, 0, 30, 36),
                        #                                              "E1u": SpinorNumber(10, 0, 40, 50)}
                        #    table_data.header_info.point_group = "C2v"
                        self.read_spinor_num_info(row)
                        table_data.header_info.point_group = None  # reset the point group string
                        self.read_point_group(row)
            except ValueError as e:
                msg = "The output file is not correct, ValueError"
                raise ValueError(msg) from e
            except IndexError as e:
                msg = "The output file is not correct, IndexError"
                raise IndexError(msg) from e

        with open(file_path, newline="") as output:
            out = output.readlines()
            # output is space separated file
            set_table_data()
        self.create_table()
        self.set_column_header_items()
        self.resize_columns()
        self.color_changed.emit()

    def read_moltra_info(self, row: List[str]) -> None:
        idx = 2
        while idx + 2 <= len(row):
            moltra_type = row[idx]
            moltra_range_str = row[idx + 1]
            moltra_range = {}
            for elem in moltra_range_str.split(","):
                moltra_range_elem = elem.strip()
                if ".." in moltra_range_elem:
                    moltra_range_start, moltra_range_end = moltra_range_elem.split("..")
                    moltra_range_start = int(moltra_range_start)
                    moltra_range_end = int(moltra_range_end)
                    for i in range(moltra_range_start, moltra_range_end + 1):
                        moltra_range[i] = True
                else:
                    key_elem = int(moltra_range_elem)
                    moltra_range[key_elem] = True
            table_data.header_info.moltra_info[moltra_type] = moltra_range
            idx += 2
        for key in table_data.header_info.moltra_info.keys():
            table_data.header_info.moltra_info[key] = dict(sorted(table_data.header_info.moltra_info[key].items()))

    def read_point_group(self, row: List[str]) -> None:
        # (e.g.) E1g closed 6 open 0 virtual 30 E1u closed 10 open 0 virtual 40 point_group C2v
        # => table_data.header_info.point_group = "C2v"
        # if the number of columns is 2, the point group is included
        if len(row) % 7 == 2:
            table_data.header_info.point_group = row[-1]
        else:
            table_data.header_info.point_group = None

    def read_spinor_num_info(self, row: List[str]):
        # spinor_num info is following the format:
        # spinor_num_type1 closed int open int virtual int ...
        # (e.g.) E1g closed 6 open 0 virtual 30 E1u closed 10 open 0 virtual 40 point_group C2v
        # => table_data.header_info.spinor_num_info = {"E1g": SpinorNumber(6, 0, 30, 36),
        #                                              "E1u": SpinorNumber(10, 0, 40, 50)}
        if len(row) < 7:
            msg = f"spinor_num info is not correct: {row},\
spinor_num_type1 closed int open int virtual int spinor_num_type2 closed int open int virtual int ... point_group str\n\
is the correct format"
            raise ValueError(msg)
        idx = 0
        while idx + 7 <= len(row):
            spinor_num_type = row[idx]
            closed_shell = int(row[idx + 2])
            open_shell = int(row[idx + 4])
            virtual_orbitals = int(row[idx + 6])
            sum_of_orbitals = closed_shell + open_shell + virtual_orbitals
            table_data.header_info.spinor_num_info[spinor_num_type] = SpinorNumber(
                closed_shell, open_shell, virtual_orbitals, sum_of_orbitals
            )
            idx += 7

    def show_context_menu(self, position):
        menu = QMenu()
        ranges = self.selectedRanges()
        selected_rows: List[int] = []
        for r in ranges:
            selected_rows.extend(range(r.topRow(), r.bottomRow() + 1))

        top_row = selected_rows[0]
        bottom_row = selected_rows[-1]
        is_action_shown: dict[str, bool] = {"inactive": True, "secondary": True}
        # inactive action
        if self.color_found["secondary"] and top_row > self.idx_info["secondary"]["start"]:
            is_action_shown["inactive"] = False

        # secondary action
        if self.color_found["inactive"] and bottom_row < self.idx_info["inactive"]["end"]:
            is_action_shown["secondary"] = False

        # Show the inactive action
        if is_action_shown["inactive"]:
            inactive_action = QAction(colors.inactive.icon, colors.inactive.message)
            inactive_action.triggered.connect(lambda: self.change_background_color(colors.inactive.color))
            menu.addAction(inactive_action)

        # Show the secondary action
        if is_action_shown["secondary"]:
            secondary_action = QAction(colors.secondary.icon, colors.secondary.message)
            secondary_action.triggered.connect(lambda: self.change_background_color(colors.secondary.color))
            menu.addAction(secondary_action)

        # Show the active action
        ras1_action = QAction(colors.ras1.icon, colors.ras1.message)
        ras1_action.triggered.connect(lambda: self.change_background_color(colors.ras1.color))
        menu.addAction(ras1_action)

        active_action = QAction(colors.active.icon, colors.active.message)
        active_action.triggered.connect(lambda: self.change_background_color(colors.active.color))
        menu.addAction(active_action)

        ras3_action = QAction(colors.ras3.icon, colors.ras3.message)
        ras3_action.triggered.connect(lambda: self.change_background_color(colors.ras3.color))
        menu.addAction(ras3_action)

        not_used_action = QAction(colors.not_used.icon, colors.not_used.message)
        not_used_action.triggered.connect(lambda: self.change_background_color(colors.not_used.color))
        menu.addAction(not_used_action)

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
