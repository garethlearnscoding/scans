from pathlib import Path
import fitz
from helper import  build_reorder_map


def reorder_doc(doc:fitz.Document) -> fitz.Document:
    src = doc
    total_pages = len(src)
    order: list = build_reorder_map(total_pages)

    out = fitz.open()
    for src_idx in order:
        out.insert_pdf(src, from_page=src_idx, to_page=src_idx)

    out.close()
    return out
    
