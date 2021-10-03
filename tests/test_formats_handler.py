import unittest

import wordreader.formats_handler as fh

def get_name(extension: str):
    return 'tests/{0}_test.{0}'.format(extension)

class FormatsHandlerTest(unittest.TestCase):
    """ doc """
    def test_doc_splitter(self):
        splitted_text = fh.split_doc_file(get_name('doc'))

        self.assertEqual(splitted_text[0].strip(), 'Какой-то текст')
        self.assertEqual(splitted_text[-1].strip(), '1234567890')

    def test_doc_raises_value_error(self):
        with self.assertRaises(ValueError):
            fh.split_doc_file('file.exe')

    def test_doc_raises_not_found(self):
        with self.assertRaises(FileNotFoundError):
            fh.split_doc_file('tests/not_found.doc')

    """ docx """
    def test_docx_splitter(self):
        splitted_text = fh.split_docx_file(get_name('docx'))

        self.assertEqual(splitted_text[1], 'Какой-то текст')
        self.assertEqual(splitted_text[-1], '1234567890')

    def test_docx_raises_error(self):
        with self.assertRaises(ValueError):
            fh.split_docx_file('file.exe')

    """ txt """
    def test_txt_splitter(self):
        splitted_text = fh.split_txt_file(get_name('txt'))

        self.assertEqual(splitted_text[0], 'Какой-то текст')
        self.assertEqual(splitted_text[-1], '1234567890')

    def test_txt_raises_error(self):
        with self.assertRaises(ValueError):
            fh.split_txt_file('file.exe')

    """ pdf """
    def test_pdf_splitter(self):
        splitted_text = fh.split_pdf_file(get_name('pdf'))

        self.assertEqual(splitted_text[0], 'Какой-то текст')
        self.assertEqual(splitted_text[-1], '1234567890')

    def test_pdf_raises_error(self):
        with self.assertRaises(ValueError):
            fh.split_pdf_file('file.exe')


if __name__ == '__main__':
    unittest.main()
