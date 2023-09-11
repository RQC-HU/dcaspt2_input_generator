from components.table_summary import TableSummary
from components.table_widget import TableWidget
from components.data import colors


class WidgetController:
    def __init__(self, table_summary: TableSummary, table_widget: TableWidget):
        self.table_summary = table_summary
        self.table_widget = table_widget

        # Connect signals and slots
        # change_background_color is a slot
        self.table_widget.colorChanged.connect(self.onTableWidgetColorChanged)

    def onTableWidgetColorChanged(self):
        color_count = {"core": 0, "inactive": 0, "ras1": 0, "active, ras2": 0, "ras3": 0, "secondary": 0}
        for row in range(self.table_widget.rowCount()):
            color = self.table_widget.item(row, 0).background()
            if color == colors.core.color:
                color_count["core"] += 2
            elif color == colors.inactive.color:
                color_count["inactive"] += 2
            elif color == colors.ras1.color:
                color_count["ras1"] += 2
            elif color == colors.active.color:
                color_count["active, ras2"] += 2
            elif color == colors.ras3.color:
                color_count["ras3"] += 2
            elif color == colors.secondary.color:
                color_count["secondary"] += 2

        self.table_summary.spinor_summary.core_label.setText(f"core: {color_count['core']}")
        self.table_summary.spinor_summary.inactive_label.setText(f"inactive: {color_count['inactive']}")
        self.table_summary.spinor_summary.ras1_label.setText(f"ras1: {color_count['ras1']}")
        self.table_summary.spinor_summary.active_label.setText(f"active, ras2: {color_count['active, ras2']}")
        self.table_summary.spinor_summary.ras3_label.setText(f"ras3: {color_count['ras3']}")
        self.table_summary.spinor_summary.secondary_label.setText(f"secondary: {color_count['secondary']}")

        # Reload the input
        self.table_summary.update()
