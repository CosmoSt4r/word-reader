"""
Module for processing files of specified formats.

Supported formats:
    - doc
    - docx
    - txt

"""

import os
from typing import List

import docx2txt


def split_doc_file(filename: str) -> List[str]:
    """
    Split text into lines in doc (Word 2003 and older) file.

    Security warning: it may be unsafe to feed user input into shell.
    Check the `filename` before calling the function (ex. os.path.exists)

    Args:
        filename (str): name of file to process.

    Returns:
        List[str]: list with lines of text.

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
    return stream.read().replace('[pic]', '').split('\n')


def split_docx_file(filename: str) -> List[str]:
    """
    Split text into lines in docx (Word 2007 and newer) file.

    Args:
        filename (str): name of file to process.

    Returns:
        List[str]: list with lines of text.

    Raises:
        ValueError: file has extension other than docx.

    """
    if not filename.endswith('.docx'):
        raise ValueError('File extension must be .docx')

    file_text: str = docx2txt.process(filename).replace('\xa0', '')
    return file_text.split('\n')


def split_txt_file(filename: str) -> List[str]:
    """
    Split text into lines in txt (Notepad) file.

    Args:
        filename (str): name of file to process.

    Returns:
        List[str]: list with lines of text.

    Raises:
        ValueError: file has extension other than txt.

    """
    if not filename.endswith('.txt'):
        raise ValueError('File extension must be txt')

    with open(filename, encoding='utf-8') as txt_file:
        # `read.split` is not the same as `readlines`
        # this is intentional
        return txt_file.read().split('\n')
