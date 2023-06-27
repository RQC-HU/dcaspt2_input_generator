from PySide6.QtGui import QColor


class Color:
    def __init__(self):
        # Default color
        self.core = QColor("#D3E8EB")
        self.inactive = QColor("#D5ECD4")
        self.active = QColor("#F4D9D9")
        self.secondary = QColor("#FDF4CD")
        self.core_message = "core(Pale Blue)"
        self.inactive_message = "inactive(Pale Green)"
        self.active_message = "active(Pale Pink)"
        self.secondary_message = "secondary(Pale Yellow)"

        # # For red-green color blindness
        # self.core = QColor("#6495ED")
        # self.inactive = QColor("#FFA07A")
        # self.active = QColor("#ADFF2F")
        # self.secondary = QColor("#DA70D6")
        # self.core_message = "core(Cornflower blue)"
        # self.inactive_message = "inactive(Light salmon)"
        # self.active_message = "active(Green yellow)"
        # self.secondary_message = "secondary(Orchid)"

        # # For green-yellow color blindness
        # self.core = QColor("#F08080")
        # self.inactive = QColor("#90EE90")
        # self.active = QColor("#FFD700")
        # self.secondary = QColor("#6A5ACD")
        # self.core_message = "core(Light coral)"
        # self.inactive_message = "inactive(Light green)"
        # self.active_message = "active(Gold)"
        # self.secondary_message = "secondary(Slate blue)"


colors = Color()


class DisplayMode:
    def __init__(self):
        self.display_mode = False

    def get_display_mode(self):
        return self.display_mode

    def set_display_mode(self, mode: bool):
        self.display_mode = mode


is_display_mode = DisplayMode()
