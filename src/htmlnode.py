class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag 
        #A string representing the HTML tag name
        self.value = value 
        #A string representing the value of the HTML tag. An HTMLNode without a value will be assumed to have children
        self.children = children 
        #A list of HTMLNode objects representing the children of this node. An HTMLNode without children will be assumed to have a value
        self.props = props 
        #A dictionary of key-value pairs representing the attributes of the HTML tag
    
    def to_html(self):
        raise NotImplementedError
        #To Be Implemented by Child Classes
    
    def props_to_html(self):
        string = ""
        if(not self.props):
            return string
        for prop in self.props:
            string += f" {prop}=\"{self.props[prop]}\""
        return string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if(not self.tag):
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if(not self.tag):
            raise ValueError("ParentNode must have a tag")
        if(not self.children):
            raise ValueError("ParentNode must have children")
        string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            string += child.to_html()
        string += f"</{self.tag}>"
        return string
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"