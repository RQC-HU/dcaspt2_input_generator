from components.table_widget import TableWidget
from components.toggle_button_with_label import ToggleButtonWithLabel


class ToggleButtonController:
    def __init__(self, toggle_button: ToggleButtonWithLabel, table_widget: TableWidget):
        self.toggle_button = toggle_button
        self.table_widget = table_widget

        # Connect signals and slots
        # change_background_color is a slot
        self.toggle_button.toggled.connect(self.onToggleButtonToggled)

    def onToggleButtonToggled(self):
        print("onToggleButtonToggled")
        self.table_widget.create_table()
