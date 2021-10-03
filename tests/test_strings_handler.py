import unittest

import wordreader.strings_handler as sh 

class StringsHandlerTest(unittest.TestCase):
    def test_trim_string(self):
        self.assertEqual(sh.trim_string('', 0, 0, 0), '')
        self.assertEqual(sh.trim_string('', -1, -1, -1), '')
        self.assertEqual(
                sh.trim_string('I am too long to process', 2, 10, 10), 
                'I am too long',
            )
        self.assertEqual(
                sh.trim_string('cut_this_0_cut_this', 9, 1, 1),
                '_0_',
            )

    def test_drop_empty_lines(self):
        self.assertEqual(sh.drop_empty_lines(['', '', '']), [])
        self.assertEqual(
                sh.drop_empty_lines(['', '  test  ', '']), 
                ['test'],
            )

    def test_find_in_text_lines(self):
        self.assertEqual(
                sh.find_in_text_lines('test', []),
                [],
            )
        self.assertEqual(
                sh.find_in_text_lines('test', ['test', 'TEST', 'Test']),
                ['test']
            )
        self.assertEqual(
                sh.find_in_text_lines(
                    'test', 
                    ['test', 'TEST', 'Test'], 
                    case_sensitive=False
                ),
                ['test', 'TEST', 'Test'],
            )


if __name__ == '__main__':
    unittest.main()
