from enum import Enum, auto

class SplitMode(Enum):
    IDX = auto()
    COUNT = auto()
    NONE = auto()
    
class CropMode(Enum):
    NONE = auto()
    DEFAULT = auto()
    INP = auto()