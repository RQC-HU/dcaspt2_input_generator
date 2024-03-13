from qtpy.QtCore import Signal
from qtpy.QtGui import QFocusEvent, QIntValidator
from qtpy.QtWidgets import QFrame, QGridLayout, QLabel, QLineEdit, QWidget

from dcaspt2_input_generator.utils.settings import settings
from dcaspt2_input_generator.utils.utils import debug_print


class NaturalNumberInput(QLineEdit):
    default_num: int
    validator: QIntValidator

    def __init__(self, bottom_num: int = 0, default_num: int = 0):
        super().__init__()
        if default_num < bottom_num:
            msg = f"default_num must be larger than bottom_num. default_num: {default_num}, bottom_num: {bottom_num}"
            raise ValueError(msg)
        self.default_num = default_num
        self.__setup_validator__(bottom_num)
        self.setText(str(self.default_num))
        self.setMaximumWidth(200)

    def __setup_validator__(self, bottom_num: int):
        self.validator = QIntValidator()
        self.validator.setBottom(bottom_num)
        self.setValidator(self.validator)

    def set_top(self, top_num: int):
        self.validator.setTop(top_num)
        if not self.is_input_valid():
            self.update_text()

    def is_input_valid(self):
        if self.hasAcceptableInput():
            return True
        else:
            return False

    def update_text(self):
        current_val = self.get_value()
        if int(current_val) > self.validator.top():
            self.setText(str(self.validator.top()))
        elif int(current_val) < self.validator.bottom():
            self.setText(str(self.validator.bottom()))
        elif self.default_num > self.validator.top():
            self.setText(str(self.validator.top()))
        else:
            self.setText(str(self.default_num))

    def get_value(self) -> int:
        try:
            return int(self.text())
        except ValueError:
            return self.bottom_num

    # At the end of the input, the number is validated
    def focusOutEvent(self, arg__1: QFocusEvent) -> None:
        if not self.is_input_valid():  # Validate the input
            debug_print("Invalid input")
            self.update_text()
        return super().focusOutEvent(arg__1)


class TotsymNumberInput(NaturalNumberInput):
    def __init__(self, changed: Signal, default_num: int, bottom_num: int = 1):
        super().__init__(bottom_num, default_num)
        self.changed = changed

    def focusOutEvent(self, arg__1: QFocusEvent) -> None:
        super().focusOutEvent(arg__1)
        self.changed.emit()


class UserInput(QGridLayout):
    changed = Signal()

    def __init__(self):
        super().__init__()
        # 数値を入力するためのラベル
        self.totsym_label = QLabel("totsym")
        self.totsym_number = TotsymNumberInput(self.changed, default_num=settings.input.totsym)
        self.selectroot_label = QLabel("selectroot")
        self.selectroot_number = NaturalNumberInput(bottom_num=1, default_num=settings.input.selectroot)
        self.diracver_label = QLabel("DIRAC major version (if 21.1, type 21)")
        self.dirac_ver_number = NaturalNumberInput(bottom_num=12, default_num=settings.input.dirac_ver)
        self.ras1_max_hole_label = QLabel("ras1 max hole")
        self.ras1_max_hole_number = NaturalNumberInput(default_num=settings.input.ras1_max_hole)
        self.ras3_max_electron_label = QLabel("ras3 max electron")
        self.ras3_max_electron_number = NaturalNumberInput(default_num=settings.input.ras3_max_electron)

        self.addWidget(self.totsym_label, 0, 0)
        self.addWidget(self.totsym_number, 0, 1)
        self.addWidget(self.selectroot_label, 0, 2)
        self.addWidget(self.selectroot_number, 0, 3)
        self.addWidget(self.diracver_label, 0, 4)
        self.addWidget(self.dirac_ver_number, 0, 5)
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
            "dirac_ver": self.dirac_ver_number.get_value(),
        }


class SpinorSummary(QGridLayout):
    def __init__(self):
        super().__init__()
        # Create the labels
        self.inactive_label = QLabel("inactive")
        self.ras1_label = QLabel("ras1")
        self.active_label = QLabel("active, ras2")
        self.ras3_label = QLabel("ras3")
        self.secondary_label = QLabel("secondary")

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
        self.point_group = QLabel("Point Group")

        self.summaryLayout.addWidget(QLabel("Summary of the number of spinors"), 0, 0)
        self.summaryLayout.addLayout(self.spinor_summary, 1, 0)
        self.summaryLayout.addWidget(self.recommended_moltra, 2, 0)
        self.summaryLayout.addWidget(self.point_group, 3, 0)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.summaryLayout.addWidget(line, 4, 0)

        self.summaryLayout.addWidget(QLabel("User Input"), 5, 0)
        self.summaryLayout.addLayout(self.user_input, 6, 0)

        self.setLayout(self.summaryLayout)
