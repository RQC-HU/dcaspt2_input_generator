# This script contains all functions to handle settings of this application.

import json
import os

from .dir_info import dir_info


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
            with open(dir_info.setting_file_path, mode="r") as f:
                try:
                    settings = json.load(f)
                    self.totsym = settings["totsym"]
                    self.selectroot = settings["selectroot"]
                    self.ras1_max_hole = settings["ras1_max_hole"]
                    self.ras3_max_hole = settings["ras3_max_hole"]
                    self.dirac_ver_21_or_later = settings["dirac_ver_21_or_later"]
                except CustomJsonDecodeError as e:
                    raise CustomJsonDecodeError(dir_info.setting_file_path) from e


class DefaultColorTheme:
    def __init__(self):
        self.color_theme = self.get_color_theme()

    def get_color_theme(self):
        if dir_info.setting_file_path.exists():
            with open(dir_info.setting_file_path, mode="r") as f:
                try:
                    settings = json.load(f)
                    if "color_theme" in settings:
                        return settings["color_theme"]
                except CustomJsonDecodeError as e:
                    raise CustomJsonDecodeError(dir_info.setting_file_path) from e
        return "default"


class Settings:
    def __init__(self):
        if dir_info.setting_file_path.exists():
            self.create_default_settings_file()
        self.input = DefaultUserInput()
        self.color_theme = DefaultColorTheme()

    def create_default_settings_file(self):
        # Application Default Settings
        settings = {
            "totsym": 1,
            "selectroot": 1,
            "ras1_max_hole": 0,
            "ras3_max_hole": 0,
            "dirac_ver_21_or_later": False,
            "color_theme": "default",
        }
        with open(dir_info.setting_file_path, mode="w") as f:
            json.dump(settings, f, indent=4)
