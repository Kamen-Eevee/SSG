from text_to_textNodes import *
import unittest

class TestTextToNodes(unittest.TestCase):
    def test_basic_node(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
                                    TextNode("This is ", text_type_text),
                                    TextNode("text", text_type_bold),
                                    TextNode(" with an ", text_type_text),
                                    TextNode("italic", text_type_italic),
                                    TextNode(" word and a ", text_type_text),
                                    TextNode("code block", text_type_code),
                                    TextNode(" and an ", text_type_text),
                                    TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                    TextNode(" and a ", text_type_text),
                                    TextNode("link", text_type_link, "https://boot.dev"),
                                ])
        
    def test_swapped_node(self):
        text = "This is *text* with a **bold** word and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and a `code block`"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
                                    TextNode("This is ", text_type_text),
                                    TextNode("text", text_type_italic),
                                    TextNode(" with a ", text_type_text),
                                    TextNode("bold", text_type_bold),
                                    TextNode(" word and an ", text_type_text),
                                    TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                    TextNode(" and a ", text_type_text),
                                    TextNode("link", text_type_link, "https://boot.dev"),
                                    TextNode(" and a ", text_type_text),
                                    TextNode("code block", text_type_code)
                                ])
        
    def test_start_with_nontext(self):
        text = "**I LOVE ** a good *story.* They always give me **joy.** This `block of code` will let you see an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) while also sending you to [a great site](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
                                    TextNode("I LOVE ", text_type_bold),
                                    TextNode(" a good ", text_type_text),
                                    TextNode("story.", text_type_italic),
                                    TextNode(" They always give me ", text_type_text),
                                    TextNode("joy.", text_type_bold),
                                    TextNode(" This ", text_type_text),
                                    TextNode("block of code", text_type_code),
                                    TextNode(" will let you see an ", text_type_text),
                                    TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                    TextNode(" while also sending you to ", text_type_text),
                                    TextNode("a great site", text_type_link, "https://boot.dev")
        ])