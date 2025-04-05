from enum import Enum

from htmlnode import ParentNode
from inline_md import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    return list(
        map(lambda x: x.strip(), filter(lambda y: y != "", markdown.split("\n\n")))
    )


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        nodes.append(create_html_node_from_block(block, block_type))
    return ParentNode("div", nodes, None)


def create_html_node_from_block(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return create_html_paragraph(block)
        case BlockType.HEADING:
            return create_html_heading(block)
        case BlockType.CODE:
            return create_html_code(block)
        case BlockType.QUOTE:
            return create_html_quote(block)
        case BlockType.UNORDERED_LIST:
            return create_html_ul(block)
        case BlockType.ORDERED_LIST:
            return create_html_ol(block)
        case _:
            raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def create_html_paragraph(block):
    lines = block.split("\n")
    para = " ".join(lines)
    children = text_to_children(para)
    return ParentNode("p", children)


def create_html_heading(block):
    lv = 0
    for c in block:
        if c == "#":
            lv += 1
        else:
            break
    if lv + 1 >= len(block):
        raise ValueError(f"invalid heading level: {lv}")

    children = text_to_children(block[lv + 1 :])
    return ParentNode(f"h{lv}", children)


def create_html_code(block):
    text_node = TextNode(block[4:-3], TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def create_html_ol(block):
    items = block.split("\n")
    li = []
    for item in items:
        children = text_to_children(item[3:])
        li.append(ParentNode("li", children))
    return ParentNode("ol", li)


def create_html_ul(block):
    items = block.split("\n")
    li = []
    for item in items:
        children = text_to_children(item[2:])
        li.append(ParentNode("li", children))
    return ParentNode("ul", li)


def create_html_quote(block):
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        quote_lines.append(line.strip(">").strip())
    children = text_to_children(" ".join(quote_lines))
    return ParentNode("blockquote", children)
