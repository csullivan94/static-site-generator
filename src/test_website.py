import unittest
from logging import exception

from website import *

class TestWebsite(unittest.TestCase):

    def test_extract_title(self):
        markdown = '# This is the heading'
        extracted_title = 'This is the heading'
        self.assertEqual(extract_title(markdown), extracted_title)

    def test_extract_title_exception(self):
        with self.assertRaises(Exception):
            markdown = 'This is not a heading'
            extract_title(markdown)

    def test_extract_title_blocks(self):
        markdown = '''# this is the heading

This is a paragraph

```This is some code```'''
        extracted_title = 'this is the heading'
        self.assertEqual(extract_title(markdown), extracted_title)

    def test_extract_title_blocks_not_first(self):
        markdown = '''this is not the heading

# this is a paragraph

```This is some code```'''
        extracted_title = 'this is a paragraph'
        self.assertEqual(extract_title(markdown), extracted_title)