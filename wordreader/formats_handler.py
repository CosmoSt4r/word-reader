"""
Module for processing files of specified formats.

Supported formats:
    - doc
    - docx

"""

import os
from typing import List, Optional

import docx2txt


def find_in_text_lines(
    search_word: str,
    text_lines: List[str],
    case_sensitive: Optional[bool] = True,
) -> List[str]:
    """
    Get all lines where given word is found.

    Args:
        search_word (str): word to search in lines.
        text_lines (List[str]): list with text lines.
        case_sensitive (Optional[bool]): case sensitive search.

    Returns:
        List[str]: list with lines where word is found.

    """
    found_lines: List[str] = []
    word_is_found: bool = False

    for line in text_lines:
        if case_sensitive:
            word_is_found = search_word in line
        else:
            word_is_found = search_word.lower() in line.lower()

        if word_is_found:
            found_lines.append(line)
    return found_lines


def split_doc_file(search_word: str, filename: str) -> List[str]:
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
    text_lines: List[str] = stream.read().replace('[pic]', '').split('\n')

    return text_lines


def split_docx_file(search_word: str, filename: str) -> List[str]:
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

    return text_lines
