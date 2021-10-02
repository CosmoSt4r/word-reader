"""Module for helper functions."""


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


