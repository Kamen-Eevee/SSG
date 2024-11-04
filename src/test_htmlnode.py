import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def testNode(self):
        node = HTMLNode("a", "Link", [], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), 
                         ' href="https://www.google.com" target="_blank"')

    
    def testNoProps(self):
        node = HTMLNode("a", "Link", [], None)
        self.assertEqual(node.props_to_html(), "")
        
    def testException(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def testNode(self):
        node = LeafNode("p", "This is a sentence of text", None)
        self.assertEqual(node.to_html(), "<p>This is a sentence of text</p>")

    def testProps(self):
        node = LeafNode("a", "Here is a fun link", {
            "href": "www.ILiveHere.org",
            "target": "_blank"
        })        
        self.assertEqual(node.to_html(), '<a href="www.ILiveHere.org" target="_blank">Here is a fun link</a>')

    def testException(self):
        node = LeafNode("p", None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def testRawText(self):
        node = LeafNode(None, "Raw Text", None)
        self.assertEqual(node.to_html(), "Raw Text")

class TestParentNodes(unittest.TestCase):
    def testBasicNode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def testErrorNoTag(self):
        node = ParentNode(None, [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],{
            "href": "https://www.google.com",
            "target": "_blank",
        })
        with self.assertRaises(ValueError):
            node.to_html()

    def testErrorNoChildren(self):
        node = ParentNode("p", None ,{
            "href": "https://www.google.com",
            "target": "_blank",
        })
        with self.assertRaises(ValueError):
            node.to_html()
        
    def testNestedParents(self):
        node = ParentNode(
            "p",
            [
                ParentNode("a", [
                    LeafNode("b", "Bold text"),
                    LeafNode("i", "Italic text")
                ]),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), 
                         "<p><a><b>Bold text</b><i>Italic text</i></a>Normal text<i>italic text</i>Normal text</p>")
    
    def testMultipleNests(self):
        node = ParentNode(
            "p",
            [
                ParentNode("a", [
                    LeafNode("b", "Bold text"),
                    LeafNode("i", "Italic text")
                ]),
                ParentNode("c", [
                    ParentNode("d",[
                        LeafNode("b", "Bold Text"),
                        LeafNode(None, "Regular Text")
                    ]),
                    LeafNode("b", "Bolded Text")
                ]),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), 
                         "<p><a><b>Bold text</b><i>Italic text</i></a><c><d><b>Bold Text</b>"+
                         "Regular Text</d><b>Bolded Text</b></c>Normal text<i>italic text</i>Normal text</p>")
        
