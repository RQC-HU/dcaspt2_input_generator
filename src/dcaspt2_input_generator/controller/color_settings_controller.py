from dcaspt2_input_generator.components.color_settings import ColorSettings
from dcaspt2_input_generator.components.data import colors
from dcaspt2_input_generator.components.table_widget import TableWidget
from dcaspt2_input_generator.utils.utils import debug_print


class ColorSettingsController:
    # table_widget: TableWidget
    # color_settings: ColorSettings
    def __init__(self, table_widget: TableWidget, color_settings: ColorSettings):
        self.table_widget = table_widget
        self.color_settings = color_settings

        # Connect signals and slots
        self.color_settings.color_settings_changed.connect(self.onColorSettingsChanged)

    def onColorSettingsChanged(self):
        debug_print("onColorSettingsChanged")
        prev_color = colors.deep_copy()
        selected_button = self.color_settings.buttonGroup.checkedButton()
        color_type = selected_button.text()
        colors.change_color_templates(color_type)
        if prev_color != colors:
            self.table_widget.update_color(prev_color)
