# This script contains all functions to handle settings of this application.

import json
import os

from dcaspt2_input_generator.utils.dir_info import dir_info


class CustomJsonDecodeError(json.decoder.JSONDecodeError):
    def __init__(self, settings_file_path: str):
        self.message = f"settings.json is broken. Please delete the file and restart this application.\n\
File path: {settings_file_path}"
        super().__init__(self.message, self.doc, self.pos)


class DefaultUserInput:
    totsym: int
    selectroot: int
    ras1_max_hole: int
    ras3_max_hole: int
    dirac_ver_21_or_later: bool

    def __init__(self):
        # If the settings.json file exists, read the settings from the file
        if dir_info.setting_file_path.exists():
            with open(dir_info.setting_file_path) as f:
                try:
                    settings = json.load(f)
                    self.totsym = int(settings["totsym"])
                    self.selectroot = int(settings["selectroot"])
                    self.ras1_max_hole = int(settings["ras1_max_hole"])
                    self.ras3_max_electron = int(settings["ras3_max_electron"])
                    self.dirac_ver_21_or_later = settings["dirac_ver_21_or_later"]
                except CustomJsonDecodeError as e:
                    raise CustomJsonDecodeError(dir_info.setting_file_path) from e


class DefaultColorTheme:
    def __init__(self):
        self.color_theme = self.get_color_theme()

    def get_color_theme(self):
        if dir_info.setting_file_path.exists():
            with open(dir_info.setting_file_path) as f:
                try:
                    settings = json.load(f)
                    if "color_theme" in settings:
                        return settings["color_theme"]
                except CustomJsonDecodeError as e:
                    raise CustomJsonDecodeError(dir_info.setting_file_path) from e
        return "default"


class DefaultMultiProcessInput:
    def __init__(self):
        self.multi_process_num = self.get_multi_process_num()

    def get_multi_process_num(self) -> int:
        num_process = 4  # default
        if dir_info.setting_file_path.exists():
            with open(dir_info.setting_file_path) as f:
                try:
                    settings = json.load(f)
                    if "multi_process_num" in settings:
                        num_process = int(settings["multi_process_num"])
                except CustomJsonDecodeError as e:
                    raise CustomJsonDecodeError(dir_info.setting_file_path) from e
        # If the number of CPU cores is less than the number of processes, use the number of CPU cores.
        return min(os.cpu_count(), num_process)


class Settings:
    def __init__(self):
        if not dir_info.setting_file_path.exists():
            self.create_default_settings_file()
        self.input = DefaultUserInput()
        self.color_theme = DefaultColorTheme()
        self.multi_process_input = DefaultMultiProcessInput()

    def create_default_settings_file(self):
        # Application Default Settings
        settings = {
            "totsym": 1,
            "selectroot": 1,
            "ras1_max_hole": 0,
            "ras3_max_electron": 0,
            "dirac_ver_21_or_later": False,
            "color_theme": "default",
            "multi_process_num": 4,
        }
        with open(dir_info.setting_file_path, mode="w") as f:
            json.dump(settings, f, indent=4)


settings = Settings()
