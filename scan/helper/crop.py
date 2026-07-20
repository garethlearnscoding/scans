import fitz
from var import CropMode,A4_MARGINS,Margins

def crop_page(
        page:fitz.Page, 
        margin:Margins
    ) -> None:
    
    rect = page.rect

    page.set_cropbox(
        fitz.Rect(
            rect.x0 + margin.left,
            rect.y0 + margin.top,
            rect.x1 - margin.right,
            rect.y1 - margin.bottom,
        )
    )


def crop_doc(
    doc:fitz.Document,
    crop_mode:CropMode,
    margin: list[int] | None
) -> None:
    if crop_mode == CropMode.NONE:
        return
    elif crop_mode == CropMode.DEFAULT:
        margin = A4_MARGINS
    elif crop_mode == CropMode.INP:
        margin = Margins(*margin)
    for page in doc:
        crop_page(page,margin)