from dataclasses import dataclass

@dataclass
class Margins:
    left: int
    right: int
    top: int
    bottom: int

A4_MARGINS = Margins(
    left = 28,
    right = 28,
    top =0,
    bottom= 179
)