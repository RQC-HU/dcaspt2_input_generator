from qtpy.QtCore import Qt
from qtpy.QtWidgets import QHBoxLayout, QLabel

from components.toggle_button import AnimatedToggle
from components.config import is_display_mode


class ToggleButtonWithLabel(QHBoxLayout):
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
        is_display_mode.set_display_mode(self.toggle_button.isChecked())
        if is_display_mode.get_display_mode():
            message = "Spinor mode"
        else:
            message = "MO mode"
        self.toggle_button_message.setText(message)

    def toggle_button_clicked(self):
        self.set_button_message()
