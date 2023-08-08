from qtpy.QtWidgets import QGridLayout, QLabel


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
        self.active_label = QLabel("active")
        self.secondary_label = QLabel("secondary")

        # Add the labels and line edits to the layout
        self.addWidget(self.core_label, 0, 0)
        self.addWidget(self.inactive_label, 0, 1)
        self.addWidget(self.active_label, 0, 2)
        self.addWidget(self.secondary_label, 0, 3)