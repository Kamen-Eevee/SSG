from text_to_textNodes import *
import unittest
from markdown_to_blocks import *

class TestMarkdown(unittest.TestCase):
    def test_basic_markdown(self):
        text = "This is a heading \n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        block_list = markdown_to_blocks(text)
        self.assertEqual(block_list, ['This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item'])

    def test_extra_newlines(self):
        text = "\n\n\n\n\n\nHeading\n\nMidsection text\n\nList1\nList2\nList3"
        block_list = markdown_to_blocks(text)
        self.assertEqual(block_list, ['Heading', 'Midsection text', 'List1\nList2\nList3'])

    def test_no_blocks(self):
        text = "Heading\nMidsection text\nList1\nList2\nList3"
        block_list = markdown_to_blocks(text)
        self.assertEqual(block_list, ["Heading\nMidsection text\nList1\nList2\nList3"])

class TestBlockType(unittest.TestCase):
    def test_normal_block(self):
        text = "This is a Paragraph"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")
    
    def test_heading_block_1(self):
        text = "# Header with 1 #"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")

    def test_heading_block_2(self):
        text = "## Header with 2 #"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")

    def test_heading_block_3(self):
        text = "### Header with 3 #"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")

    def test_heading_block_4(self):
        text = "#### Header with 4 #"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")

    def test_heading_block_5(self):
        text = "##### Header with 5 #"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")

    def test_heading_block_6(self):
        text = "###### Header with 6 #"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")

    def test_fail_heading_block(self):
        text = "###B### Header with 6 #"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_fail_heading_missing_space(self):
        text = "######Header with 6 #"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_code_block(self):
        text = "```Test code block```"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "code")

    def test_code_block_missing_tick_start(self):
        text = "``Test code block```"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_code_block_missing_tick_end(self):
        text = "```Test code block``"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_quote_block(self):
        text = ">Quote1\n>Quote2\n>Quote3"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "quote")

    def test_quote_block_with_spaces(self):
        text = "> Quote1\n> Quote2\n> Quote3"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "quote")

    def test_quote_block_missing_char(self):
        text = "> Quote1\nQuote2\nQuote3"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_unordered_list_star_only(self):
        text = "* line 1\n* line 2\n* line 3"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "unordered list")

    def test_unordered_list_dash_only(self):
        text = "- line 1\n- line 2\n- line 3"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "unordered list")
    
    def test_mixed_unordered_list(self):
        text = "* line 1\n- line 2\n* line 3\n- line 4"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "unordered list")

    def test_unordered_list_missing_space(self):
        text = "* line 1\n- line 2\n-line 3"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_ordered_list(self):
        text = "1. line 1\n2. line 2\n3. line 3"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "ordered list")
    
    def test_ordered_list_wrong_order(self):
        text = "1. line 1\n3. line 2\n2. line 3"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_ordered_list_no_space(self):
        text = "1. line 1\n2. line 2\n3.line 3"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")