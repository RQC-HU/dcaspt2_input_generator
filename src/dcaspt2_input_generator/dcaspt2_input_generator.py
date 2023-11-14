import os
import sys

from qtpy.QtWidgets import QApplication

from .utils.args import args  # noqa: F401, only import args to parse the command line arguments
from .utils.dir_info import dir_info

# import qt_material


class MainApp:
    def __init__(self):
        from .components.main_window import MainWindow
        from .utils.settings import Settings

        self.app = QApplication(sys.argv)
        self.settings = Settings()
        self.window = MainWindow()
        self.window.setWindowTitle("DIRAC-CASPT2 Input Generator")
        self.window.show()

    def run(self):
        try:
            sys.exit(self.app.exec())
        except SystemExit:
            # Remove the sum_dirac_dfcoef.out file
            if os.path.exists(dir_info.sum_dirac_dfcoef_path):
                os.remove(dir_info.sum_dirac_dfcoef_path)


def main():
    app = MainApp()
    app.run()
