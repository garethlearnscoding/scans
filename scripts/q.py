from pathlib import Path
import fitz


A4_PORTRAIT = fitz.paper_rect("a4")
A4_LANDSCAPE = fitz.Rect(0, 0, A4_PORTRAIT.height, A4_PORTRAIT.width)


def build_reorder_map(total_pages: int) -> list[int]:
    """
    Returns the list of 0-indexed source page numbers in their correct
    final reading order, given a scan that contains all odd pages first
    followed by all even pages in reverse order.
    """
    if total_pages % 2 == 0:
        midpoint = total_pages // 2
        odd_pages = list(range(midpoint))
        even_pages = list(range(total_pages - 1, midpoint - 1, -1))
    else:
        midpoint = (total_pages + 1) // 2
        odd_pages = list(range(midpoint))
        even_pages = list(range(total_pages - 1, midpoint - 1, -1))

    ordered = []
    for i, odd in enumerate(odd_pages):
        ordered.append(odd)
        if i < len(even_pages):
            ordered.append(even_pages[i])

    return ordered


def reorder_doc(src: fitz.Document) -> fitz.Document:
    order = build_reorder_map(len(src))

    out = fitz.open()

    for src_idx in order:
        src_page = src[src_idx]

        # Determine the displayed page size (includes rotation)
        rect = src_page.rect

        if rect.width > rect.height:
            page_rect = A4_LANDSCAPE
        else:
            page_rect = A4_PORTRAIT

        new_page = out.new_page(
            width=page_rect.width,
            height=page_rect.height,
        )

        new_page.show_pdf_page(
            page_rect,
            src,
            src_idx,
            keep_proportion=True,
        )

    return out


if __name__ == "__main__":
    src = fitz.open("./input-document/2EC_Prelim_RevisionPackage.pdf")
    out = reorder_doc(src)
    out.save("./output-document/2EC_Prelim_RevisionPackage.pdf")
    out.close()
    src.close()