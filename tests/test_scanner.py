import pytest

from wordreader.scanner import *

def test_find_in_files():
    assert find_in_files('', []) == {}
    assert find_in_files('', [1, 2, 3]) == {'1': [], '2': [], '3': []}
    assert find_in_files(
            '1', ['tests/doc_test.doc'],
            ) == find_in_files(1, ['tests/doc_test.doc'])
   
    target = {
    'tests/doc_test.doc': ['Какой-то текст', 'Еще немного текста'],
    'tests/docx_test.docx': ['Какой-то текст', 'Еще немного текста'],
    }
    assert find_in_files(
            'текст', ['tests/doc_test.doc', 'tests/docx_test.docx']
            ) == target
