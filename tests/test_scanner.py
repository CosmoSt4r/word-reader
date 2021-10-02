import unittest

from wordreader.scanner import find_in_files

docx = 'tests/docx_test.docx'
doc = 'tests/doc_test.doc'


class ScannerTest(unittest.TestCase):
    def test_basic_cases(self):
        self.assertEqual(find_in_files('', []), {})
        self.assertEqual(
                find_in_files('', [1, 2, 3]), {'1': [], '2': [], '3': []}
            )
        self.assertEqual(find_in_files('1', [doc]), find_in_files(1, [doc]))

    def test_different_formats(self):
        target = {
            doc: ['Какой-то текст', 'Еще немного текста'],
            docx: ['Какой-то текст', 'Еще немного текста'],
        }
        self.assertEqual(find_in_files('текст', [doc, docx]), target)

    def test_case_sensitive_search(self):
        target = {
            doc: ['Еще немного текста'],
            docx: ['Еще немного текста'],
        }
        self.assertEqual(find_in_files('еще', [doc, docx]), {doc: [], docx: []})
        self.assertEqual(
                find_in_files('еще', [doc, docx], case_sensitive=False), target
            )

if __name__ == '__main__':
    unittest.main()
