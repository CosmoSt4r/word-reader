"""Module for scanning files and searching specified words in them."""

import os
from typing import Callable, Dict, Iterable, List, Optional

import formats_handler


def find_in_single_file(search_word: str, filename: str) -> List[str]:
    """
    Find specified word in single file.

    Args:
        search_word (str): word to search in file.
        filename (str): name of file to search in.

    Returns:
        List[str]: list with lines where the word is found.
        If word is not found, list is empty.

    """
    file_extension: str = filename.split('.')[-1]
    file_handler: Optional[Callable] = getattr(
        formats_handler, 'find_in_{0}_file'.format(file_extension),
    )
    found_lines: List[str] = []

    if file_handler and os.path.exists(filename):
        found_lines = file_handler(search_word, filename)

    return found_lines


def find_in_files(
    search_word: str, filenames: Iterable[str],
) -> Dict[str, List[str]]:
    """
    Find specified word in multiple files.

    Args:
        search_word (str): word to search in files.
        filenames (Iterable[str]): list with names of files to search in.

    Returns:
        dict[str, List[str]: filename -> list with lines.

    """
    search_result: Dict[str, List[str]] = {}
    for filename in filenames:
        search_result[filename] = find_in_single_file(search_word, filename)
    return search_result
