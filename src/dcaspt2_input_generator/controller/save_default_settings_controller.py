import json

from ..components.data import Color
from ..components.menu_bar import SaveDefaultSettingsAction
from ..components.table_summary import UserInput
from ..utils.dir_info import dir_info


class SaveDefaultSettingsController:
    # app: MainApp
    # color_settings: ColorSettings
    def __init__(self, color: Color, user_input: UserInput, save_default_settings_action: SaveDefaultSettingsAction):
        self.color = color
        self.user_input = user_input
        self.save_default_settings_action = save_default_settings_action

        # Connect signals and slots
        self.save_default_settings_action.saveDefaultSettings.connect(self.save_default_settings)

    def save_default_settings(self):
        # Save current settings in user input and color settings to the settings.json file as default.
        user_input = self.user_input.get_input_values()
        color_setting = self.color.color_type
        user_input["color_theme"] = color_setting
        setting_file_path = dir_info.setting_file_path
        with open(setting_file_path) as f:
            settings = json.load(f)
            print(settings)
            for key, value in user_input.items():
                print(key, value)
                settings.setdefault(key, {})
                settings[key] = value
            print(settings)

        with open(setting_file_path, "w") as f:
            json.dump(settings, f, indent=4)
