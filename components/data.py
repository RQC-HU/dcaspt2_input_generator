from dataclasses import dataclass
from qtpy.QtGui import QColor


@dataclass
class MOData:
    mo_number: int
    mo_symmetry: str
    energy: float
    ao_type: list[str]
    percentage: list[float]
    ao_len: int


class TableData:
    def __init__(self):
        self.mo_data: list[MOData] = []
        self.column_max_len: int = 0

    def reset(self):
        self.mo_data = []
        self.column_max_len = 0


table_data = TableData()


@dataclass
class ColorPopupInfo:
    color: QColor = QColor()
    message: str = ""


class Color:
    def __init__(self):
        # Default color
        self.change_color_templates("default")

    def __eq__(self, __value: object):
        if not isinstance(__value, Color):
            return NotImplemented
        # Compare all colors
        # core
        if self.core.color != __value.core.color:
            return False
        elif self.inactive != __value.inactive:
            return False
        elif self.ras1 != __value.ras1:
            return False
        elif self.active != __value.active:
            return False
        elif self.ras3 != __value.ras3:
            return False
        elif self.secondary != __value.secondary:
            return False
        else:
            return True

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def change_color_templates(self, color_type: str):
        if color_type == "default":
            # Default color
            self.core = ColorPopupInfo(QColor("#D3E8EB"), "core(Pale Blue)")
            self.inactive = ColorPopupInfo(QColor("#D5ECD4"), "inactive(Pale Green)")
            self.ras1 = ColorPopupInfo(QColor("#BBA0CB"), "ras1(Pale Purple)")
            self.active = ColorPopupInfo(QColor("#F4D9D9"), "active, ras2(Pale Pink)")
            self.ras3 = ColorPopupInfo(QColor("#FFB7C5"), "ras3(Pastel Pink)")
            self.secondary = ColorPopupInfo(QColor("#FDF4CD"), "secondary(Pale Yellow)")
        elif color_type == "For red-green color blindness":
            # For red-green color blindness
            self.core = ColorPopupInfo(QColor("#6495ED"), "core(Cornflower blue)")
            self.inactive = ColorPopupInfo(QColor("#FFA07A"), "inactive(Light salmon)")
            self.ras1 = ColorPopupInfo(QColor("#32CD32"), "ras1(Lime green)")
            self.active = ColorPopupInfo(QColor("#ADFF2F"), "active, ras2(Green yellow)")
            self.ras3 = ColorPopupInfo(QColor("#FFFF00"), "ras3(Yellow)")
            self.secondary = ColorPopupInfo(QColor("#DA70D6"), "secondary(Orchid)")
        elif color_type == "For green-yellow color blindness":
            # For green-yellow color blindness
            self.core = ColorPopupInfo(QColor("#F08080"), "core(Light coral)")
            self.inactive = ColorPopupInfo(QColor("#90EE90"), "inactive(Light green)")
            self.ras1 = ColorPopupInfo(QColor("#4682B4"), "ras1(Steel blue)")
            self.active = ColorPopupInfo(QColor("#FF1493"), "active, ras2(Deep pink)")
            self.ras3 = ColorPopupInfo(QColor("#FFD700"), "ras3(Gold)")
            self.secondary = ColorPopupInfo(QColor("#6A5ACD"), "secondary(Slate blue)")
        else:
            raise ValueError("Invalid color type")


colors = Color()
