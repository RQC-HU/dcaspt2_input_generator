import sys

from qtpy.QtWidgets import QApplication

from dcaspt2_input_generator.utils.args import args  # noqa: F401, only import args to parse the command line arguments
from dcaspt2_input_generator.utils.dir_info import dir_info

# import qt_material


class MainApp:
    def __init__(self):
        from dcaspt2_input_generator.components.main_window import MainWindow
        from dcaspt2_input_generator.utils.settings import Settings

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
            dir_info.sum_dirac_dfcoef_path.unlink(missing_ok=True)


def main():
    app = MainApp()
    app.run()
