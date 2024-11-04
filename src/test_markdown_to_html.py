import unittest
from markdown_to_html import *

class Test_Markdown_to_HTML(unittest.TestCase):
    def test_one_basic_node(self):
        text = "# Heading"
        node = markdown_to_html(text)
        self.assertEqual(str(node), "HTMLNode(div, None, [HTMLNode(h1, None, [HTMLNode(None, Heading, None, )], )], )")

    def test_complex_multiple_nodes(self):
        text = "###### Heading number 1 **HISTORY REPEATS YET AGAIN**\n\n>I've never seen such a sorry sight\n>My kid fell for that trap\n>I need help from the government!\n\n### How to save the world\n\n* Accept everyone for who they are\n* Provide cheaper alternatives to the current system.\n* Give everyone the same opportunities"
        node = markdown_to_html(text)
        self.assertEqual(str(node), "HTMLNode(div, None, [HTMLNode(h6, None, [HTMLNode(None, Heading number 1 , None, ), HTMLNode(b, HISTORY REPEATS YET AGAIN, None, )], ), HTMLNode(blockquote, None, [HTMLNode(None, I've never seen such a sorry sight\nMy kid fell for that trap\nI need help from the government!, None, )], ), HTMLNode(h3, None, [HTMLNode(None, How to save the world, None, )], ), HTMLNode(ul, None, [HTMLNode(li, None, [HTMLNode(None, Accept everyone for who they are, None, )], ), HTMLNode(li, None, [HTMLNode(None, Provide cheaper alternatives to the current system., None, )], ), HTMLNode(li, None, [HTMLNode(None, Give everyone the same opportunities, None, )], )], )], )")

    def test_blocks_with_multiple_text_nodes(self):
        text = "## How to use the `type()` function\n\n1. Insert whatever variable whose *type* you want to **check**.\n2. Print the **result** to the *console* using the `print()` function\n\nIf you're not sure, go [to boot dev](https://www.boot.dev)"
        node = markdown_to_html(text)
        self.assertEqual(str(node), "HTMLNode(div, None, [HTMLNode(h2, None, [HTMLNode(None, How to use the , None, ), HTMLNode(code, type(), None, ), HTMLNode(None,  function, None, )], ), HTMLNode(ol, None, [HTMLNode(li, None, [HTMLNode(None, Insert whatever variable whose , None, ), HTMLNode(i, type, None, ), HTMLNode(None,  you want to , None, ), HTMLNode(b, check, None, ), HTMLNode(None, ., None, )], ), HTMLNode(li, None, [HTMLNode(None, Print the , None, ), HTMLNode(b, result, None, ), HTMLNode(None,  to the , None, ), HTMLNode(i, console, None, ), HTMLNode(None,  using the , None, ), HTMLNode(code, print(), None, ), HTMLNode(None,  function, None, )], )], ), HTMLNode(p, None, [HTMLNode(None, If you're not sure, go , None, ), HTMLNode(a, to boot dev, None,  href=\"https://www.boot.dev\")], )], )")