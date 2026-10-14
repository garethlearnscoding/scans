import pymupdf
from helper import  build_reorder_map


def reorder_doc(doc:pymupdf.Document) -> pymupdf.Document:
    src = doc
    total_pages = len(src)
    order: list = build_reorder_map(total_pages)

    out = pymupdf.open()
    for src_idx in order:
        out.insert_pdf(src, from_page=src_idx, to_page=src_idx)

    return out
    
