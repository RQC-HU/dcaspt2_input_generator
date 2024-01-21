from dcaspt2_input_generator.utils.settings import settings
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QAction, QDialog, QSpinBox, QVBoxLayout


class MultiProcessSettings(QDialog):
    # 質問と回答を受け取る
    # 回答はinteger, natural number

    multi_process_changed = Signal()

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Set Process Number for sum_dirac_dfcoef calculation")
        self.resize(400, 50)
        self.multi_process_spin_box = QSpinBox()
        self.multi_process_spin_box.setRange(1, 100)
        self.multi_process_spin_box.setValue(settings.multi_process_input.multi_process_num)
        self.multi_process_spin_box.valueChanged.connect(self.onMultiProcessChanged)

        layout = QVBoxLayout()
        layout.addWidget(self.multi_process_spin_box)
        self.setLayout(layout)

    def onMultiProcessChanged(self):
        self.multi_process_changed.emit()


class MultiProcessAction(QAction):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.multi_process_settings = MultiProcessSettings()
        self.setText("Multi Process Settings")
        self.triggered.connect(self.openMultiProcessSettings)

    def openMultiProcessSettings(self):
        self.multi_process_settings.exec_()
