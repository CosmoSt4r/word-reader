"""Module for helper functions."""

from typing import List, Optional


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


def drop_empty_lines(text_lines: List[str]) -> List[str]:
    """
    Drop empty lines and spaces around the line.

    Args:
        text_lines (List[str]): list with text lines.

    Returns:
        List[str]: given list without empty lines and spaces around them.

    """
    text_lines_without_spaces: List[str] = []
    for line in text_lines:
        line = line.strip()
        if line:
            text_lines_without_spaces.append(line)
    return text_lines_without_spaces


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
        line = line.strip()
        if case_sensitive:
            word_is_found = search_word in line
        else:
            word_is_found = search_word.lower() in line.lower()

        if word_is_found:
            found_lines.append(line)
    return found_lines
