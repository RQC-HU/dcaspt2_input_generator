# This script contains all functions to handle settings of this application.

import os
import json
from typing import Dict

from ..components.dir_info import dir_info
from ..components.main_window import MainWindow


class CustomJsonDecodeError(json.decoder.JSONDecodeError):
    #  print f"settings.json is broken. Please delete the file and restart this application.\n\
    # File path: {settings_file_path}"

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
        settings_file_path = dir_info.setting_file_path
        if os.path.exists(settings_file_path):
            setting_file_path = os.path.abspath(settings_file_path)
            with open("settings.json", "r") as f:
                try:
                    settings = json.load(f)
                    self.totsym = settings["totsym"]
                    self.selectroot = settings["selectroot"]
                    self.ras1_max_hole = settings["ras1_max_hole"]
                    self.ras3_max_hole = settings["ras3_max_hole"]
                    self.dirac_ver_21_or_later = settings["dirac_ver_21_or_later"]
                except CustomJsonDecodeError:
                    raise CustomJsonDecodeError(setting_file_path)


class WindowSize:
    def __init__(self):
        self.width: int = 0
        self.height: int = 0
        self.windowSizeLoadedOnStartUp = False

    def get_window_size_from_setting_file(self):
        if os.path.exists(dir_info.setting_file_path):
            with open(dir_info.setting_file_path) as f:
                try:
                    settings = json.load(f)
                    if (
                        "window_size" in settings
                        and "width" in settings["window_size"]
                        and "height" in settings["window_size"]
                    ):
                        # Get the window position from the settings.json file
                        self.width = settings["window_size"]["width"]
                        self.height = settings["window_size"]["height"]
                        self.windowSizeLoadedOnStartUp = True
                except CustomJsonDecodeError:
                    raise CustomJsonDecodeError(dir_info.setting_file_path)

    def save_window_size(self, window: MainWindow):
        # Get the current window position
        width, height = window.size().width(), window.size().height()
        # Save the window position to the settings.json file
        with open(dir_info.setting_file_path) as f:
            settings: Dict = json.load(f)
            settings.setdefault("window_size", {})
            settings["window_size"]["width"] = width
            settings["window_size"]["height"] = height

        with open(dir_info.setting_file_path, "w") as f:
            json.dump(settings, f, indent=4)


class WindowPosition:
    def __init__(self):
        self.posx: int = 0
        self.posy: int = 0
        self.windowPositionLoadedOnStartUp = False

    def get_window_pos_from_setting_file(self):
        if os.path.exists(dir_info.setting_file_path):
            with open(dir_info.setting_file_path) as f:
                try:
                    settings = json.load(f)
                    if (
                        "window_pos" in settings
                        and "posx" in settings["window_pos"]
                        and "posy" in settings["window_pos"]
                    ):
                        # Get the window position from the settings.json file
                        self.posx = settings["window_pos"]["posx"]
                        self.posy = settings["window_pos"]["posy"]
                        self.windowPositionLoadedOnStartUp = True
                except CustomJsonDecodeError:
                    raise CustomJsonDecodeError(dir_info.setting_file_path)

    def save_window_pos(self, window: MainWindow):
        # Get the current window position
        posx, posy = window.geometry().x(), window.geometry().y()
        # Save the window position to the settings.json file
        with open(dir_info.setting_file_path) as f:
            settings: Dict = json.load(f)
            settings.setdefault("window_pos", {})
            settings["window_pos"]["posx"] = posx
            settings["window_pos"]["posy"] = posy

        with open(dir_info.setting_file_path, "w") as f:
            json.dump(settings, f, indent=4)


class DefaultColorTheme:
    def __init__(self):
        self.setting_file_path = dir_info.setting_file_path
        self.color_theme = self.get_color_theme()

    def get_color_theme(self):
        if os.path.exists(self.setting_file_path):
            with open(self.setting_file_path) as f:
                try:
                    settings = json.load(f)
                    if "color_theme" in settings:
                        return settings["color_theme"]
                except CustomJsonDecodeError:
                    raise CustomJsonDecodeError(self.setting_file_path)
        return "default"


class Settings:
    def __init__(self):
        self.setting_file_path = dir_info.setting_file_path
        self.window_pos = WindowPosition()
        self.window_pos.get_window_pos_from_setting_file()
        self.window_size = WindowSize()
        self.window_size.get_window_size_from_setting_file()
        if not os.path.exists(self.setting_file_path):
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
        with open(self.setting_file_path, "w") as f:
            json.dump(settings, f, indent=4)

    def save_window_pos(self, window):
        self.window_pos.save_window_pos(window)
