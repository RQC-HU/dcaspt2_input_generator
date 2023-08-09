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
