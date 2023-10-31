import os
import subprocess

from qtpy.QtGui import QDragEnterEvent
from qtpy.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget

from ..controller.color_settings_controller import ColorSettingsController
from ..controller.save_default_settings_controller import SaveDefaultSettingsController
from ..controller.widget_controller import WidgetController
from ..utils.dir_info import dir_info
from ..utils.utils import create_ras_str
from .data import colors
from .menu_bar import MenuBar
from .table_summary import TableSummary
from .table_widget import TableWidget


# Layout for the main window
# File, Settings, About (menu bar)
# message, AnimatedToggle (button)
# TableWidget (table)
# InputLayout (layout): core, inactive, active, secondary
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()

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

    def save_input(self):
        output = ""
        core = 0
        inact = 0
        act = 0
        sec = 0
        ras1_list = []
        ras2_list = []
        ras3_list = []
        for idx in range(self.table_widget.rowCount()):
            spinor_indices = [2 * idx + 1, 2 * idx + 2]  # 1 row = 2 spinors
            color = self.table_widget.item(idx, 0).background().color()
            if color == colors.core.color:
                print(idx, "core")
                core += 2
            elif color == colors.inactive.color:
                print(idx, "inactive")
                inact += 2
            elif color == colors.ras1.color:
                print(idx, "ras1")
                act += 2
                ras1_list.extend(spinor_indices)
            elif color == colors.active.color:
                print(idx, "active")
                act += 2
                ras2_list.extend(spinor_indices)
            elif color == colors.ras3.color:
                print(idx, "ras3")
                act += 2
                ras3_list.extend(spinor_indices)
            elif color == colors.secondary.color:
                print(idx, "secondary")
                sec += 2
        output += "ncore\n" + str(core) + "\n"
        output += "ninact\n" + str(inact) + "\n"
        output += "nact\n" + str(act) + "\n"
        output += "nsec\n" + str(sec) + "\n"
        output += "nbas\n" + str(core + inact + act + sec) + "\n"
        output += "nroot\n" + self.table_summary.user_input.selectroot_number.text() + "\n"
        output += "selectroot\n" + self.table_summary.user_input.selectroot_number.text() + "\n"
        output += "totsym\n" + self.table_summary.user_input.totsym_number.text() + "\n"
        output += "diracver\n" + ("21" if self.table_summary.user_input.diracver_checkbox.isChecked() else "19") + "\n"
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

        # open dialog to save the file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Input Files (*.inp)")
        if file_path:
            # open the file with write mode
            with open(file_path, "w") as f:
                # get the text from the table widget
                f.write(output)

    def select_file_Dirac(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "SELECT A DIRAC OUTPUT FILE", "", "Output file (*.out)")
        if file_path:
            self.run_sum_Dirac_DFCOEF(file_path)
            self.reload_table(dir_info.sum_dirac_dfcoef_path)

    def select_file_DFCOEF(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "SELECT A sum_dirac_dfcoef OUTPUT FILE", "", "Output file (*.out)"
        )
        if file_path:
            self.reload_table(file_path)

    def save_sum_dirac_dfcoef(self):
        if not os.path.exists(dir_info.sum_dirac_dfcoef_path):
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
        command = f"sum_dirac_dfcoef -i {file_path} -d 3 -c -o {dir_info.sum_dirac_dfcoef_path}"
        # If the OS is Windows, add "python -m" to the command to run the subprocess correctly
        if os.name == "nt":
            command = f"python -m {command}"
        # Run the subprocess
        process = subprocess.run(
            command,
            shell=True,
        )
        # Check the status of the subprocess named process
        if process.returncode != 0:
            QMessageBox.critical(
                self,
                "Error",
                f"An error has ocurred while running the sum_dirac_dfcoef program.\n\
Please check the output file. path: {file_path}\nExecuted command: {command}",
            )

    def reload_table(self, filepath: str):
        self.table_widget.reload(filepath)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            event.accept()

    def dropEvent(self, event="") -> None:
        # Get the file path
        filepath = event.mimeData().text()[8:]
        if not os.path.exists(filepath):
            QMessageBox.critical(
                self,
                "Error",
                "The file does not exist.\n\
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
