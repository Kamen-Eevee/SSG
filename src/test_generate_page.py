import unittest
from generate_page import *

class TestExtractTitle(unittest.TestCase):
    def test_basic_extract(self):
        markdown = "# Top Story of the Day!"
        title = extract_title(markdown)
        self.assertEqual(title, "Top Story of the Day!")

    def test_whitespace(self):
        markdown = "#    Best Heading Ever      "
        title = extract_title(markdown)
        self.assertEqual(title, "Best Heading Ever")

    def test_multiple_blocks(self):
        markdown = "# Heading 1\n\n##Heading 2\n\n```code 1 ```"
        title = extract_title(markdown)
        self.assertEqual(title, "Heading 1")

    def test_mixed_in_why_I_dont_know(self):
        markdown = "## Heading 2\n\n*List 1\n*List 2\n\n# Heading 1\n\n```Code 1```"
        title = extract_title(markdown)
        self.assertEqual(title, "Heading 1")

    def test_exceptions(self):
        markdown = "## Heading 2\n\n*list 1\n*list 2\n\n#### Heading 4"
        with self.assertRaises(Exception):
            title = extract_title(markdown)