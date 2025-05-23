from typing import Optional
import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from blocktype import BlockType, block_to_blocktype


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if isinstance(text_node.url, str):
                return LeafNode("a", text_node.text, { "href": text_node.url })
            else:
                return LeafNode("a", text_node.text, { "href": "" })
        case TextType.IMAGE:
            if isinstance(text_node.url, str):
                return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text })
            else:
                return LeafNode("img", "", { "src": "", "alt": text_node.text })
        case _:
            raise Exception("invalid TextType value")


def split_nodes_delimiter(old_nodes: list['TextNode'], delimiter: str, text_type: TextType) -> list['TextNode']:
    new_nodes: list['TextNode'] = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 == 1:
            raise Exception("invalid markdown syntax: unterminated element")
        
        new_texts = node.text.split(delimiter)

        for i, value in enumerate(new_texts):
            if i % 2 == 0:
                new_nodes.append(TextNode(value, node.text_type, node.url))
            else:
                new_nodes.append(TextNode(value, text_type, node.url))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes: list['TextNode']) -> list['TextNode']:
    new_nodes: list['TextNode'] = []
    
    for node in old_nodes:
        matches = extract_markdown_images(node.text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        texts = [node.text]
        trailing_text = False

        for match in matches:
            last_text = texts.pop()

            last_text_split = last_text.split(f"![{match[0]}]({match[1]})", maxsplit=1)

            if last_text_split[-1] == "":
                del last_text_split[-1]
                trailing_text = False
            else:
                trailing_text = True

            texts.extend(last_text_split)

        new_nodes_count = len(texts) * 2
        if trailing_text:
            new_nodes_count -= 1

        for i in range(new_nodes_count):
            if i % 2 == 0:
                text = texts[i // 2]
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                match = matches[(i - 1) // 2]
                new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))

    return new_nodes 
         

def split_nodes_link(old_nodes: list['TextNode']) -> list['TextNode']:
    new_nodes: list['TextNode'] = []

    for node in old_nodes:
        matches = extract_markdown_links(node.text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        texts = [node.text]
        trailing_text = False

        for match in matches:
            last_text = texts.pop()

            last_text_split = last_text.split(f"[{match[0]}]({match[1]})", maxsplit=1)

            if last_text_split[-1] == "":
                del last_text_split[-1]
                trailing_text = False
            else:
                trailing_text = True

            texts.extend(last_text_split)

        new_nodes_count = len(texts) * 2
        if trailing_text:
            new_nodes_count -= 1

        for i in range(new_nodes_count):
            if i % 2 == 0:
                text = texts[i // 2]
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                match = matches[(i - 1) // 2]
                new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))

    return new_nodes 


def text_to_textnodes(text: str) -> list['TextNode']:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x: x.strip(), blocks))
    blocks = list(filter(lambda x: x != "", blocks))
    return blocks


def text_to_html_nodes(text: str, parent_tag: str = "div"):
    children: list[HTMLNode] = []

    for node in text_to_textnodes(text):
        html_node = text_node_to_html_node(node)
        children.append(html_node)

    return ParentNode(parent_tag, children)
    

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)

    root = ParentNode("div", [])

    if not isinstance(root.children, list):
        raise Exception("")

    for block in blocks:
        match block_to_blocktype(block):
            case BlockType.HEADING:
                tag, text = block.split(" ", maxsplit=1)

                root.children.append(
                    text_to_html_nodes(text, f"h{tag.count("#")}")
                )

            case BlockType.QUOTE:
                text = ""

                for line in block.split("\n"):
                    line.strip()
                    line.lstrip("> ")
                    text += line

                root.children.append(
                    text_to_html_nodes(text, f"blockquote")
                )

            case BlockType.UNORDERED_LIST:
                list_node = ParentNode("ul", [])

                if not isinstance(list_node.children, list):
                    raise Exception("")

                for line in block.split():
                    line.strip()
                    line.lstrip("- ")
                    list_node.children.append(
                        text_to_html_nodes(line, f"li")
                    )

                root.children.append(list_node)

            case BlockType.ORDERED_LIST:
                list_node = ParentNode("ol", [])

                if not isinstance(list_node.children, list):
                    raise Exception("")

                for i, line in enumerate(block.split()):
                    line.strip()
                    line.lstrip(f"{i+1}. ")
                    list_node.children.append(
                        text_to_html_nodes(line, f"li")
                    )

                root.children.append(list_node)

            case BlockType.CODE:
                text = block.strip("```")
                text = text.lstrip()

                root.children.append(
                    ParentNode("pre", [LeafNode("code", text)])
                )

            case BlockType.PARAGRAPH:
                root.children.append(
                    text_to_html_nodes(block.replace("\n", " "), f"p")
                )

    return root


def main():
    textNode1 = TextNode("Some bold text", TextType.BOLD)
    textNode2 = TextNode("Some anchor text", TextType.LINK, "https://github.com")
    htmlNode1 = HTMLNode(None, None, None, None)
    htmlNode2 = HTMLNode("h1", "this is a text inside a tag", [htmlNode1], { "target": "_blank" })

    print(split_nodes_image([
        TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) in the middle of text",
            TextType.TEXT,
        )
    ]))

    print(textNode1)
    print(textNode2)
    print(htmlNode1)
    print(htmlNode2)



if __name__ == "__main__":
    main()
