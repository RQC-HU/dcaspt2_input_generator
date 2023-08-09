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
    color: QColor = QColor()

class TableData:
    def __init__(self):
        self.mo_data: list[MOData] = []
        self.column_max_len: int = 0

    def reset(self):
        self.mo_data = []
        self.column_max_len = 0


table_data = TableData()


class ColorInfo:
    _instance = None

    index_info: dict[str, tuple[int, int]] = {"core": (-1, -1), "inactive": (-1, -1), "active": (-1, -1), "secondary": (-1, -1)}
    ras: list[list[int]] = [[] for _ in range(3)]

    # Singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # 各色の開始位置、終了位置を格納する
    def setIndices(self, inactive_start, active_start, secondary_start, length):
        self.index_info["core"] = (0, inactive_start - 1)
        self.index_info["inactive"] = (inactive_start, active_start - 1)
        self.index_info["active"] = (active_start, secondary_start - 1)
        self.index_info["secondary"] = (secondary_start, length - 1)


color_info = ColorInfo()
