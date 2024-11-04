class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        text = ""
        for item in self.props:
            text += " " + item + "=" + '"' + self.props[item] + '"'
        return text
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All Leaf nodes must have a value")
        elif self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNodes must have a tag")
        elif self.children == None:
            raise ValueError("Who has my kids?")
        else:
            end_string = ""
            for child in self.children:
                end_string += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{end_string}</{self.tag}>"
        

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text, None)
        case "bold":
            return LeafNode("b", text_node.text, None)
        case "italic":
            return LeafNode("i", text_node.text, None)
        case "code":
            return LeafNode("code", text_node.text, None)
        case "link":
            return LeafNode("a", text_node.text, {"href" : text_node.url})
        case "image":
            return LeafNode("img", "", {"src" : text_node.url,
                                          "alt" : text_node.text})
        case _:
            raise Exception("Not a valid Node Type")