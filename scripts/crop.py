import fitz
from pathlib import Path
A4_WIDTH = 4603  # points (≈210 mm)
A4_HEIGHT = 6509   # points (≈297 mm)
proc_folder = Path("to-proc")

for doc in proc_folder.glob("*.pdf"):
    pdfdoc = fitz.open(doc)
    for page in pdfdoc:
        rect = page.rect

        if page.number % 2 == 0:
            # Flush top-left
            crop = fitz.Rect(
                rect.x0,
                rect.y0,
                rect.x0 + A4_WIDTH,
                rect.y0 + A4_HEIGHT,
            )
        else:
            # Flush top-right
            crop = fitz.Rect(
                rect.x1 - A4_WIDTH,
                rect.y0,
                rect.x1,
                rect.y0 + A4_HEIGHT,
            )

        page.set_cropbox(crop)
    schl,year,no = doc.stem.split(" ")
    subfolder = f"2MA_PRELIM_{schl}_{year}"
    folder_path = proc_folder / subfolder
    folder_path.mkdir(parents=True,exist_ok=True)
    name = f"2MA_PRELIM_{schl}_{year}_{no}_QP.pdf"
    pdfdoc.save(folder_path/name)
    pdfdoc.close()