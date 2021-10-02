"""Module for scanning files and searching specified words in them."""

import os
from typing import Callable, Dict, Iterable, List, Optional

import docx2txt

import helpers


def find_in_text_lines(search_word: str, text_lines: List[str]) -> List[str]:
    """
    Get all lines where given word is found.

    Args:
        search_word (str): word to search in lines.
        text_lines (List[str]): list with text lines.

    Returns:
        List[str]: list with lines where word is found.

    """
    line_bound: int = 24
    found_lines: List[str] = []

    for line in text_lines:
        if search_word in line:
            line = helpers.trim_string(
                line,
                line.index(search_word),
                line_bound,
                line_bound + len(search_word),
            )
            found_lines.append(line)
    return found_lines


def find_in_doc_file(search_word: str, filename: str) -> List[str]:
    """
    Find specified word in doc (Word 2003 and older) file.

    Security warning: it may be unsafe to feed user input into shell.
    Check the `filename` before calling the function (ex. os.path.exists)

    Args:
        search_word (str): word to search in file.
        filename (str): name of file to search in.

    Returns:
        List[str]: list with lines where the word is found.

    Raises:
        ValueError: file has extension other than doc.

    """
    if not filename.endswith('.doc'):
        raise ValueError('File extension must be .doc')
    if not os.path.exists('.antiword'):
        return ['Не найден модуль для обработки .doc файлов']

    os.environ['HOME'] = '.'
    # `filename` string is checked for validity in `find_in_single_file` func
    stream = os.popen('{0} -m {1} {2}'.format(
        r'.antiword\antiword.exe', 'cp1251', filename,
        ),
    )
    text_lines = stream.read().replace('[pic]', '').split('\n')

    return find_in_text_lines(search_word, text_lines)


def find_in_docx_file(search_word: str, filename: str) -> List[str]:
    """
    Find specified word in docx (Word 2007 and newer) file.

    Args:
        search_word (str): word to search in file.
        filename (str): name of file to search in.

    Returns:
        List[str]: list with lines where the word is found.

    Raises:
        ValueError: file has extension other than docx.

    """
    if not filename.endswith('.docx'):
        raise ValueError('File extension must be .docx')

    file_text: str = docx2txt.process(filename).replace('\xa0', '')
    text_lines: List[str] = file_text.split('\n')
    return find_in_text_lines(search_word, text_lines)


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
    file_handler: Optional[Callable] = globals().get(
        'find_in_{0}_file'.format(file_extension),
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
