import argparse

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