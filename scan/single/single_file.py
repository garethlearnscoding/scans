from pathlib import Path
import fitz
from helper import build_reorder_map,split_doc,crop_doc,reorder_doc

def proc_file(
    in_file: str,
    split_idxs: list[int] | None = None,
    margins: list[int] | None = None,
    format_string: str = "{stem}_{id}"
):
    input_path: Path = Path("input-document") / in_file
    output_path: Path = Path("ouput-document")

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    src = fitz.open(input_path)

    out = [reorder_doc(src)]
    
    if margins is not None:
        crop_doc(out[0],*margins)

    if split_idxs is not None:
        out = split_doc(out[0],split_idxs)

    stem = input_path.stem

    for id,doc in enumerate(out):
        filename = format_string.format(stem = stem,id = id)
        doc.save(output_path / filename)
        print(f"PDF saved to: {output_path.stem}")

    src.close()
