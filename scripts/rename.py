from pathlib import Path

proc_folder = Path("to-proc")

for doc in proc_folder.glob("*.pdf"):
    sch,no,doc_type = doc.stem.split(" ")
    filename = f"1GP_PRELIM_2025_{sch}_{no}{doc_type}.pdf"
    filepath = proc_folder / filename
    # filepath = folder_path / filename
    doc.rename(filepath)

