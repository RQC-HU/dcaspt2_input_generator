from qtpy.QtWidgets import QGridLayout, QLabel, QLineEdit
from qtpy.QtGui import QIntValidator


class NaturalNumberInput(QLineEdit):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        varidator = QIntValidator(bottom=0)  # type: ignore
        self.setValidator(varidator)
        self.setText("0")
        # サイズはとっても小さくする
        self.setMaximumWidth(200)


# TableSummary provides the layout for the input data
# like the following: ([ ] = line edit)
# core   inactive    active    secondary
# [  ]     [  ]       [  ]       [ ]
class TableSummary(QGridLayout):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        # Create the labels
        self.core_label = QLabel("core")
        self.inactive_label = QLabel("inactive")
        self.ras1_label = QLabel("ras1")
        self.active_label = QLabel("active, ras2")
        self.ras3_label = QLabel("ras3")
        self.secondary_label = QLabel("secondary")
        # 数値を入力するためのラベル
        self.ras1_max_hole_label = QLabel("ras1 max hole")
        self.ras1_max_hole_number = NaturalNumberInput()
        self.ras3_max_electron_label = QLabel("ras3 max electron")
        self.ras3_max_electron_number = NaturalNumberInput()
        # Add the labels and line edits to the layout
        self.addWidget(self.core_label, 0, 0)
        self.addWidget(self.inactive_label, 0, 1)
        self.addWidget(self.ras1_label, 0, 2)
        self.addWidget(self.active_label, 0, 3)
        self.addWidget(self.ras3_label, 0, 4)
        self.addWidget(self.secondary_label, 0, 5)
        self.addWidget(self.ras1_max_hole_label, 1, 0)
        self.addWidget(self.ras1_max_hole_number, 1, 1)
        self.addWidget(self.ras3_max_electron_label, 1, 2)
        self.addWidget(self.ras3_max_electron_number, 1, 3)
