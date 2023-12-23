from typing import Optional

from qtpy.QtGui import QFocusEvent, QIntValidator
from qtpy.QtWidgets import (QCheckBox, QFrame, QGridLayout, QLabel, QLineEdit,
                            QWidget)

from dcaspt2_input_generator.utils.utils import debug_print
from dcaspt2_input_generator.utils.settings import settings


class NaturalNumberInput(QLineEdit):
    bottom_num: int
    default_num: int
    top_num: Optional[int]

    def __init__(self, bottom_num: int = 0, default_num: int = 0):
        super().__init__()
        if default_num < bottom_num:
            msg = f"default_num must be larger than bottom_num. default_num: {default_num}, bottom_num: {bottom_num}"
            raise ValueError(msg)
        self.default_num = default_num
        self.bottom_num = bottom_num
        self.top_num = None
        self.set_validator()
        self.setText(str(self.default_num))
        self.setMaximumWidth(200)

    def set_validator(self):
        validator = QIntValidator()
        if self.top_num is not None:
            validator.setBottom(self.bottom_num)
            validator.setTop(self.top_num)
        else:
            validator.setBottom(self.bottom_num)
        self.setValidator(validator)

    def is_input_valid(self):
        if self.hasAcceptableInput():
            return True
        else:
            return False

    def update_text(self):
        current_text = self.text()
        if current_text == "":
            # If the input is empty, set the default number
            self.setText(str(self.default_num))
        elif self.top_num is not None and int(current_text) > self.top_num:
            self.setText(str(self.top_num))
        elif int(current_text) < self.bottom_num:
            self.setText(str(self.bottom_num))

    def get_value(self):
        return self.text()

    # At the end of the input, the number is validated
    def focusOutEvent(self, arg__1: QFocusEvent) -> None:
        if not self.is_input_valid():  # Validate the input
            debug_print("Invalid input")
            self.update_text()
        return super().focusOutEvent(arg__1)


class RASNumberInput(NaturalNumberInput):
    def __init__(self, bottom_num: int = 0, default_num: int = 0):
        super().__init__(bottom_num, default_num)
        self.setTop(0)

    def setTop(self, top_num: int):
        self.top_num = top_num
        self.set_validator()
        if self.is_input_valid():
            self.update_text()


class UserInput(QGridLayout):
    def __init__(self):
        super().__init__()
        # 数値を入力するためのラベル
        self.ras1_max_hole_label = QLabel("ras1 max hole")
        self.ras1_max_hole_number = RASNumberInput(default_num=settings.input.ras1_max_hole)
        self.ras3_max_electron_label = QLabel("ras3 max electron")
        self.ras3_max_electron_number = RASNumberInput(default_num=settings.input.ras3_max_electron)
        self.totsym_label = QLabel("totsym")
        self.totsym_number = NaturalNumberInput(bottom_num=1, default_num=settings.input.totsym)
        self.selectroot_label = QLabel("selectroot")
        self.selectroot_number = NaturalNumberInput(bottom_num=1, default_num=settings.input.selectroot)
        # Add checkbox
        self.diracver_label = QLabel("Is the version of DIRAC larger than 21?")
        self.diracver_checkbox = QCheckBox()
        self.diracver_checkbox.setChecked(settings.input.dirac_ver_21_or_later)

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

    def get_input_values(self):
        return {
            "totsym": self.totsym_number.get_value(),
            "selectroot": self.selectroot_number.get_value(),
            "ras1_max_hole": self.ras1_max_hole_number.get_value(),
            "ras3_max_electron": self.ras3_max_electron_number.get_value(),
            "dirac_ver_21_or_later": self.diracver_checkbox.isChecked(),
        }


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
        self.recommended_moltra = QLabel("Recommended MOLTRA setting")

        self.summaryLayout.addWidget(QLabel("Summary of the number of spinors"), 0, 0)
        self.summaryLayout.addLayout(self.spinor_summary, 1, 0)
        self.summaryLayout.addWidget(self.recommended_moltra, 2, 0)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.summaryLayout.addWidget(line, 3, 0)

        self.summaryLayout.addWidget(QLabel("User Input"), 4, 0)
        self.summaryLayout.addLayout(self.user_input, 5, 0)

        self.setLayout(self.summaryLayout)
