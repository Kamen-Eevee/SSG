import unittest

from textnode import *
from split_nodes_delimiter import *

class TestDelimiter(unittest.TestCase):
    def test_basic_node(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
            ])
    
    def test_multiple_nodes(self):
        node1 = TextNode("This will have **multiple** nodes to parse through", text_type_text)
        node2 = TextNode("Ideally this *should* parse through each one multiple times", text_type_text)
        node3 = TextNode("And give an accurate result", text_type_text)
        node_list = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(node_list, "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertEqual(new_nodes, [TextNode("This will have ", text_type_text, None), 
                                     TextNode("multiple", text_type_bold, None), 
                                     TextNode(" nodes to parse through", text_type_text, None), 
                                     TextNode("Ideally this ", text_type_text, None), 
                                     TextNode("should", text_type_italic, None), 
                                     TextNode(" parse through each one multiple times", text_type_text, None), 
                                     TextNode("And give an accurate result", text_type_text, None)])
        
    def test_Exception(self):
        node = TextNode("This node is missing an important `delimiter and will fail", text_type_text)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", text_type_code)

    def test_Bold_only(self):
        node = TextNode("This **whole** node is bolded", text_type_bold)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes, [node])

    def test_Bad_type(self):
        node = node = TextNode("I want to use a ^link^ node", "link")
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "^", "link")

class TestImageAndLinkExtraction(unittest.TestCase):
    def test_basic_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text),
                         [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
                        )

    def test_basic_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text),
                         [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_both_image_and_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/akaOqIh.gif) and a link [to boot dev](https://www.boot.dev)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertNotEqual(images, links)

    def test_invalid_link(self):
        text = "I don't know what the syntax is for this [link][www.howyadoing.com]"
        self.assertEqual([], extract_markdown_links(text))

class TestSplitNodesImageAndText(unittest.TestCase):
    def test_basic_image(self):
        node = TextNode("A basic image ![of an apple](https://i.imgur.com/aka0qIh.gif)", text_type_text)
        self.assertEqual(split_nodes_image([node]), [TextNode("A basic image ", "text", None), TextNode("of an apple", "image", "https://i.imgur.com/aka0qIh.gif")])

    def test_basic_link(self):
        node = TextNode("A basic link [to an apple](https://i.imgur.com/aka0qIh.gif)", text_type_text)
        self.assertEqual(split_nodes_link([node]), [TextNode("A basic link ", "text", None), TextNode("to an apple", "link", "https://i.imgur.com/aka0qIh.gif")])

    def test_link_and_image(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
            )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a link ", "text", None), TextNode("to boot dev", "image", "https://www.boot.dev"), TextNode(" and ", "text", None), TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")])

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
            )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("This is text with a link ", "text", None), TextNode("to boot dev", "link", "https://www.boot.dev"), TextNode(" and ", "text", None), TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")])

    def test_back_to_back_images(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)[and to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
            )
        self.assertEqual(split_nodes_link([node]), [TextNode("This is text with a link ", "text", None), TextNode("to boot dev", "link", "https://www.boot.dev"), TextNode("and to youtube", "link", "https://www.youtube.com/@bootdotdev")])
    
    def test_no_images(self):
        node = TextNode("I have no links or images to offer", text_type_text)
        self.assertEqual(split_nodes_image([node]), [TextNode("I have no links or images to offer", "text", None)])

    def test_multi_node(self):
        node1 = TextNode("A basic link ![to an apple](https://i.imgur.com/aka0qIh.gif)", text_type_text)
        node2 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
            )
        node_list = [node1, node2]
        new_nodes = split_nodes_link(node_list)
        new_nodes = split_nodes_image(new_nodes)
        self.assertEqual(new_nodes, [TextNode("A basic link ", "text", None),
                                     TextNode("to an apple", "image", "https://i.imgur.com/aka0qIh.gif"), 
                                     TextNode("This is text with a link ", "text", None), 
                                     TextNode("to boot dev", "link", "https://www.boot.dev"), 
                                     TextNode(" and ", "text", None), 
                                     TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")])

    def test_already_image_node(self):
        node = TextNode("to boot dev", text_type_image, "https://www.boot.dev")
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("to boot dev", text_type_image, "https://www.boot.dev")])

    def test_already_link_node(self):
        node = TextNode("to boot dev", text_type_link, "https://www.boot.dev")
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("to boot dev", text_type_link, "https://www.boot.dev")])

    def test_only_images_no_text(self):
        node = TextNode(
            "![to boot dev](https://www.boot.dev)![and to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
            )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("to boot dev", "image", "https://www.boot.dev"), 
                                     TextNode("and to youtube", "image", "https://www.youtube.com/@bootdotdev")])
    
    def test_only_links_no_text(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)[and to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
            )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("to boot dev", "link", "https://www.boot.dev"), 
                                     TextNode("and to youtube", "link", "https://www.youtube.com/@bootdotdev")])

    def test_alternating_image_and_links(self):
        node = TextNode("[to boot dev](https://www.boot.dev)![and to youtube](https://www.youtube.com/@bootdotdev)[and to google](https://google.com)![Have an apple](imgur.com/haveanapple)",
                        text_type_text,)
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertEqual(new_nodes, [TextNode("to boot dev", "link", "https://www.boot.dev"), 
                                     TextNode("and to youtube", "image", "https://www.youtube.com/@bootdotdev"), 
                                     TextNode("and to google", "link", "https://google.com"), 
                                     TextNode("Have an apple", "image", "imgur.com/haveanapple")])

