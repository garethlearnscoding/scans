from pathlib import Path
import fitz
from helper import build_reorder_map,split_doc,crop_doc,reorder_doc
from var import SplitMode, CropMode

def proc_file(
    in_file: str,
    crop_mode: CropMode,
    margins: list[int] | None,
    split_mode:SplitMode,
    split_lst: list[int] | None,
    grp_counts: list[int] | None,
    format_string: str = "{stem}_{id}",
):
    input_path: Path = Path("input-document") / in_file[0]
    output_path: Path = Path("output-document")

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    src = fitz.open(input_path)

    out = reorder_doc(src)

    crop_doc(out,crop_mode,margins)

    grps = split_doc(out,split_mode,split_lst,grp_counts)

    for grp in grps:
        if (stem := grp[0]) is None:
            stem = input_path.stem
        print("STEM:",stem)
        for id,doc in enumerate(grp[1::],start=1):
            filename = format_string.format(stem = stem,id = f"{id:02d}")
            out_file = output_path / filename
            doc.save(out_file)
            print(f"PDF saved to: {out_file.stem}")

    src.close()
