from qtpy.QtCore import Signal  # type: ignore
from qtpy.QtWidgets import QAction, QMenuBar  # type: ignore

from dcaspt2_input_generator.components.color_settings import ColorSettingsAction


class SaveDefaultSettingsAction(QAction):
    signal_save_default_settings = Signal()

    def __init__(self):
        super().__init__()
        self.setText("Save current settings as default")
        self.triggered.connect(self.signal_save_default_settings)

    def save_default_settings(self):
        self.signal_save_default_settings.emit()


class AboutAction(QAction):
    # クリックしたらバージョン情報などを表示する

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Version")
        self.triggered.connect(self.about)

    def about(self):
        from qtpy.QtWidgets import QMessageBox, QWidget

        from dcaspt2_input_generator.__about__ import __version__

        msg = f"Version: {__version__}"
        QMessageBox.about(QWidget(), "Version info", msg)


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        # Create the menu bar
        self.file_menu = self.addMenu("File")
        self.open_action_dirac = QAction("Open with DIRAC output", self)
        self.file_menu.addAction(self.open_action_dirac)
        self.open_action_dfcoef = QAction("Open with sum_dirac_dfcoef output", self)
        self.file_menu.addAction(self.open_action_dfcoef)
        self.save_action_input = QAction("Save input file", self)
        self.file_menu.addAction(self.save_action_input)
        self.save_action_dfcoef = QAction("Save sum_dirac_dfcoef file", self)
        self.file_menu.addAction(self.save_action_dfcoef)

        self.file_menu = self.addMenu("Settings")
        self.color_settings_action = ColorSettingsAction()
        self.save_default_settings_action = SaveDefaultSettingsAction()
        self.file_menu.addAction(self.color_settings_action)
        self.file_menu.addAction(self.save_default_settings_action)

        # クリックしたらバージョン情報などを表示する
        self.file_menu = self.addMenu("About")
        self.about_action = AboutAction("About")
        self.file_menu.addAction(self.about_action)
