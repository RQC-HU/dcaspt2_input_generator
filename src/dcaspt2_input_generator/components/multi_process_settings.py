import os

from qtpy.QtCore import Signal
from qtpy.QtWidgets import QAction, QDialog, QSpinBox, QVBoxLayout

from dcaspt2_input_generator.utils.settings import settings


class MultiProcessSettingDialog(QDialog):
    multi_process_changed = Signal()

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Set Process Number for sum_dirac_dfcoef calculation")
        self.resize(400, 50)
        self.multi_process_spin_box = QSpinBox()
        self.multi_process_spin_box.setRange(1, os.cpu_count())
        self.multi_process_spin_box.setValue(settings.multi_process_input.multi_process_num)
        self.multi_process_spin_box.valueChanged.connect(self.onMultiProcessDialogChanged)

        layout = QVBoxLayout()
        layout.addWidget(self.multi_process_spin_box)
        self.setLayout(layout)

    def onMultiProcessDialogChanged(self):
        self.multi_process_changed.emit()


class MultiProcessDialogAction(QAction):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.multi_process_settings = MultiProcessSettingDialog()
        self.setText("Multi Process Settings")
        self.triggered.connect(self.openMultiProcessDialogSettings)

    def openMultiProcessDialogSettings(self):
        self.multi_process_settings.exec_()
