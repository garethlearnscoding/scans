def build_reorder_map(total_pages: int) -> list:
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
