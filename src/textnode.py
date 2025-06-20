import re
from htmlnode import LeafNode
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self,text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        if(self.text == node.text and self.text_type == node.text_type and self.url == node.url):
            return True
        else:
            return False
        
    def __repr__(self):
        string = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return string

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text,{"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "",{"src": text_node.url,"alt": text_node.text})
        case _:
            raise Exception("Node does not have a Valid Text Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid Markdown Syntax")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    alt_text = re.findall(r"\!\[(.*?)\]",text)
    url = re.findall(r"\((.*?)\)",text)
    pairs = []
    for i in range(len(alt_text)):
        pair = (alt_text[i], url[i])
        pairs.append(pair)
    return pairs

def extract_markdown_links(text):
    anchor_text = re.findall(r"\[(.*?)\]",text)
    url = re.findall(r"\((.*?)\)",text)
    pairs = []
    for i in range(len(anchor_text)):
        pair = (anchor_text[i], url[i])
        pairs.append(pair)
    return pairs

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        image_pairs = extract_markdown_images(old_node.text)
        if(image_pairs == []):
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for pair in image_pairs:
            image_alt = pair[0]
            image_link = pair[1]
            split = text.split(f"![{image_alt}]({image_link})", 1)
            if(split[0] != ""):
                new_text_node = TextNode(split[0],TextType.TEXT)
                new_nodes.append(new_text_node)
            new_image_node = TextNode(image_alt, TextType.IMAGE, image_link)
            new_nodes.append(new_image_node)
            text = split[1]
        if(text != ""):
            new_text_node = TextNode(text,TextType.TEXT)
            new_nodes.append(new_text_node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        link_pairs = extract_markdown_links(old_node.text)
        if(link_pairs == []):
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for pair in link_pairs:
            anchor_text = pair[0]
            link_url = pair[1]
            split = text.split(f"[{anchor_text}]({link_url})", 1)
            if(split[0] != ""):
                new_text_node = TextNode(split[0],TextType.TEXT)
                new_nodes.append(new_text_node)
            new_link_node = TextNode(anchor_text, TextType.LINK, link_url)
            new_nodes.append(new_link_node)
            text = split[1]
        if(text != ""):
            new_text_node = TextNode(text,TextType.TEXT)
            new_nodes.append(new_text_node)
    return new_nodes

def text_to_textnodes(text):
    root_node = TextNode(text,TextType.TEXT)
    node_list = [root_node]
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list,"`", TextType.CODE)
    return node_list