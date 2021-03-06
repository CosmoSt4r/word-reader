"""
Module for processing files of specified formats.

Supported formats:
    - doc
    - docx
    - txt

"""

import os
from subprocess import PIPE, Popen
from typing import List

import docx2txt
import pdfplumber

from wordreader.strings_handler import drop_empty_lines


def split_doc_file(filename: str) -> List[str]:
    """
    Split text into lines in doc (Word 2003 and older) file.

    Security warning: it may be unsafe to feed user input into shell.

    Args:
        filename (str): name of file to process.

    Returns:
        List[str]: list with lines of text.

    Raises:
        ValueError: file has extension other than doc.
        FileNotFoundError: if file or antiword not found.

    """
    if not filename.endswith('.doc'):
        raise ValueError('File extension must be .doc')
    if not (os.path.exists('.antiword') and os.path.exists(filename)):
        raise FileNotFoundError('Unable to process .doc file')

    os.environ['HOME'] = '.'
    stream = Popen(
        [r'.antiword\antiword.exe', '-m', 'UTF-8', filename],
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        stdin=PIPE,
    ).communicate()[0]

    text = stream.decode('utf-8').replace('[pic]', '')
    return drop_empty_lines(text.split('\n'))


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
    return drop_empty_lines(file_text.split('\n'))


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

    with open(filename, encoding='cp1251') as txt_file:
        return drop_empty_lines(txt_file.readlines())


def split_pdf_file(filename: str) -> List[str]:
    """
    Split text into lines in PDF (Adobe) file.

    Args:
        filename (str): name of file to process.

    Returns:
        List[str]: list with lines of text.

    Raises:
        ValueError: file has extension other than pdf.

    """
    if not filename.endswith('.pdf'):
        raise ValueError('File extension must be pdf')

    text_lines: List[str] = []
    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            page = page.extract_text()
            if page:
                text_lines.extend(page.split('\n'))
    return drop_empty_lines(text_lines)
