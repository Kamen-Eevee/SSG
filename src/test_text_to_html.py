import unittest

from htmlnode import *
from textnode import *

class TestTextToHTML(unittest.TestCase):
    def testBasicNode(self):
        node = TextNode("This is practice text", "text")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "This is practice text")

    def testBoldNode(self):
        node = TextNode("This is practice text", "bold")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<b>This is practice text</b>")

    def testItalicNode(self):
        node = TextNode("This is practice text", "italic")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<i>This is practice text</i>")

    def testCodeNode(self):
        node = TextNode("This is practice text", "code")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<code>This is practice text</code>")

    def testLinkNode(self):
        node = TextNode("This is practice text", "link", "www.google.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), '<a href="www.google.com">This is practice text</a>')
    
    def testImageNode(self):
        node = TextNode("This is practice text", "image", "www.google.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), '<img src="www.google.com" alt="This is practice text"></img>')
    
    def testBadType(self):
        node = TextNode("This is practice text", "lol", "www.google.com")
        with self.assertRaises(Exception):
            html = text_node_to_html_node(node)