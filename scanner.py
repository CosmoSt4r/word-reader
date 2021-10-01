"""Module for scanning files and searching specified words in them."""

from os import path
from typing import Callable, Dict, Iterable, List, Optional

import docx2txt


def trim_string(
    long_string: str,
    center: int,
    left_bound: int,
    right_bound: int,
) -> str:
    """
    Trim long sting.

    Ex.: function with arguments ('I am too long to process', 2, 10, 10)
    returns string 'I am too long'

    Args:
        long_string (str): long string to trim.
        center (int): central character.
        left_bound (int): amount of chars left from central character.
        right_bound (int): amount of chars right from central character.

    Returns:
        str: trimmed string.

    """
    right_bound = center + right_bound + 1
    left_bound = center - left_bound
    left_bound = 0 if left_bound < 0 else left_bound

    return long_string[left_bound:right_bound]


def find_in_docx_file(search_word: str, filename: str) -> List[str]:
    """
    Search specified word in docx (Word) file.

    Args:
        search_word (str): word to search in file.
        filename (str): name of file to search in.

    Returns:
        List[str]: list with lines where word is found.

    Raises:
        ValueError: file has extension other than docx.

    """
    if not filename.endswith('.docx'):
        raise ValueError('File extension must be .docx')

    file_text: str = docx2txt.process(filename).replace('\xa0', '')
    text_lines: List[str] = file_text.split('\n')

    found_lines: List[str] = []
    for line in text_lines:
        if search_word in line:
            line = trim_string(
                line, line.index(search_word), 10, 10 + len(search_word),
            )
            found_lines.append(line)

    return found_lines


def find_in_single_file(search_word: str, filename: str) -> List[str]:
    """
    Find specified word in single file.

    Args:
        search_word (str): word to search in file.
        filename (str): name of file to search in.

    Returns:
        List[str]: list with lines where word is found.
        If word is not found, list is empty.

    """
    file_extension: str = filename.split('.')[-1]
    file_handler: Optional[Callable] = globals().get(
        'find_in_{0}_file'.format(file_extension),
    )
    found_lines: List[str] = []

    if file_handler and path.exists(filename):
        found_lines = file_handler(search_word, filename)

    return found_lines


def find_in_files(
    search_word: str, filenames: Iterable[str],
) -> Dict[str, List[str]]:
    """
    Find specified word in multiple files.

    Args:
        search_word (str): word to search in files.
        filenames (List[str]): list with names of files to search in.

    Returns:
        dict[str, List[str]: filename -> list with lines.

    """
    search_result: Dict[str, List[str]] = {}
    for filename in filenames:
        search_result[filename] = find_in_single_file(search_word, filename)
    return search_result
