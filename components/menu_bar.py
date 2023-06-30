from qtpy.QtCore import Signal  # type: ignore
from qtpy.QtWidgets import QMenuBar, QAction  # type: ignore

from components.color_settings import ColorSettingsAction


class MenuBar(QMenuBar):
    colorSettingsChanged = Signal()

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

        self.file_menu = self.addMenu("Settings")
        self.color_settings_action = ColorSettingsAction()
        self.file_menu.addAction(self.color_settings_action)
