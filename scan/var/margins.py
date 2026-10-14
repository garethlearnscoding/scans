from dataclasses import dataclass

@dataclass
class Margins:
    left: int
    right: int
    top: int
    bottom: int

# If scan was for full area (document feeder)
A4_MARGINS = Margins(
    left = 14,
    right = 14,
    top =0,
    bottom= 250
)
# A4_MARGINS = Margins(
#     left = 0,
#     right = 0,
#     top =0,
#     bottom= 0
# )