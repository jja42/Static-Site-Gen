import textnode
import htmlnode
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
        if(paragraph.strip("\n") == ""):
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