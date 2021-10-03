import unittest

from wordreader.scanner import find_in_files

def get_name(extension: str):
    return 'tests/documents/{0}_test.{0}'.format(extension)

class ScannerTest(unittest.TestCase):
    def test_basic_cases(self):
        self.assertEqual(find_in_files('', []), {})
        self.assertEqual(
                find_in_files('', [1, 2, 3]), 
                {'1': [], '2': [], '3': []},
            )
        self.assertEqual(
                find_in_files('1', [get_name('doc')]), 
                find_in_files(1, [get_name('doc')]),
            )

    def test_different_formats(self):
        search_result = ['Какой-то текст', 'Еще немного текста']
        target = {
            get_name('doc'): search_result,
            get_name('docx'): search_result,
            get_name('txt'): search_result,
        }
        self.assertEqual(
                find_in_files('текст', target.keys()), 
                target,
            )

    def test_case_sensitive_search(self):
        target = {
            get_name('doc'): ['Еще немного текста'],
            get_name('docx'): ['Еще немного текста'],
        }
        self.assertEqual(
                find_in_files('еще', target.keys()), 
                { get_name('doc'): [], get_name('docx'): [] },
            )
        self.assertEqual(
                find_in_files('еще', target.keys(), case_sensitive=False), 
                target,
            )

if __name__ == '__main__':
    unittest.main()
