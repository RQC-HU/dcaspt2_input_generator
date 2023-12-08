from qtpy.QtCore import Signal  # type: ignore
from qtpy.QtWidgets import QAction, QButtonGroup, QDialog, QRadioButton, QVBoxLayout, QWidget  # type: ignore


class ColorSettings(QDialog):
    color_settings_changed = Signal()

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        # 3つの選択肢を持つQInputDialogを作成
        self.buttonGroup = QButtonGroup(self)
        self.default_button = QRadioButton("default", self)
        self.default_button.setChecked(True)
        self.red_green_button = QRadioButton("For red-green color blindness", self)
        self.green_yellow_button = QRadioButton("For green-yellow color blindness", self)
        self.buttonGroup.addButton(self.default_button)
        self.buttonGroup.addButton(self.red_green_button)
        self.buttonGroup.addButton(self.green_yellow_button)
        self.buttonGroup.setExclusive(True)
        self.buttonGroup.buttonClicked.connect(self.button_clicked)

        # Add the radio buttons to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.default_button)
        layout.addWidget(self.red_green_button)
        layout.addWidget(self.green_yellow_button)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Show the widget as a dialog
        self.setWindowTitle("Color Settings")
        self.setLayout(layout)

    # When buttonClicked is emitted, the signal is connected to the slot color_settings_changed
    def button_clicked(self):
        self.color_settings_changed.emit()


class ColorSettingsAction(QAction):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.color_settings = ColorSettings()
        self.setText("Color Settings")
        self.triggered.connect(self.openColorSettings)

    def openColorSettings(self):
        self.color_settings.exec_()
