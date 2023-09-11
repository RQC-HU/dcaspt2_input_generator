from dataclasses import dataclass
from qtpy.QtGui import QColor


@dataclass
class MOData:
    mo_number: int
    mo_symmetry: str
    energy: float
    ao_type: "list[str]"
    percentage: "list[float]"
    ao_len: int


class TableData:
    def __init__(self):
        self.mo_data: "list[MOData]" = []
        self.column_max_len: int = 0

    def reset(self):
        self.mo_data = []
        self.column_max_len = 0


table_data = TableData()


@dataclass
class ColorPopupInfo:
    color: QColor
    name: str
    message: str


class Color:
    def __init__(self):
        # Default color
        self.change_color_templates(color_type="default")

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

    def get_color_info(self, q_color: QColor):
        # QColor is not hashable, so I use QColor.name() instead of QColor for dictionary keys.
        colormap = {
            self.core.color.name(): self.core,
            self.inactive.color.name(): self.inactive,
            self.ras1.color.name(): self.ras1,
            self.active.color.name(): self.active,
            self.ras3.color.name(): self.ras3,
            self.secondary.color.name(): self.secondary,
        }
        if q_color.name() in colormap:
            return colormap[q_color.name()]
        else:
            raise ValueError(f"Cannot find the corresponding color. q_color: {q_color.name()}, {q_color.getRgb()}")

    def change_color_templates(self, color_type: str):
        if color_type == "default":
            # Default color
            self.core = ColorPopupInfo(QColor("#D3E8EB"), "core", "core(Pale Blue)")
            self.inactive = ColorPopupInfo(QColor("#D5ECD4"), "inactive", "inactive(Pale Green)")
            self.ras1 = ColorPopupInfo(QColor("#BBA0CB"), "ras1", "ras1(Pale Purple)")
            self.active = ColorPopupInfo(QColor("#F4D9D9"), "active", "active, ras2(Pale Pink)")
            self.ras3 = ColorPopupInfo(QColor("#FFB7C5"), "ras3", "ras3(Pastel Pink)")
            self.secondary = ColorPopupInfo(QColor("#FDF4CD"), "secondary", "secondary(Pale Yellow)")
        elif color_type == "For red-green color blindness":
            # For red-green color blindness
            self.core = ColorPopupInfo(QColor("#6495ED"), "core", "core(Cornflower blue)")
            self.inactive = ColorPopupInfo(QColor("#FFA07A"), "inactive", "inactive(Light salmon)")
            self.ras1 = ColorPopupInfo(QColor("#32CD32"), "ras1", "ras1(Lime green)")
            self.active = ColorPopupInfo(QColor("#ADFF2F"), "active", "active, ras2(Green yellow)")
            self.ras3 = ColorPopupInfo(QColor("#FFFF00"), "ras3", "ras3(Yellow)")
            self.secondary = ColorPopupInfo(QColor("#DA70D6"), "secondary", "secondary(Orchid)")
        elif color_type == "For green-yellow color blindness":
            # For green-yellow color blindness
            self.core = ColorPopupInfo(QColor("#F08080"), "core", "core(Light coral)")
            self.inactive = ColorPopupInfo(QColor("#90EE90"), "inactive", "inactive(Light green)")
            self.ras1 = ColorPopupInfo(QColor("#4682B4"), "ras1", "ras1(Steel blue)")
            self.active = ColorPopupInfo(QColor("#FF1493"), "active", "active, ras2(Deep pink)")
            self.ras3 = ColorPopupInfo(QColor("#FFD700"), "ras3", "ras3(Gold)")
            self.secondary = ColorPopupInfo(QColor("#6A5ACD"), "secondary", "secondary(Slate blue)")
        else:
            raise ValueError("Invalid color type")


colors = Color()
