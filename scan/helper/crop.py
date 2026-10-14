import pymupdf
from var import CropMode,A4_MARGINS,Margins

def crop_page(
        page:pymupdf.Page, 
        margin:Margins
    ) -> None:
    
    rect = page.rect

    page.set_cropbox(
        pymupdf.Rect(
            rect.x0 + margin.left,
            rect.y0 + margin.top,
            rect.x1 - margin.right,
            rect.y1 - margin.bottom,
        )
    )


def crop_doc(
    doc:pymupdf.Document,
    crop_mode:CropMode,
    margin: list[int] | None
) -> None:
    print(crop_mode)
    if crop_mode == CropMode.NONE or crop_mode is None:
        return
    elif crop_mode == CropMode.DEFAULT:
        margin = A4_MARGINS
    elif crop_mode == CropMode.INP:
        margin = Margins(*margin)
    for page in doc:
        crop_page(page,margin)