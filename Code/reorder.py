import os
import PyPDF2
from PyPDF2.generic import RectangleObject

def reorder_and_crop_pdf(input_path, output_path, crop_points=20):
    ordered_list = []

    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        return

    with open(input_path, "rb") as infile:
        reader = PyPDF2.PdfReader(infile)
        writer = PyPDF2.PdfWriter()

        total_pages = len(reader.pages)

        if total_pages % 2 == 0:
            midpoint = total_pages // 2
            odd_pages = [reader.pages[i] for i in range(midpoint)]
            even_pages = [reader.pages[-i] for i in range(1, midpoint + 1)]
        else:
            midpoint = (total_pages + 1) // 2
            reverse_point = midpoint - 1
            odd_pages = [reader.pages[i] for i in range(midpoint)]
            even_pages = [reader.pages[-i] for i in range(1, reverse_point + 1)]

        for idx, pg in enumerate(odd_pages):
            ordered_list.append(pg)
            if idx < len(even_pages):
                ordered_list.append(even_pages[idx])

        for page in ordered_list:
            writer.add_page(page)

        with open(output_path, "wb") as outfile:
            writer.write(outfile)
        print(f"Reordered PDF saved to: {output_path}")

def batch_reorder_pdfs(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]

    for idx, filename in enumerate(pdf_files, start=1):
        input_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}.pdf"
        output_path = os.path.join(output_folder, output_filename)

        reorder_and_crop_pdf(input_path, output_path)

# Example usage
input_folder = "C:/Users/ryan_/Downloads/School/Admin/Scans/input-document"
output_folder = "C:/Users/ryan_/Downloads/School/Admin/Scans/output-document"

batch_reorder_pdfs(input_folder, output_folder)
