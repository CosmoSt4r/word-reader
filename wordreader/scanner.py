"""Module for scanning files and searching specified words in them."""

import os
from typing import Callable, Dict, Iterable, List, Optional

from wordreader import formats_handler, strings_handler


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
    file_splitter: Optional[Callable] = getattr(
        formats_handler,
        'split_{0}_file'.format(file_extension),
        None,
    )
    found_lines: List[str] = []

    if file_splitter and os.path.exists(filename):
        found_lines = strings_handler.find_in_text_lines(
            search_word, file_splitter(filename), case_sensitive,
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
        try:
            search_result[filename] = find_in_single_file(
                search_word, filename, case_sensitive,
            )
        except Exception:
            search_result[filename] = []
    return search_result
