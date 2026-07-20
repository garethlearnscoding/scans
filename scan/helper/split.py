import fitz
from itertools import zip_longest
from var import SplitMode

def split_by_page_no(
        doc:fitz.Document,
        split_idxs:list[int],
    ) -> list[fitz.Document]:
    """
    Splits a fitz.Document object into three separate 
    documents based on 1-indexed, via page numbers(inclusive):

      First  doc: doc[0] ... split_idxs[0]
      Second doc: split_idxs[0]+1 ... split_idxs[1]
      .
      .
      .
      Final  doc: split_idxs[-1]+1 ... doc[-1]

    IndexError will be raised if the maximum file number provided in 
    split_idxs is larger than that of the total number of pages of the 
    document.
    """

    total = len(doc)

    split_idxs.sort()

    if (split_idxs[-1] > total) or (split_idxs[0] < 1):
        raise IndexError("Page numbers provided are out of range.")
    
    split_idxs = [0] + split_idxs + [total]

    output_docs = []

    for i in range(len(split_idxs)-1):
        part = fitz.open()

        start = split_idxs[i]+1

        end = split_idxs[i+1]

        part.insert_pdf(doc, from_page=start - 1, to_page=end - 1)

        output_docs.append(part)


    return output_docs

def split_by_no_of_pages(
        doc:fitz.Document,
        page_counts: list[int],
) -> list[fitz.Document]:
    """
    Splits a fitz.Document object into three separate 
    documents via number of pages.
    
    IndexError will be raised if the maximum file number provided in 
    split_idxs is larger than that of the total number of pages of the 
    document.
    """

    total = len(doc)
    provided_count = sum(page_counts)

    if provided_count > total:
        raise IndexError("Total pages provide exceeds source document total page count.")
    
    if provided_count < total:
        page_counts.append(total-provided_count)

    start = 0
    output_docs = []

    for i in range(len(page_counts)):

        part = fitz.open()

        end = start + page_counts[i]

        part.insert_pdf(doc, from_page=start, to_page=end - 1)

        output_docs.append(part)

        start = end

    return output_docs

def group_splits(
        output_docs:list[fitz.Document],
        grp_counts:int | list[int] | None,
) -> list[tuple[fitz.Document]]:
    
    if grp_counts is None:
        grouped_docs = [tuple(output_docs)]

    elif isinstance(grp_counts,int):
        grouped_docs = list(zip_longest(output_docs[::grp_counts],output_docs[1::grp_counts]))

    elif isinstance(grp_counts,list):
        if sum(grp_counts) > len(output_docs):
            raise IndexError("Total provided counts for grouping exceeds number of available documents.")
        
        grouped_docs = []
        i = 0
        
        for c in grp_counts:
            grouped_docs.append(tuple(output_docs[i:i + c]))
            i += c
        
    return grouped_docs


def split_doc(
        doc:fitz.Document,
        mode: SplitMode,
        split_lst: list[int],
        grp_counts: list[int]
) -> list[tuple[fitz.Document]]:
    
    if mode == SplitMode.IDX:
        docs = split_by_page_no(doc,split_lst)

    elif mode == SplitMode.COUNT:
        docs = split_by_no_of_pages(doc,split_lst)
    
    elif mode == SplitMode.NONE:
        docs = doc
        
    else:
        raise KeyError("Split mode provided is incorrect.")
        
    output_docs = group_splits(docs,grp_counts)
    
    return output_docs
