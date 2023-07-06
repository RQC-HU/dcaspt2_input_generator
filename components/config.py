from PySide6.QtGui import QColor


class Color:
    def __init__(self):
        # Default color
        self.change_color_templates("default")

    def __eq__(self, __value: object):
        if not isinstance(__value, Color):
            return NotImplemented
        # Compare all colors
        # core
        if self.core != __value.core or self.core_message != __value.core_message:
            return False
        elif self.inactive != __value.inactive or self.inactive_message != __value.inactive_message:
            return False
        elif self.active != __value.active or self.active_message != __value.active_message:
            return False
        elif self.secondary != __value.secondary or self.secondary_message != __value.secondary_message:
            return False
        else:
            return True

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def change_color_templates(self, color_type: str):
        if color_type == "default":
            # Default color
            self.core = QColor("#D3E8EB")
            self.inactive = QColor("#D5ECD4")
            self.active = QColor("#F4D9D9")
            self.secondary = QColor("#FDF4CD")
            self.core_message = "core(Pale Blue)"
            self.inactive_message = "inactive(Pale Green)"
            self.active_message = "active(Pale Pink)"
            self.secondary_message = "secondary(Pale Yellow)"
        elif color_type == "For red-green color blindness":
            # For red-green color blindness
            self.core = QColor("#6495ED")
            self.inactive = QColor("#FFA07A")
            self.active = QColor("#ADFF2F")
            self.secondary = QColor("#DA70D6")
            self.core_message = "core(Cornflower blue)"
            self.inactive_message = "inactive(Light salmon)"
            self.active_message = "active(Green yellow)"
            self.secondary_message = "secondary(Orchid)"
        elif color_type == "For green-yellow color blindness":
            # For green-yellow color blindness
            self.core = QColor("#F08080")
            self.inactive = QColor("#90EE90")
            self.active = QColor("#FFD700")
            self.secondary = QColor("#6A5ACD")
            self.core_message = "core(Light coral)"
            self.inactive_message = "inactive(Light green)"
            self.active_message = "active(Gold)"
            self.secondary_message = "secondary(Slate blue)"
        else:
            raise ValueError("Invalid color type")


colors = Color()


class SpinorMode:
    def __init__(self):
        self.is_spinor_mode = False

    def get_is_spinor_mode(self):
        return self.is_spinor_mode

    def set_is_spinor_mode(self, mode: bool):
        self.is_spinor_mode = mode


spinor_mode = SpinorMode()
