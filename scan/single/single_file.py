from pathlib import Path
import pymupdf
from helper import split_doc,crop_doc,reorder_doc
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

    src = pymupdf.open(input_path)

    out = reorder_doc(src)

    # print(crop_mode)
    crop_doc(out,crop_mode,margins)

    out.save("reordered.pdf")

    grps = split_doc(out,split_mode,split_lst,grp_counts)

    stem = input_path.stem
    print(stem)

    print(grps)
    for grp in grps:
        print(grp[0] == None)
        if isinstance(grp[0],str):
            stem = grp[0]
            for id,doc in enumerate(grp[1::],start=1):
                print("hello")
                filename = format_string.format(stem = stem,id = f"{id:02d}")
                out_file = output_path / filename
                doc.save(out_file)
                print(f"PDF saved to: {out_file.stem}")
        else:
    

    src.close()
