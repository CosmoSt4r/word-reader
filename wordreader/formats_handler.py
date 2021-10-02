"""
Module for processing files of specified formats.

Supported formats:
    - doc
    - docx
    TODO:
    + pdf
    + txt

"""

import os
from typing import List

import docx2txt

from wordreader import helpers


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
    # `filename` string is validated in `find_in_single_file` function
    stream = os.popen('{0} -m {1} "{2}"'.format(
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
