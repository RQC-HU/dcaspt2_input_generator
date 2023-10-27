import os
import sys

from qtpy.QtGui import QScreen
from qtpy.QtWidgets import QApplication

# import qt_material


class MainApp:
    def __init__(self):
        from utils.settings import Settings
        from components.main_window import MainWindow

        self.app = QApplication(sys.argv)
        self.user_current_dir = os.getcwd()
        self.app_rootdir = os.path.dirname(os.path.abspath(__file__))
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
            sum_dirac_dfocef_path = os.path.join(self.app_rootdir, "sum_dirac_dfcoef.out")
            if os.path.exists(sum_dirac_dfocef_path):
                os.remove(sum_dirac_dfocef_path)
            self.settings.window_pos.save_window_pos(self.window)
            self.settings.window_size.save_window_size(self.window)


if __name__ == "__main__":
    app = MainApp()
    app.run()
