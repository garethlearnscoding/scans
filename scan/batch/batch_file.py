from pathlib import Path
import fitz
from single import proc_file

def proc_batch(
    margins: list[int] | None = None,
    format_string: str = "{stem}_{id}"

):
    folder = Path("input-document")
    for file in folder.glob("*.pdf"):
        proc_file(file.stem,margins=margins,format_string=format_string)