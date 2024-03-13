from dataclasses import dataclass
from typing import Dict, Union
from typing import OrderedDict as ODict

from qtpy.QtGui import QColor, QIcon, QPixmap


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


class MoltraInfo(Dict[str, ODict[int, bool]]):
    pass


class SpinorNumInfo(Dict[str, SpinorNumber]):
    pass


@dataclass
class HeaderInfo:
    spinor_num_info: SpinorNumInfo = None
    moltra_info: MoltraInfo = None
    point_group: Union[str, None] = None
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
    icon: QIcon


class Color:
    def __init__(self):
        # Default color
        self.color_type = "default"
        self.change_color_templates(self.color_type)

    def __eq__(self, __value: object):
        if not isinstance(__value, Color):
            return NotImplemented
        # Compare all colors
        if self.inactive != __value.inactive:
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

    def deep_copy(self):
        new_color = Color()
        new_color.color_type = self.color_type
        new_color.colormap = self.colormap.copy()

        for key, value in self.__dict__.items():
            if isinstance(value, ColorPopupInfo):
                setattr(new_color, key, value)

        new_color.not_used.icon = self.create_icon(new_color.not_used.color)
        new_color.inactive.icon = self.create_icon(new_color.inactive.color)
        new_color.ras1.icon = self.create_icon(new_color.ras1.color)
        new_color.active.icon = self.create_icon(new_color.active.color)
        new_color.ras3.icon = self.create_icon(new_color.ras3.color)
        new_color.secondary.icon = self.create_icon(new_color.secondary.color)

        return new_color

    def get_color_info(self, q_color: QColor):
        if q_color.name() in self.colormap:
            return self.colormap[q_color.name()]
        else:
            msg = f"Cannot find the corresponding color. q_color: {q_color.name()}, {q_color.getRgb()}"
            raise ValueError(msg)

    def create_icon(self, color: QColor, size=64):
        pixmap = QPixmap(size, size)
        pixmap.fill(color)
        icon = QIcon(pixmap)
        return icon

    def change_color_templates(self, color_type: str):
        if color_type == "default":
            # Default color
            color_not_used, msg_not_used, msg_color_not_used = (
                QColor("#FFFFFF"),
                "not used in CASPT2",
                "not used in CASPT2(White)",
            )
            color_inactive, msg_inactive, msg_color_inactive = QColor("#D5ECD4"), "inactive", "inactive(Pale Green)"
            color_ras1, msg_ras1, msg_color_ras1 = QColor("#BBA0CB"), "ras1", "ras1(Pale Purple)"
            color_active, msg_active, msg_color_active = QColor("#F4D9D9"), "active", "active, ras2(Pale Pink)"
            color_ras3, msg_ras3, msg_color_ras3 = QColor("#FFB7C5"), "ras3", "ras3(Pastel Pink)"
            color_secondary, msg_secondary, msg_color_secondary = (
                QColor("#FDF4CD"),
                "secondary",
                "secondary(Pale Yellow)",
            )
            self.not_used = ColorPopupInfo(
                color_not_used, msg_not_used, msg_color_not_used, self.create_icon(color_not_used)
            )
            self.inactive = ColorPopupInfo(
                color_inactive, msg_inactive, msg_color_inactive, self.create_icon(color_inactive)
            )
            self.ras1 = ColorPopupInfo(color_ras1, msg_ras1, msg_color_ras1, self.create_icon(color_ras1))
            self.active = ColorPopupInfo(color_active, msg_active, msg_color_active, self.create_icon(color_active))
            self.ras3 = ColorPopupInfo(color_ras3, msg_ras3, msg_color_ras3, self.create_icon(color_ras3))
            self.secondary = ColorPopupInfo(
                color_secondary, msg_secondary, msg_color_secondary, self.create_icon(color_secondary)
            )
        elif color_type == "Color type 1":
            # Color type 1
            not_used, msg_not_used, msg_color_not_used = (
                QColor("#FFFFFF"),
                "not used in CASPT2",
                "not used in CASPT2(White)",
            )
            color_inactive, msg_inactive, msg_color_inactive = QColor("#FFA07A"), "inactive", "inactive(Light salmon)"
            color_ras1, msg_ras1, msg_color_ras1 = QColor("#32CD32"), "ras1", "ras1(Lime green)"
            color_active, msg_active, msg_color_active = QColor("#ADFF2F"), "active", "active, ras2(Green yellow)"
            color_ras3, msg_ras3, msg_color_ras3 = QColor("#FFFF00"), "ras3", "ras3(Yellow)"
            color_secondary, msg_secondary, msg_color_secondary = (
                QColor("#DA70D6"),
                "secondary",
                "secondary(Orchid)",
            )
            self.not_used = ColorPopupInfo(not_used, msg_not_used, msg_color_not_used, self.create_icon(not_used))
            self.inactive = ColorPopupInfo(
                color_inactive, msg_inactive, msg_color_inactive, self.create_icon(color_inactive)
            )
            self.ras1 = ColorPopupInfo(color_ras1, msg_ras1, msg_color_ras1, self.create_icon(color_ras1))
            self.active = ColorPopupInfo(color_active, msg_active, msg_color_active, self.create_icon(color_active))
            self.ras3 = ColorPopupInfo(color_ras3, msg_ras3, msg_color_ras3, self.create_icon(color_ras3))
            self.secondary = ColorPopupInfo(
                color_secondary, msg_secondary, msg_color_secondary, self.create_icon(color_secondary)
            )
        elif color_type == "Color type 2":
            # Color type 2
            not_used, msg_not_used, msg_color_not_used = (
                QColor("#FFFFFF"),
                "not used in CASPT2",
                "not used in CASPT2(White)",
            )
            color_inactive, msg_inactive, msg_color_inactive = QColor("#FFA07A"), "inactive", "inactive(Light salmon)"
            color_ras1, msg_ras1, msg_color_ras1 = QColor("#FFD700"), "ras1", "ras1(Gold)"
            color_active, msg_active, msg_color_active = QColor("#FF1493"), "active", "active, ras2(Deep pink)"
            color_ras3, msg_ras3, msg_color_ras3 = QColor("#4682B4"), "ras3", "ras3(Steel blue)"
            color_secondary, msg_secondary, msg_color_secondary = (
                QColor("#6A5ACD"),
                "secondary",
                "secondary(Slate blue)",
            )
            self.not_used = ColorPopupInfo(not_used, msg_not_used, msg_color_not_used, self.create_icon(not_used))
            self.inactive = ColorPopupInfo(
                color_inactive, msg_inactive, msg_color_inactive, self.create_icon(color_inactive)
            )
            self.ras1 = ColorPopupInfo(color_ras1, msg_ras1, msg_color_ras1, self.create_icon(color_ras1))
            self.active = ColorPopupInfo(color_active, msg_active, msg_color_active, self.create_icon(color_active))
            self.ras3 = ColorPopupInfo(color_ras3, msg_ras3, msg_color_ras3, self.create_icon(color_ras3))
            self.secondary = ColorPopupInfo(
                color_secondary, msg_secondary, msg_color_secondary, self.create_icon(color_secondary)
            )
        else:
            msg = f"Invalid color type: {color_type}"
            raise ValueError(msg)
        self.color_type = color_type

        # colormap is a dictionary that maps QColor.name() to ColorPopupInfo
        # QColor is not hashable, so I use QColor.name() instead of QColor for dictionary keys.
        self.colormap = {
            self.not_used.color.name(): self.not_used,
            self.inactive.color.name(): self.inactive,
            self.ras1.color.name(): self.ras1,
            self.active.color.name(): self.active,
            self.ras3.color.name(): self.ras3,
            self.secondary.color.name(): self.secondary,
        }


colors = Color()
