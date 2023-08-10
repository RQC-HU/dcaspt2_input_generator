import copy

from components.color_settings import ColorSettings
from components.table_widget import TableWidget
from components.data import colors


class ColorSettingsController:
    # table_widget: TableWidget
    # color_settings: ColorSettings
    def __init__(self, table_widget: TableWidget, color_settings: ColorSettings):
        self.table_widget = table_widget
        self.color_settings = color_settings

        # Connect signals and slots
        # change_background_color is a slot
        self.color_settings.colorSettingsChanged.connect(self.onColorSettingsChanged)

    def onColorSettingsChanged(self):
        print("onColorSettingsChanged")
        prev_color = copy.deepcopy(colors)
        selected_button = self.color_settings.buttonGroup.checkedButton()
        color_type = selected_button.text()
        colors.change_color_templates(color_type)
        if prev_color != colors:
            self.table_widget.update_color(prev_color)
