import subprocess

from qtpy.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QInputDialog, QPushButton
from qtpy.QtGui import QDragEnterEvent


from components.menu_bar import MenuBar
from components.table_summary import TableSummary
from components.table_widget import TableWidget
from components.data import table_data
from components.config import colors
from components.toggle_button_with_label import ToggleButtonWithLabel
from controller.color_settings_controller import ColorSettingsController
from controller.toggle_button_controller import ToggleButtonController
from controller.widget_controller import WidgetController


# Layout for the main window
# File, Settings
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

        # Body
        self.toggle_button_with_label = ToggleButtonWithLabel()
        self.table_summary = TableSummary()
        self.table_widget = TableWidget()
        # Add Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_input)

        # Create an instance of WidgetController
        self.widget_controller = WidgetController(self.table_summary, self.table_widget)
        self.color_settings_controller = ColorSettingsController(self.table_widget, self.menu_bar.color_settings_action.color_settings)
        self.toggle_button_controller = ToggleButtonController(self.toggle_button_with_label, self.table_widget)
        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.menu_bar)
        layout.addLayout(self.toggle_button_with_label)
        layout.addWidget(self.table_widget)
        layout.addLayout(self.table_summary)
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
        for idx, row in enumerate(table_data.spinor_data):
            color = row["color"]
            if color == colors.core:
                print(idx, "core")
                core += 1
            elif color == colors.inactive:
                print(idx, "inactive")
                inact += 1
            elif color == colors.active:
                print(idx, "active")
                act += 1
            elif color == colors.secondary:
                print(idx, "secondary")
                sec += 1
        output += "core\n" + str(core) + "\n"
        output += "inactive\n" + str(inact) + "\n"
        output += "active\n" + str(act) + "\n"
        output += "secondary\n" + str(sec) + "\n"

        # open dialog to save the file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if file_path:
            # open the file with write mode
            with open(file_path, "w") as f:
                # get the text from the table widget
                f.write(output)

    def select_file_Dirac(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "SELECT A DIRAC OUTPUT FILE", "", "Output file (*.out)")
        if file_path:
            molecule_name = ""
            while molecule_name == "":
                molecule_name, _ = self.questionMolecule()
            # Run sum_dirac_defcoef subprocess
            self.run_sum_Dirac_DFCOEF(file_path, molecule_name)
            self.reload_table(molecule_name + ".out")

    def select_file_DFCOEF(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "SELECT A sum_dirac_dfcoef OUTPUT FILE", "", "Output file (*.out)")
        if file_path:
            self.reload_table(file_path)

    def questionMolecule(self):
        # Show a question message box that allow the user to write the molecule name
        molecule_name, ok = QInputDialog.getText(
            self,
            "Molecule formula",
            "Enter the molecule formula that you calculated using DIRAC:",
        )
        return molecule_name, ok

    def run_sum_Dirac_DFCOEF(self, file_path, molecule_name):
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

    def reload_table(self, output_path: str):
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
        self.reload_table(filepath)
