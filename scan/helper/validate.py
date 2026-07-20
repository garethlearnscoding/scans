import argparse
from var import SplitMode

def validate_fs(format_string: str) -> str:
    if "{stem}" not in format_string or "{id}" not in format_string:
        raise argparse.ArgumentTypeError(
            f"Format string is missing required fields: {', '.join(["stem","id"])}"
        )
    
    try:
        format_string.format()
    except Exception as e:
        raise argparse.ArgumentTypeError(
            repr(e)
        )
    
    return format_string


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