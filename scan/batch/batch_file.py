from pathlib import Path
from single import proc_file
from var import SplitMode,CropMode

def proc_batch(
    split_lst: list[int] | None,
    crop_mode: CropMode,
    margins: list[int] | None,
    split_mode:SplitMode,
    grp_counts: list[int] | None,
    format_string: str = "{stem}_{id}",
):
    folder = Path("input-document")
    for file in folder.glob("*.pdf"):
        proc_file(
            in_file=file.stem,
            crop_mode=crop_mode,
            margins=margins,
            split_mode=split_mode,
            split_lst = split_lst,
            grp_counts= grp_counts,
            format_string=format_string
        )        
