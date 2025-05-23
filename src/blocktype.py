from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def is_ordered_list(text: str) -> bool:
    lines = text.splitlines()
    
    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}. "):
            return False

    return True


def block_to_blocktype(block: str) -> BlockType:
    if bool(re.match(r"^#{1,6} (?!#).*", block)):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    elif all(line.startswith("> ") for line in block.splitlines()):
        return BlockType.QUOTE
    else:
        return BlockType.PARAGRAPH
