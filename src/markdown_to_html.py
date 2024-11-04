from markdown_to_blocks import *
from htmlnode import *
from textnode import *
from text_to_textNodes import *

code_tag = "pre"
quote_tag = "blockquote"
unordered_tag = "ul"
list_item_tag = "li"
ordered_tag = "ol"
paragraph_tag = "p"

def hashtag_counter(string):
    num = 0
    for i in range(0, 6):
        if string[i] == "#":
            num += 1
    return num

def text_to_html(node_list):
    new_node_list = []
    for i in range(0, len(node_list)):
        new_node = text_node_to_html_node(node_list[i])
        new_node_list.append(new_node)
    return new_node_list

def remove_markdown(text, type):
    match type:
        case "code":
            return text[3:-3].strip()
        case "quote":
            lines = text.split("\n")
            new_text = ""
            for line in range(0, len(lines)):
                new_line = lines[line][1:].strip()
                new_text += new_line
                if line != len(lines)-1:
                    new_text += "\n"
            return new_text
        
        case "unordered list":
            lines = text.split("\n")
            new_text = ""
            for line in range(0, len(lines)):
                new_text += lines[line][2:]
                if line != len(lines)-1:
                    new_text += "\n"
            return new_text
        case "ordered list":
            lines = text.split("\n")
            new_text = ""
            for line in range(0, len(lines)):
                new_text += lines[line][3:]
                if line != len(lines)-1:
                    new_text += "\n"
            return new_text
        case "heading":
            num = hashtag_counter(text)
            return text[num+1:]
        case ___:
            return text

def list_to_nodes(block):
    item_list = block.split("\n")
    node_list = []
    for item in range(0, len(item_list)):
        node = HTMLNode(list_item_tag, item_list[item], None, None)
        node_list.append(node)
    return node_list

###Determine how multiple children nodes would react
def text_to_children(node):
    leaf_node_list = []
    all_nodes = []
    if node.value == None:
        for i in range(0, len(node.children)):
            #Send child recursively until you have no children (aka a value)
            text_node = text_to_children(node.children[i])
            all_nodes.append(text_node)
        return ParentNode(node.tag, all_nodes, None)
    else:
        text_node = text_to_textnodes(node.value) #list of text nodes
        for i in range(0, len(text_node)):
            #returns a leaf node for each resulting text node
            leaf_node_list.append(text_node_to_html_node(text_node[i]))
        return ParentNode(node.tag, leaf_node_list, None)
    

def markdown_to_html(markdown):
    new_node_list = []
    blocks = markdown_to_blocks(markdown)
    for block in range(0, len(blocks)):
        block_type = block_to_block_type(blocks[block])
        match block_type:
            case "code":
                text = remove_markdown(blocks[block], block_type)
                code_node = HTMLNode("code", text, None, None)
                node = HTMLNode(code_tag, None, [code_node], None)
            case "quote":
                text = remove_markdown(blocks[block], block_type)
                node = HTMLNode(quote_tag, text, None, None)
            case "unordered list":
                text = remove_markdown(blocks[block], block_type)
                node_list = list_to_nodes(text)
                node = HTMLNode(unordered_tag, None, node_list, None)
            case "ordered list":
                text = remove_markdown(blocks[block], block_type)
                node_list = list_to_nodes(text)
                node = HTMLNode(ordered_tag, None, node_list, None)
            case "heading":
                text = remove_markdown(blocks[block], block_type)
                num_hashtags = hashtag_counter(blocks[block])
                heading_tag = "h" + str(num_hashtags)
                node = HTMLNode(heading_tag, text, None, None)
            case __:
                node = HTMLNode(paragraph_tag, blocks[block], None, None)
        child_node_list = text_to_children(node)
        new_node_list.append(child_node_list)
    final_node = ParentNode("div", new_node_list, None)
    return final_node
        
        
        