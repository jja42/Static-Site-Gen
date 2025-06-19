import textnode
import htmlnode
from enum import Enum

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