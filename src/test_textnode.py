import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_noneq(self):
        node = TextNode("Test Node 1", "bold")
        node2 = TextNode("Test Node 2", "bold")
        self.assertNotEqual(node, node2)

    def test__no_url(self):
        node = TextNode("Test Node", "bold", None)
        node2 = TextNode("Test Node", "bold")
        self.assertEqual(node, node2)
    
    def test_with_url(self):
        node = TextNode("Test Node", "bold", None)
        node2 = TextNode("Test Node", "bold", "http://boot.dev")
        self.assertNotEqual(node, node2)

    def test_with_types(self):
        node = TextNode("Test Node", "bold")
        node2 = TextNode("Test Node", "italic")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()