import fitz

def crop_page(
        page:fitz.Page, 
        left:int, 
        right:int, 
        top:int, 
        bottom:int
    ) -> None:
    
    rect = page.rect

    page.set_cropbox(
        fitz.Rect(
            rect.x0 + left,
            rect.y0 + top,
            rect.x1 - right,
            rect.y1 - bottom,
        )
    )


def crop_doc(
    doc:fitz.Document,
    left:int = 15,
    right:int = 15,
    top:int =0,
    bottom:int = 125
) -> None:
    for page in doc:
        crop_page(page,left,right,top,bottom)