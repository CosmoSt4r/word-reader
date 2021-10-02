import pytest

from wordreader.scanner import find_in_files

docx = 'tests/docx_test.docx'
doc = 'tests/doc_test.doc'

def test_basic_cases():
    assert find_in_files('', []) == {}
    assert find_in_files('', [1, 2, 3]) == {'1': [], '2': [], '3': []}
    assert find_in_files('1', [doc]) == find_in_files(1, [doc])


def test_different_formats():

    target = {
        doc: ['Какой-то текст', 'Еще немного текста'],
        docx: ['Какой-то текст', 'Еще немного текста'],
    }
    assert find_in_files('текст', [doc, docx]) == target


def test_case_sensitive_search():
    target = {
        doc: ['Еще немного текста'],
        docx: ['Еще немного текста'],
    }
    assert find_in_files('еще', [doc, docx]) == {doc: [], docx: []}
    assert find_in_files('еще', [doc, docx], case_sensitive=False) == target
