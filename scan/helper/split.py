import fitz

def split_doc(
        doc:fitz.Document,
        split_idxs:list[int],
    ) -> list[fitz.Document]:
    """
    Given a finished (reordered + cropped) fitz.Document, split it into up
    to three separate PDFs based on 1-indexed, inclusive page numbers:

      First split: doc[0] ... split_idxs[0]
      Second split: split_idxs[0]+1 ... split_idxs[1]
      .
      .
      .
      Final split: split_idxs[-1]+1 ... doc[-1]

    IndexError will be raised if the maximum file number provided in split_idxs
    is larger than that of the total number of pages of the document.
    """

    total = len(doc)

    split_idxs.sort()

    if (split_idxs[-1] > total) or (split_idxs[0] < 1):
        raise IndexError("Indexes provided are out of range.")
    
    split_idxs = [0] + split_idxs + [total]

    output_docs = []

    for i in range(len(split_idxs)-1):
        part = fitz.open()
        start = split_idxs[i]+1
        end = split_idxs[i+1]
        part.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
        output_docs.append(part)

    return output_docs