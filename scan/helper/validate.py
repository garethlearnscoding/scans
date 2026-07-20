import argparse
from var import SplitMode, CropMode

def validate_fs(format_string: str) -> str:
    if "{stem}" not in format_string or "{id}" not in format_string:
        raise argparse.ArgumentTypeError(
            f"Format string is missing required fields: {', '.join(["stem","id"])}"
        )
    
    return format_string + ".pdf"


def validate_sm(split_mode:str) -> SplitMode:
    if split_mode is None:
        return SplitMode.NONE
    elif split_mode.upper() == "IDX":
        return SplitMode.IDX
    elif split_mode.upper() == "COUNT":
        return SplitMode.COUNT
    else:
        raise argparse.ArgumentTypeError(
            f"'{split_mode}' is not an available mode to split the document by."
        )
    

def validate_cm(crop_mode:str) -> CropMode:
    if crop_mode is None:
        return CropMode.NONE
    elif crop_mode.upper() == "DEFAULT":
        return CropMode.DEFAULT
    elif crop_mode.upper() == "INP":
        return CropMode.INP
    else:
        raise argparse.ArgumentTypeError(
            f"'{crop_mode}' is not an available mode to crop document pages by."
        )