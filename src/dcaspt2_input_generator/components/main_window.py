import os
import subprocess
from pathlib import Path

from dcaspt2_input_generator.components.data import colors, table_data
from dcaspt2_input_generator.components.menu_bar import MenuBar
from dcaspt2_input_generator.components.table_summary import TableSummary
from dcaspt2_input_generator.components.table_widget import TableWidget
from dcaspt2_input_generator.controller.color_settings_controller import ColorSettingsController
from dcaspt2_input_generator.controller.save_default_settings_controller import SaveDefaultSettingsController
from dcaspt2_input_generator.controller.widget_controller import WidgetController
from dcaspt2_input_generator.utils.dir_info import dir_info
from dcaspt2_input_generator.utils.utils import create_ras_str, debug_print
from qtpy.QtCore import QSettings
from qtpy.QtGui import QDragEnterEvent
from qtpy.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget


# Layout for the main window
# File, Settings, About (menu bar)
# message, AnimatedToggle (button)
# TableWidget (table)
# InputLayout (layout): core, inactive, active, secondary
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_UI()
        # employ native setting events to save/load form size and position
        self.settings = QSettings("Hiroshima University", "DIRAC-CASPT2 Input Generator")
        if self.settings.value("geometry") is not None:
            self.restoreGeometry(self.settings.value("geometry"))
        if self.settings.value("windowState") is not None:
            self.restoreState(self.settings.value("windowState"))

    def init_UI(self):
        # Add drag and drop functionality
        self.setAcceptDrops(True)

        # Show the header bar
        self.menu_bar = MenuBar()
        self.menu_bar.open_action_dirac.triggered.connect(self.select_file_Dirac)
        self.menu_bar.open_action_dfcoef.triggered.connect(self.select_file_DFCOEF)
        self.menu_bar.save_action_input.triggered.connect(self.save_input)
        self.menu_bar.save_action_dfcoef.triggered.connect(self.save_sum_dirac_dfcoef)

        # Body
        self.table_summary = TableSummary()
        self.table_widget = TableWidget()
        # Add Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_input)

        # Create an instance of WidgetController
        self.widget_controller = WidgetController(self.table_summary, self.table_widget)
        self.color_settings_controller = ColorSettingsController(
            self.table_widget, self.menu_bar.color_settings_action.color_settings
        )

        self.save_default_settings_controller = SaveDefaultSettingsController(
            color=colors,
            user_input=self.table_summary.user_input,
            save_default_settings_action=self.menu_bar.save_default_settings_action,
        )
        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.menu_bar)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.table_summary)
        layout.addWidget(self.save_button)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def closeEvent(self, a0) -> None:
        # save settings when closing
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        return super().closeEvent(a0)

    def save_input(self):
        def add_nelec(cur_nelec: int, rem_electrons: int) -> int:
            if rem_electrons >= 0:
                cur_nelec += 2
            return cur_nelec

        output = ""
        core = 0
        inact = 0
        act = 0
        sec = 0
        elec = 0
        ras1_list = []
        ras2_list = []
        ras3_list = []
        rem_electrons = table_data.header_info.electron_number
        for idx in range(self.table_widget.rowCount()):
            rem_electrons -= 2
            spinor_indices = [2 * idx + 1, 2 * idx + 2]  # 1 row = 2 spinors
            color = self.table_widget.item(idx, 0).background().color()
            if color == colors.core.color:
                debug_print(f"{idx}, core")
                core += 2
            elif color == colors.inactive.color:
                debug_print(f"{idx}, inactive")
                inact += 2
            elif color == colors.ras1.color:
                debug_print(f"{idx}, ras1")
                act += 2
                ras1_list.extend(spinor_indices)
                elec = add_nelec(elec, rem_electrons)
            elif color == colors.active.color:
                debug_print(f"{idx}, active")
                act += 2
                ras2_list.extend(spinor_indices)
                elec = add_nelec(elec, rem_electrons)
            elif color == colors.ras3.color:
                debug_print(f"{idx}, ras3")
                act += 2
                elec = add_nelec(elec, rem_electrons)
                ras3_list.extend(spinor_indices)
            elif color == colors.secondary.color:
                debug_print(f"{idx}, secondary")
                sec += 2
        # output += "ncore\n" + str(core) + "\n"  # ncore is meaningless option (https://github.com/kohei-noda-qcrg/dirac_caspt2/pull/114)
        output += "ninact\n" + str(inact) + "\n"
        output += "nact\n" + str(act) + "\n"
        output += "nelec\n" + str(elec) + "\n"
        output += "nsec\n" + str(sec) + "\n"
        output += "nroot\n" + self.table_summary.user_input.selectroot_number.text() + "\n"
        output += "selectroot\n" + self.table_summary.user_input.selectroot_number.text() + "\n"
        output += "totsym\n" + self.table_summary.user_input.totsym_number.text() + "\n"
        output += "diracver\n" + ("21" if self.table_summary.user_input.diracver_checkbox.isChecked() else "19") + "\n"
        # If only ras2_list is not empty, it means that is a CASPT2 calculation (not a RASPPT2 calculation)
        if len(ras1_list) + len(ras3_list) > 0:
            ras1_str = create_ras_str(sorted(ras1_list))
            ras2_str = create_ras_str(sorted(ras2_list))
            ras3_str = create_ras_str(sorted(ras3_list))
            output += (
                ""
                if len(ras1_list) == 0
                else "ras1\n" + ras1_str + "\n" + self.table_summary.user_input.ras1_max_hole_number.text() + "\n"
            )
            output += "" if len(ras2_list) == 0 else "ras2\n" + ras2_str + "\n"
            output += (
                ""
                if len(ras3_list) == 0
                else "ras3\n" + ras3_str + "\n" + self.table_summary.user_input.ras3_max_electron_number.text() + "\n"
            )
        output += "end\n"

        # open dialog to save the file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save dirac_caspt2 input File", "", "")
        if file_path:
            with open(file_path, mode="w") as f:
                f.write(output)

    def display_critical_error_message_box(self, message: str):
        QMessageBox.critical(self, "Error", message)

    def select_file_Dirac(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "SELECT A DIRAC OUTPUT FILE", "", "Output file (*.out)")
        if file_path:
            try:
                self.run_sum_Dirac_DFCOEF(file_path)
                self.reload_table(dir_info.sum_dirac_dfcoef_path)
            except subprocess.CalledProcessError as e:
                err_msg = f"It seems that the sum_dirac_dfcoef program has failed.\n\
Please check the output file. Is this DIRAC output file?\npath: {file_path}\n\n\ndetails: {e.stderr}"
                self.display_critical_error_message_box(err_msg)
            except Exception as e:
                err_msg = f"An unexpected error has ocurred.\n\
file_path: {file_path}\n\n\ndetails: {e}"
                self.display_critical_error_message_box(err_msg)

    def select_file_DFCOEF(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "SELECT A sum_dirac_dfcoef OUTPUT FILE", "", "Output file (*.out)"
        )
        if file_path:
            try:
                self.reload_table(file_path)
            except Exception as e:
                err_msg = f"An unexpected error has ocurred.\n\
file_path: {file_path}\n\n\ndetails: {e}"
                self.display_critical_error_message_box(err_msg)

    def save_sum_dirac_dfcoef(self):
        if not dir_info.sum_dirac_dfcoef_path.exists():
            QMessageBox.critical(
                self,
                "Error",
                "The sum_dirac_dfcoef.out file does not exist.\n\
Please run the sum_dirac_dfcoef program first.",
            )
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, caption="Save sum_dirac_dfcoef.out file as different name", filter="Output file (*.out)"
        )
        if not file_path.endswith(".out"):
            file_path += ".out"
        if file_path:
            import shutil

            # Copy the sum_dirac_dfcoef.out file to the file_path
            shutil.copy(dir_info.sum_dirac_dfcoef_path, file_path)

    def run_sum_Dirac_DFCOEF(self, file_path):
        def create_command(command: str) -> str:
            if os.name == "nt":
                return f"python -m {command}"
            return command

        def check_version():
            command = create_command("sum_dirac_dfcoef -v")
            p = subprocess.run(
                command.split(),
                check=True,
                stdout=subprocess.PIPE,
            )
            output = p.stdout.decode("utf-8")
            # v4.0.0 or later is required
            major_version = int(output.split(".")[0])
            if major_version < 4:
                msg = f"The version of sum_dirac_dfcoef is too old.\n\
sum_dirac_dfcoef version: {output}\n\
Please update sum_dirac_dfcoef to v4.0.0 or later with `pip install -U sum_dirac_dfcoef`"
                raise Exception(msg)

        def run_command():
            command = f"sum_dirac_dfcoef -i {file_path} -d 3 -c -o {dir_info.sum_dirac_dfcoef_path}"
            # If the OS is Windows, add "python -m" to the command to run the subprocess correctly
            if os.name == "nt":
                command = f"python -m {command}"
            # Run the subprocess
            try:
                subprocess.run(
                    command.split(),
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                err_msg = f"An error has ocurred while running the sum_dirac_dfcoef program.\n\
Please check the output file. path: {file_path}\nExecuted command: {command}"
                raise subprocess.CalledProcessError(e.returncode, e.cmd, e.output, err_msg) from e

        check_version()
        run_command()

    def reload_table(self, filepath: str):
        self.table_widget.reload(filepath)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            event.accept()

    def dropEvent(self, event="") -> None:
        # Get the file path
        filename = event.mimeData().text()[8:]
        filepath = Path(filename).expanduser().resolve()
        if not filepath.exists():
            QMessageBox.critical(
                self,
                "Error",
                "The file cannot be found.\n\
Please check your dropped file.",
            )
        try:
            self.table_widget.reload(filepath)
        except Exception:
            try:
                self.run_sum_Dirac_DFCOEF(filepath)
                self.table_widget.reload(dir_info.sum_dirac_dfcoef_path)
            except Exception:
                QMessageBox.critical(
                    self,
                    "Error",
                    "We cannot load the file properly.\n\
Please check your dropped file.",
                )
