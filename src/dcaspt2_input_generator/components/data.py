from dataclasses import dataclass
from typing import Dict

from qtpy.QtGui import QColor


@dataclass
class MOData:
    mo_number: int
    mo_symmetry: str
    energy: float
    ao_type: "list[str]"
    percentage: "list[float]"
    ao_len: int


@dataclass
class SpinorNumber:
    closed_shell: int = 0
    open_shell: int = 0
    virtual_orbitals: int = 0
    sum_of_orbitals: int = 0

    def __add__(self, other: "SpinorNumber") -> "SpinorNumber":
        if not isinstance(other, SpinorNumber):
            msg = f"unsupported operand type(s) for +: {type(self)} and {type(other)}"
            raise TypeError(msg)
        return SpinorNumber(
            self.closed_shell + other.closed_shell,
            self.open_shell + other.open_shell,
            self.virtual_orbitals + other.virtual_orbitals,
            self.sum_of_orbitals + other.sum_of_orbitals,
        )


class MoltraInfo(Dict[str, Dict[int, bool]]):
    pass


class SpinorNumInfo(Dict[str, SpinorNumber]):
    pass


@dataclass
class HeaderInfo:
    spinor_num_info: SpinorNumInfo = None
    moltra_info: MoltraInfo = None
    electron_number: int = 0

    def __post_init__(self):
        if self.spinor_num_info is None:
            self.spinor_num_info = SpinorNumInfo({})
        if self.moltra_info is None:
            self.moltra_info = MoltraInfo({})


class TableData:
    def __init__(self):
        self.mo_data: "list[MOData]" = []
        self.column_max_len: int = 0
        self.header_info: HeaderInfo = HeaderInfo({})

    def reset(self):
        self.mo_data = []
        self.column_max_len = 0
        self.header_info = HeaderInfo({})


table_data = TableData()


@dataclass
class ColorPopupInfo:
    color: QColor
    name: str
    message: str


class Color:
    def __init__(self):
        # Default color
        self.color_type = "default"
        self.change_color_templates(self.color_type)

    def __eq__(self, __value: object):
        if not isinstance(__value, Color):
            return NotImplemented
        # Compare all colors
        if self.core != __value.core:
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
        if q_color.name() in self.colormap:
            return self.colormap[q_color.name()]
        else:
            msg = f"Cannot find the corresponding color. q_color: {q_color.name()}, {q_color.getRgb()}"
            raise ValueError(msg)

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
            msg = f"Invalid color type: {color_type}"
            raise ValueError(msg)
        self.color_type = color_type

        # colormap is a dictionary that maps QColor.name() to ColorPopupInfo
        # QColor is not hashable, so I use QColor.name() instead of QColor for dictionary keys.
        self.colormap = {
            self.core.color.name(): self.core,
            self.inactive.color.name(): self.inactive,
            self.ras1.color.name(): self.ras1,
            self.active.color.name(): self.active,
            self.ras3.color.name(): self.ras3,
            self.secondary.color.name(): self.secondary,
        }


colors = Color()
