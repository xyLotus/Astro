"""
Tests for the astro_file module
"""
import unittest

import astro_file


def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


class AstroFileTests(unittest.TestCase):

    def test_cleanup(self):
        file = astro_file.AstroFile('test_sources/astro_file_comments.asx')
        result = '! function_name(param1                                  ' \
                 '    , param2):\n\n    function_content\n\n\n\n\n\n'
        self.assertEqual(file.content, result)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(AstroFileTests('test_cleanup'))
    return tests


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
