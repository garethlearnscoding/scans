from pathlib import Path
import fitz
from helper import build_reorder_map,split_doc,crop_doc,reorder_doc
from var import SplitMode

def proc_file(
    in_file: str,
    split_lst: list[int] | None,
    margins: list[int] | None,
    mode:SplitMode,
    grp_counts: list[int] | None,
    format_string: str = "{stem}_{id}",


):
    input_path: Path = Path("input-document") / in_file
    output_path: Path = Path("ouput-document")

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    src = fitz.open(input_path)

    out = reorder_doc(src)
    
    if margins is not None:
        crop_doc(out,*margins)

    
    grps = split_doc(out,mode,split_lst,grp_counts)

    stem = input_path.stem

    for grp in grps:
        for id,doc in enumerate(grp,start=1):
            filename = format_string.format(stem = stem,id = id)
            doc.save(output_path / filename)
            print(f"PDF saved to: {output_path.stem}")

    src.close()
