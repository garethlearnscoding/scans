import sys
import argparse
from pathlib import Path
import numpy as np
import fitz  # PyMuPDF   -> pip install pymupdf


# ---------------------------------------------------------------------------
# CROPPING
# ---------------------------------------------------------------------------

def get_content_bbox(page, dpi=150, white_thresh=250):
    """
    Render a page to a bitmap and find the bounding box of all 'non-white'
    (i.e. actual ink/content) pixels. Returns the bbox in PDF point
    coordinates, or None if the page looks blank.
    """
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)

    w, h, stride = pix.width, pix.height, pix.stride
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(h, stride)[:, :w]

    dark_mask = arr < white_thresh
    if not dark_mask.any():
        return None

    rows = np.where(dark_mask.any(axis=1))[0]
    cols = np.where(dark_mask.any(axis=0))[0]
    min_y, max_y = rows[0], rows[-1]
    min_x, max_x = cols[0], cols[-1]

    scale = 72.0 / dpi
    x0, y0 = min_x * scale, min_y * scale
    x1, y1 = (max_x + 1) * scale, (max_y + 1) * scale
    return fitz.Rect(x0, y0, x1, y1)


def crop_page(page, dpi=300, padding=6, white_thresh=250):
    """Auto-crop a single page in place to its detected content bbox."""
    bbox = get_content_bbox(page, dpi=dpi, white_thresh=white_thresh)
    if bbox is None:
        return  # blank page, leave it alone

    page_rect = page.rect
    bbox.x0 = max(page_rect.x0, bbox.x0 - padding)
    bbox.y0 = max(page_rect.y0, bbox.y0 - padding)
    bbox.x1 = min(page_rect.x1, bbox.x1 + padding)
    bbox.y1 = min(page_rect.y1, bbox.y1 + padding)
    page.set_cropbox(bbox)


def crop_page_manual_margins(page, left=0, top=0, right=0, bottom=0):
    """
    Trim fixed margins (in points, 72pt = 1 inch) off each edge of a page.
    e.g. crop_page_manual_margins(page, left=20, top=15, right=20, bottom=40)
    shaves 20pt off the left/right and 15pt/40pt off the top/bottom.
    """
    r = page.rect  # r.x0, r.y0 = top-left; r.x1, r.y1 = bottom-right
    bbox = fitz.Rect(r.x0 + left, r.y0 + top, r.x1 - right, r.y1 - bottom)
    page.set_cropbox(bbox)


def crop_page_manual_rect(page, x0, y0, x1, y1):
    """
    Set the crop box to an exact rectangle, in PDF points, measured from
    the TOP-LEFT of the page (x0,y0) to the bottom-right (x1,y1).
    e.g. crop_page_manual_rect(page, 20, 30, 590, 800)
    """
    page.set_cropbox(fitz.Rect(x0, y0, x1, y1))


# ---------------------------------------------------------------------------
# REORDERING (odd pages scanned first, then even pages in reverse order)
# ---------------------------------------------------------------------------

def build_reorder_map(total_pages):
    """
    Returns the list of 0-indexed source page numbers in their correct
    final reading order, given a scan that contains all odd pages first
    (in order), followed by all even pages (in reverse order).
    """
    if total_pages % 2 == 0:
        midpoint = total_pages // 2
        odd_pages = list(range(midpoint))
        even_pages = [total_pages - i for i in range(1, midpoint + 1)]
    else:
        midpoint = (total_pages + 1) // 2
        reverse_point = midpoint - 1
        odd_pages = list(range(midpoint))
        even_pages = [total_pages - i for i in range(1, reverse_point + 1)]

    ordered = []
    for idx, p in enumerate(odd_pages):
        ordered.append(p)
        if idx < len(even_pages):
            ordered.append(even_pages[idx])
    return ordered


# ---------------------------------------------------------------------------
# SPLITTING (into Paper 1 / 2 / 3 by page number, 1-indexed, inclusive)
# ---------------------------------------------------------------------------

def split_into_papers(doc, output_path: Path, split1: int, split2: int):
    """
    Given a finished (reordered + cropped) fitz.Document, split it into up
    to three separate PDFs based on 1-indexed, inclusive page numbers:
      Paper 1: pages 1 .. split1
      Paper 2: pages split1+1 .. split2
      Paper 3: pages split2+1 .. end
    Each paper is saved next to output_path, named "<stem> - Paper N.pdf".
    Ranges that fall outside the document (e.g. split2 >= total pages, so
    there is no Paper 3) are skipped.
    """
    total = len(doc)

    if not (0 < split1 < split2 <= total):
        print(
            f"  Invalid split points ({split1}, {split2}) for a "
            f"{total}-page document — saving without splitting instead."
        )
        doc.save(output_path)
        print(f"Reordered + cropped PDF saved to: {output_path}")
        return

    ranges = [
        ("Paper 1", 1, split1),
        ("Paper 2", split1 + 1, split2),
        ("Paper 3", split2 + 1, total),
    ]

    for label, start, end in ranges:
        if start > end:
            continue  # e.g. split2 == total, so there's no Paper 3
        part = fitz.open()
        part.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
        part_path = output_path.parent / f"{output_path.stem} - {label}{output_path.suffix}"
        part.save(part_path)
        part.close()
        print(f"  {label} (pages {start}-{end}) saved to: {part_path}")


# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------

def reorder_and_crop_pdf(
    input_path: Path,
    output_path: Path,
    crop_mode="auto",       # "auto" | "margins" | "rect" | "none"
    dpi=300,
    padding=6,
    white_thresh=250,
    margins=None,           # dict: {"left":.., "top":.., "right":.., "bottom":..}
    rect=None,              # tuple: (x0, y0, x1, y1)
    split1=None,            # last page (1-indexed) of Paper 1
    split2=None,            # last page (1-indexed) of Paper 2
):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    src = fitz.open(input_path)
    total_pages = len(src)
    order = build_reorder_map(total_pages)

    out = fitz.open()
    for src_idx in order:
        out.insert_pdf(src, from_page=src_idx, to_page=src_idx)

    for page in out:
        if crop_mode == "auto":
            crop_page(page, dpi=dpi, padding=padding, white_thresh=white_thresh)
        elif crop_mode == "margins":
            m = margins or {}
            crop_page_manual_margins(
                page,
                left=m.get("left", 0),
                top=m.get("top", 0),
                right=m.get("right", 0),
                bottom=m.get("bottom", 0),
            )
        elif crop_mode == "rect":
            if rect is None:
                raise ValueError("crop_mode='rect' requires a rect=(x0,y0,x1,y1) argument")
            crop_page_manual_rect(page, *rect)
        elif crop_mode == "none":
            pass
        else:
            raise ValueError(f"Unknown crop_mode: {crop_mode!r}")

    if split1 is not None and split2 is not None:
        split_into_papers(out, output_path, split1, split2)
    else:
        out.save(output_path)
        print(f"Reordered + cropped PDF saved to: {output_path}")

    out.close()
    src.close()


def batch_reorder_and_crop_pdfs(input_folder: Path, output_folder: Path, **crop_kwargs):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    pdf_files = [p for p in input_folder.iterdir() if p.suffix.lower() == ".pdf"]

    for input_path in pdf_files:
        output_path = output_folder / input_path.name
        reorder_and_crop_pdf(input_path, output_path, **crop_kwargs)


if __name__ == "__main__":
    input_folder = Path("input-document")
    output_folder = Path("output-document")

    # --- CLI usage ---
    #   python run.py                          -> batch mode, no split (as before)
    #   python run.py -p 12 24                 -> batch mode, split every file
    #   python run.py -f paper.pdf             -> single-file mode, no split
    #   python run.py -f paper.pdf -p 12 24    -> single-file mode, with split
    # -f and -p can be given in either order.
    parser = argparse.ArgumentParser(description="Reorder, crop, and optionally split scanned test papers.")
    parser.add_argument("-f", "--file", type=str, default=None,
                         help="Process a single PDF instead of the whole input folder.")
    parser.add_argument("-p", "--pages", type=int, nargs=2, default=None,
                         metavar=("SPLIT1", "SPLIT2"),
                         help="Last page (1-indexed) of Paper 1 and of Paper 2. Paper 3 is everything after.")
    args = parser.parse_args()

    split1, split2 = (None, None) if args.pages is None else tuple(args.pages)
    if split1 is not None and split1 >= split2:
        print("split1 must be less than split2.")
        sys.exit(1)

    # --- pick ONE crop mode to use below ---
    crop_kwargs = dict(
        # 1) Auto-detect content and crop to it
        # crop_mode="auto",

        # 2) Manually trim fixed margins off every page (in points, 72pt = 1 inch)
        crop_mode="margins",
        margins={"left": 28, "top": 0, "right": 28, "bottom": 195},

        # 3) Manually set an exact crop rectangle for every page (in points,
        #    measured from the top-left corner of the page)
        # crop_mode="rect",
        # rect=(20, 30, 590, 800),
    )

    if args.file:
        # Single-file mode: -f name.pdf on its own, or a full/relative path.
        input_path = Path(args.file)
        if not input_path.exists():
            input_path = input_folder / args.file
        output_path = output_folder / input_path.name
        reorder_and_crop_pdf(input_path, output_path, split1=split1, split2=split2, **crop_kwargs)
    else:
        batch_reorder_and_crop_pdfs(
            input_folder, output_folder,
            split1=split1, split2=split2,
            **crop_kwargs,
        )