from textnode import *
from htmlnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    other_valid_text_types = [text_type_bold, text_type_code, text_type_italic]
    #old nodes is a list of nodes to split. Do text nodes only
    for i in range(0, len(old_nodes)):
        node = old_nodes[i]
        node_list = []
        if node.text_type == text_type_text:
            split_node = node.text.split(delimiter)
            if len(split_node)%2 == 0:
                raise Exception("One of your delimiters is missing")
            else:
                for i in range(0, len(split_node)):
                    if i % 2 == 0:
                        if split_node[i] != "":
                            node_list.append(TextNode(split_node[i], text_type_text))
                    else:
                        if split_node[i] != "":
                            node_list.append(TextNode(split_node[i], text_type))
                new_nodes.extend(node_list)
        elif node.text_type in other_valid_text_types:
            new_nodes.append(node)
        else:
            raise Exception("Not a valid text type")
    return new_nodes



def extract_markdown_images(text):
    return(re.findall(r"!\[(.*?)\]\((.*?)\)", text))

def extract_markdown_links(text):
    return(re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text))

def split_nodes_image(old_nodes):
    new_nodes = []
    for i in range(0, len(old_nodes)):
        node = old_nodes[i]
        node_list = []
        #If the node is already an image, just readd the node right to the final list.
        if node.text_type == text_type_image:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            #If there are any images in the node, split the text node, else add it to the list
            if images != []:
                image_alt = images[0][0]
                image_link = images[0][1]
                split_node = node.text.split(f"![{image_alt}]({image_link})", 1)
                #IF the text is not a blank string add it to the list. Image will be added regardless
                if split_node[0] != "":
                    first_node = TextNode(split_node[0], node.text_type)
                    node_list.append(first_node)
                image_node = TextNode(images[0][0], text_type_image, images[0][1])
                node_list.append(image_node)
                if split_node[1] != "":
                    second_node = TextNode(split_node[1], node.text_type)
                    #If there is another image in the node, recursive call the second half of the text, if not add to the list
                    if len(images) > 1:
                        next_nodes = split_nodes_image([second_node])
                        node_list.extend(next_nodes)
                    #If no other images exist in the list, immediately add the second half of the split node to the list
                    else:                       
                        node_list.append(second_node)
                new_nodes.extend(node_list)
            else:
                new_nodes.append(node)
    #Once all the nodes from the input are gone through, return the list
    return new_nodes        

def split_nodes_link(old_nodes):
    new_nodes = []
    for i in range(0, len(old_nodes)):
        node = old_nodes[i]
        node_list = []
        #If the node is already a link, just readd the node right to the final list.
        if node.text_type == text_type_link:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            #If there are any links in the node, split the text node, else add it to the list
            if links != []:
                link_alt = links[0][0]
                link_link = links[0][1]
                split_node = node.text.split(f"[{link_alt}]({link_link})", 1)
                #IF the text is not a blank string add it to the list. Link will be added regardless
                if split_node[0] != "":
                    first_node = TextNode(split_node[0], node.text_type)
                    node_list.append(first_node)
                image_node = TextNode(links[0][0], text_type_link, links[0][1])
                node_list.append(image_node)
                if split_node[1] != "":
                    second_node = TextNode(split_node[1], node.text_type)
                    #If there is another link in the node, recursive call the second half of the text, if not add to the list
                    if len(links) > 1:
                        next_nodes = split_nodes_link([second_node])
                        node_list.extend(next_nodes)
                    #If no other links exist in the list, immediately add the second half of the split node to the list
                    else:                       
                        node_list.append(second_node)
                new_nodes.extend(node_list)
            else:
                new_nodes.append(node)
    #Once all the nodes from the input are gone through, return the list
    return new_nodes