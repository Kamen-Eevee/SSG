from split_nodes_delimiter import *

def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    node_list = split_nodes_delimiter([node], "**", text_type_bold)
    node_list = split_nodes_delimiter(node_list, "*", text_type_italic)
    node_list = split_nodes_delimiter(node_list, "`", text_type_code)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list