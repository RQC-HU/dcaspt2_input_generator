import os
import sys

from qtpy.QtWidgets import QApplication

from dcaspt2_input_generator.utils.args import args  # noqa: F401, only import args to parse the command line arguments
from dcaspt2_input_generator.utils.dir_info import dir_info

# import qt_material


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.init_gui()

    def init_gui(self):
        from dcaspt2_input_generator.components.main_window import MainWindow

        self.window = MainWindow(parent=None)
        self.window.setWindowTitle("DIRAC-CASPT2 Input Generator")
        self.window.show()

    def run(self):
        try:
            sys.exit(self.app.exec())
        except SystemExit:
            # Remove the sum_dirac_dfcoef.out file
            if dir_info.sum_dirac_dfcoef_path.exists():
                os.remove(dir_info.sum_dirac_dfcoef_path)


def main():
    app = MainApp()
    app.run()
