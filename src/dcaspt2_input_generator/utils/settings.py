# This script contains all functions to handle settings of this application.

import json
import os
from typing import Dict, Union

from dcaspt2_input_generator.utils.dir_info import dir_info


class CustomJsonDecodeError(json.decoder.JSONDecodeError):
    def __init__(self, settings_file_path: str):
        self.message = f"settings.json is broken. Please delete the file and restart this application.\n\
File path: {settings_file_path}"
        super().__init__(self.message, self.doc, self.pos)


class UserInput:
    totsym: int
    selectroot: int
    ras1_max_hole: int
    ras3_max_hole: int
    dirac_ver: int

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
                    self.dirac_ver = int(settings["dirac_ver"])
                except KeyError as e:
                    msg = f"settings.json is broken. missing key: {e},\
please delete {dir_info.setting_file_path}and restart this application."
                    raise KeyError(msg) from e
                except CustomJsonDecodeError as e:
                    raise CustomJsonDecodeError(dir_info.setting_file_path) from e


class ColorTheme:
    def __init__(self):
        self.theme_list = ["default", "Color type 1", "Color type 2"]
        self.theme_name = self.get_color_theme_name()

    def get_color_theme_name(self):
        key = "color_theme"
        if dir_info.setting_file_path.exists():
            with open(dir_info.setting_file_path) as f:
                try:
                    settings = json.load(f)
                    if key in settings and settings[key] in self.theme_list:
                        return settings[key]
                except CustomJsonDecodeError as e:
                    raise CustomJsonDecodeError(dir_info.setting_file_path) from e
        return "default"


class MultiProcess:
    def __init__(self):
        self.multi_process_num = self.__init_multi_process_num__()

    def __init_multi_process_num__(self) -> int:
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
        # Application Default Settings
        self.default_settings: Dict[str, Union[int, str]] = {
            "totsym": 1,
            "selectroot": 1,
            "ras1_max_hole": 0,
            "ras3_max_electron": 0,
            "dirac_ver": 23,
            "color_theme": "default",
            "multi_process_num": 4,
        }
        if not dir_info.setting_file_path.exists():
            self.create_default_settings_file()
        self.input = UserInput()
        self.color_theme = ColorTheme()
        self.multi_process_input = MultiProcess()

    def create_default_settings_file(self):
        with open(dir_info.setting_file_path, mode="w") as f:
            json.dump(self.default_settings, f, indent=4)


settings = Settings()
