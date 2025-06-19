from textnode import *
from htmlnode import *
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    paragraphs = markdown.split("\n\n")

    for paragraph in paragraphs:
        if(paragraph == ""):
            continue
        paragraph = paragraph.strip()
        blocks.append(paragraph)
    
    return blocks

def block_to_block_type(markdown_block):
    match = re.search(r'^\#{1,6} (.*)', markdown_block)
    if(match):
        return BlockType.HEADING
    
    match = re.search(r'^\`{3}(.*)\`{3}', markdown_block, re.DOTALL)
    if(match):
        return BlockType.CODE
    
    lines = markdown_block.split("\n")
    quote = True
    unordered = True
    ordered = True

    for i in range(len(lines)):
        if(quote):
            match = re.search(r'^\>(.*)', lines[i])
            if(not match):
                quote = False
        if(unordered):
            match = re.search(r'^\-\s(.*)', lines[i])
            if(not match):
                unordered = False
        if(ordered):
            match = re.search(r'^\d+\.\s(.*)', lines[i])
            if(not match):
                ordered = False
            else:
                match = re.search(r'(^\d+)\.\s', lines[i])
                if(int(match.group(1)) != (i+1)):
                    ordered = False

    if(quote):
        return BlockType.QUOTE
    if(unordered):
        return BlockType.UNORDERED_LIST
    if(ordered):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    parent_node = ParentNode("div",children)
    return parent_node

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            block_node = markdown_paragraph_block_to_node(block)
        case BlockType.HEADING:
            block_node = markdown_heading_block_to_node(block)
        case BlockType.CODE:
            block_node = markdown_code_block_to_node(block)
        case BlockType.QUOTE:
            block_node = markdown_quote_block_to_node(block)
        case BlockType.UNORDERED_LIST:
            block_node = markdown_unordered_block_to_node(block)
        case BlockType.ORDERED_LIST:
            block_node = markdown_ordered_block_to_node(block)
    return block_node

def markdown_paragraph_block_to_node(block):
    lines = block.split("\n")
    block = " ".join(lines)
    child_nodes = text_to_children(block)
    block_node = ParentNode("p",child_nodes)
    return block_node

def markdown_heading_block_to_node(block):
    match = re.search(r'^(#+)\s', block)
    if match:
        heading_level = len(match.group(1))
        heading_level = f"h{heading_level}"
    block = block.replace("#","")
    block = block.lstrip()
    child_nodes = text_to_children(block)
    block_node = ParentNode(heading_level,child_nodes)
    return block_node

def markdown_code_block_to_node(block):
    block = block.replace("```","")
    block = block.lstrip("\n")
    node = TextNode(block,TextType.TEXT)
    html_node = text_node_to_html_node(node)
    block_node = ParentNode("code",[html_node])
    wrapper_node = ParentNode("pre",[block_node])
    return wrapper_node

def markdown_quote_block_to_node(block):
    lines = block.split("\n")
    quotes = []
    for line in lines:
        quotes.append(line.lstrip(">").strip())
    block = " ".join(quotes)
    child_nodes = text_to_children(block)
    block_node = ParentNode("blockquote",child_nodes)
    return block_node

def markdown_unordered_block_to_node(block):
    lines = block.split("\n")
    child_nodes = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        child_nodes.append(ParentNode("li", children))
    block_node = ParentNode("ul",child_nodes)
    return block_node

def markdown_ordered_block_to_node(block):
    lines = block.split("\n")
    child_nodes = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        child_nodes.append(ParentNode("li", children))
    block_node = ParentNode("ol",child_nodes)
    return block_node
    

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    htmlnodes = []
    for node in text_nodes:
        new_node = text_node_to_html_node(node)
        htmlnodes.append(new_node)
    return htmlnodes


