from qtpy.QtCore import Qt
from qtpy.QtWidgets import QHBoxLayout, QLabel
from qtpy.QtCore import Signal  # type: ignore

from components.toggle_button import AnimatedToggle
from components.config import spinor_mode


class ToggleButtonWithLabel(QHBoxLayout):

    toggled = Signal()

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        # トグルボタンとメッセージを配置するレイアウト(右寄せ)
        self.setAlignment(Qt.AlignRight)  # type: ignore
        # トグルボタン
        self.toggle_button = AnimatedToggle(pulse_checked_color="#D3E8EB", pulse_unchecked_color="#D5ECD4")
        self.toggle_button.setFixedSize(60, 40)
        self.toggle_button.clicked.connect(self.toggle_button_clicked)
        # メッセージ
        self.toggle_button_message = QLabel()
        self.set_button_message()
        # 配置(メッセージの右側にトグルボタンを配置)
        self.addWidget(self.toggle_button_message)
        self.addWidget(self.toggle_button)

    def set_button_message(self):
        spinor_mode.set_is_spinor_mode(self.toggle_button.isChecked())
        if spinor_mode.get_is_spinor_mode():
            message = "Spinor mode"
        else:
            message = "MO mode"
        self.toggle_button_message.setText(message)
        self.toggled.emit()

    def toggle_button_clicked(self):
        self.set_button_message()
