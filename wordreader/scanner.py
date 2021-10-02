"""Module for scanning files and searching specified words in them."""

import os
from typing import Callable, Dict, Iterable, List, Optional

from wordreader import formats_handler


def find_in_single_file(
    search_word: str,
    filename: str,
    case_sensitive: Optional[bool] = True,
) -> List[str]:
    """
    Find specified word in single file.

    Args:
        search_word (str): word to search in file.
        filename (str): name of file to search in.
        case_sensitive (Optional[bool]): case sensitive search.

    Returns:
        List[str]: list with lines where the word is found.
        If word is not found, list is empty.

    """
    file_extension: str = filename.split('.')[-1]
    file_handler: Optional[Callable] = getattr(
        formats_handler,
        'split_{0}_file'.format(file_extension),
        None,
    )
    found_lines: List[str] = []

    if file_handler and os.path.exists(filename):
        found_lines = file_handler(search_word, filename)
        found_lines = formats_handler.find_in_text_lines(
            search_word, found_lines, case_sensitive,
        )

    return found_lines


def find_in_files(
    search_word: str,
    filenames: Iterable[str],
    case_sensitive: Optional[bool] = True,
) -> Dict[str, List[str]]:
    """
    Find specified word in multiple files.

    Args:
        search_word (str): word to search in files.
        filenames (Iterable[str]): list with names of files to search in.
        case_sensitive (Optional[bool]): case sensitive search.

    Returns:
        dict[str, List[str]: filename -> list with lines.

    """
    search_word = str(search_word)
    filenames = list(map(str, filenames))
    search_result: Dict[str, List[str]] = {}
    for filename in filenames:
        search_result[filename] = find_in_single_file(
            search_word, filename, case_sensitive,
        )
    return search_result
