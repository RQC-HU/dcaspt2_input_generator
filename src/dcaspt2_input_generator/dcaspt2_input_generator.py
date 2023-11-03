import os
import sys

from qtpy.QtGui import QScreen
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
        is_window_size_loaded = self.settings.window_size.windowSizeLoadedOnStartUp
        if is_window_size_loaded:
            width, height = self.settings.window_size.width, self.settings.window_size.height
        else:
            width, height = int(QScreen.availableGeometry(QApplication.primaryScreen()).width() * (2 / 3)), int(
                QScreen.availableGeometry(QApplication.primaryScreen()).height() * (2 / 3)
            )
        self.window.resize(width, height)
        is_window_pos_loaded = self.settings.window_pos.windowPositionLoadedOnStartUp
        if is_window_pos_loaded:
            # If the window position is loaded from the settings.json file, use the loaded position
            # But if the window position exceeds the screen size, modify the position
            # Set the window position
            self.window.move(self.settings.window_pos.posx, self.settings.window_pos.posy)
        self.window.show()
        if not is_window_pos_loaded:
            # If the window position is not loaded from the settings.json file, get the current window position
            # and save it to the settings.json file for the next time
            self.settings.window_pos.save_window_pos(self.window)
        if not is_window_size_loaded:
            self.settings.window_size.save_window_size(self.window)

    def run(self):
        try:
            sys.exit(self.app.exec())
        except SystemExit:
            # Remove the sum_dirac_dfcoef.out file
            if os.path.exists(dir_info.sum_dirac_dfcoef_path):
                os.remove(dir_info.sum_dirac_dfcoef_path)
            self.settings.window_pos.save_window_pos(self.window)
            self.settings.window_size.save_window_size(self.window)


def main():
    app = MainApp()
    app.run()
