from components.table_summary import TableSummary
from components.table_widget import TableWidget
from components.config import colors
from components.color_info import color_info


class WidgetController:
    def __init__(self, table_summary: TableSummary, table_widget: TableWidget):
        self.table_summary = table_summary
        self.table_widget = table_widget

        # Connect signals and slots
        # change_background_color is a slot
        self.table_widget.colorChanged.connect(self.onTableWidgetColorChanged)

    def onTableWidgetColorChanged(self):
        color_count = {"core": 0, "inactive": 0, "active": 0, "secondary": 0}
        idx_start = {"core": -1, "inactive": -1, "active": -1, "secondary": -1}
        for row in range(self.table_widget.rowCount()):
            color = self.table_widget.item(row, 0).background()
            if color == colors.core:
                if idx_start["core"] == -1:
                    idx_start["core"] = row
                color_count["core"] += 2
            elif color == colors.inactive:
                if idx_start["inactive"] == -1:
                    idx_start["inactive"] = row
                color_count["inactive"] += 2
            elif color == colors.active:
                if idx_start["active"] == -1:
                    idx_start["active"] = row
                color_count["active"] += 2
            elif color == colors.secondary:
                if idx_start["secondary"] == -1:
                    idx_start["secondary"] = row
                color_count["secondary"] += 2

        if idx_start["core"] == -1:
            idx_start["core"] = 0
        if idx_start["inactive"] == -1:
            idx_start["inactive"] = color_count["core"] // 2
        if idx_start["active"] == -1:
            idx_start["active"] = (color_count["core"] + color_count["inactive"]) // 2
        if idx_start["secondary"] == -1:
            idx_start["secondary"] = (color_count["core"] + color_count["inactive"] + color_count["active"]) // 2

        color_info.setIndices(idx_start["inactive"], idx_start["active"], idx_start["secondary"], self.table_widget.rowCount())
        self.table_summary.core_label.setText(f"core: {color_count['core']}")
        self.table_summary.inactive_label.setText(f"inactive: {color_count['inactive']}")
        self.table_summary.active_label.setText(f"active: {color_count['active']}")
        self.table_summary.secondary_label.setText(f"secondary: {color_count['secondary']}")

        # Reload the input
        self.table_summary.core_label.update()
        self.table_summary.inactive_label.update()
        self.table_summary.active_label.update()
        self.table_summary.secondary_label.update()
