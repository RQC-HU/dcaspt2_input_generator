from typing import Optional

from qtpy.QtCore import QEvent
from qtpy.QtGui import QIntValidator
from qtpy.QtWidgets import QGridLayout, QLabel, QLineEdit, QCheckBox, QWidget, QFrame

class NaturalNumberInput(QLineEdit):
    bottom_num: int
    default_num: int
    top_num: Optional[int]

    def __init__(self, bottom_num: int = 0, default_num: int = 0, top_num: Optional[int] = None):
        super().__init__()
        if default_num < bottom_num:
            raise ValueError(
                f"default_num must be larger than bottom_num. default_num: {default_num}, bottom_num: {bottom_num}"
            )
        self.bottom_num = bottom_num
        self.default_num = default_num
        self.top_num = top_num
        self.init()

    def set_validator(self):
        if self.top_num is not None:
            validator = QIntValidator(bottom=self.bottom_num, top=self.top_num)
        else:
            validator = QIntValidator(bottom=self.bottom_num)
        self.setValidator(validator)

    def set_default_num(self, default_num: int):
        self.default_num = default_num

    def set_bottom_num(self, bottom_num: int):
        self.bottom_num = bottom_num
        self.set_validator()

    def set_top_num(self, top_num: int):
        self.top_num = top_num
        self.set_validator()

    def is_input_valid(self):
        if self.hasAcceptableInput():
            return True
        else:
            return False

    def init(self):
        self.set_validator()
        self.setText(str(self.default_num))
        self.setMaximumWidth(200)

    # At the end of the input, the number is validated
    def focusOutEvent(self, arg__1: QEvent) -> None:
        if not self.is_input_valid():  # Validate the input
            print("Invalid input")
            self.setText(str(self.default_num))
        return super().focusOutEvent(arg__1)

class UserInput(QGridLayout):
    def __init__(self):
        super().__init__()
        # 数値を入力するためのラベル
        self.ras1_max_hole_label = QLabel("ras1 max hole")
        self.ras1_max_hole_number = NaturalNumberInput()
        self.ras3_max_electron_label = QLabel("ras3 max electron")
        self.ras3_max_electron_number = NaturalNumberInput()
        self.totsym_label = QLabel("totsym")
        self.totsym_number = NaturalNumberInput(bottom_num=1, default_num=1)
        self.selectroot_label = QLabel("selectroot")
        self.selectroot_number = NaturalNumberInput(bottom_num=1, default_num=1)
        # Add checkbox
        self.diracver_label = QLabel("Is the version of DIRAC larger than 21?")
        self.diracver_checkbox = QCheckBox()

        self.addWidget(self.totsym_label, 0, 0)
        self.addWidget(self.totsym_number, 0, 1)
        self.addWidget(self.selectroot_label, 0, 2)
        self.addWidget(self.selectroot_number, 0, 3)
        self.addWidget(self.diracver_label, 0, 4)
        self.addWidget(self.diracver_checkbox, 0, 5)
        self.addWidget(self.ras1_max_hole_label, 1, 0)
        self.addWidget(self.ras1_max_hole_number, 1, 1)
        self.addWidget(self.ras3_max_electron_label, 1, 2)
        self.addWidget(self.ras3_max_electron_number, 1, 3)


class SpinorSummary(QGridLayout):
    def __init__(self):
        super().__init__()
        # Create the labels
        self.core_label = QLabel("core")
        self.inactive_label = QLabel("inactive")
        self.ras1_label = QLabel("ras1")
        self.active_label = QLabel("active, ras2")
        self.ras3_label = QLabel("ras3")
        self.secondary_label = QLabel("secondary")

        self.addWidget(self.core_label, 0, 0)
        self.addWidget(self.inactive_label, 0, 1)
        self.addWidget(self.ras1_label, 0, 2)
        self.addWidget(self.active_label, 0, 3)
        self.addWidget(self.ras3_label, 0, 4)
        self.addWidget(self.secondary_label, 0, 5)


# TableSummary provides the layout for the input data
# The layout is like this:
class TableSummary(QWidget):
    def __init__(self):
        super().__init__()
        self.summaryLayout = QGridLayout()
        self.spinor_summary = SpinorSummary()
        self.user_input = UserInput()

        self.summaryLayout.addWidget(QLabel("Summary of the number of spinors"), 0, 0)
        self.summaryLayout.addLayout(self.spinor_summary, 1, 0)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.summaryLayout.addWidget(line, 2, 0)

        self.summaryLayout.addWidget(QLabel("User Input"), 3, 0)
        self.summaryLayout.addLayout(self.user_input, 4, 0)

        self.setLayout(self.summaryLayout)
