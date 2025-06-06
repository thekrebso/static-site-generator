from typing import Optional
import re
import os, shutil
import sys
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from blocktype import BlockType, block_to_blocktype


ROOT_PATH_DIR = "./"
STATIC_PATH_DIR = "./static"
CONTENT_PATH_DIR = "./content"
PUBLIC_PATH_DIR = "./docs"
TEMPLATE_PATH = os.path.join(ROOT_PATH_DIR, "template.html")


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
                    text += line.strip().lstrip("> ")

                root.children.append(
                    text_to_html_nodes(text, f"blockquote")
                )

            case BlockType.UNORDERED_LIST:
                list_node = ParentNode("ul", [])

                if not isinstance(list_node.children, list):
                    raise Exception("")

                for line in block.split("\n"):
                    list_node.children.append(
                        text_to_html_nodes(line.strip().lstrip("- "), f"li")
                    )

                root.children.append(list_node)

            case BlockType.ORDERED_LIST:
                list_node = ParentNode("ol", [])

                if not isinstance(list_node.children, list):
                    raise Exception("")

                for i, line in enumerate(block.split("\n")):
                    list_node.children.append(
                        text_to_html_nodes(line.strip().lstrip(f"{i+1}. "), f"li")
                    )

                root.children.append(list_node)

            case BlockType.CODE:
                root.children.append(
                    ParentNode("pre", [LeafNode("code", block.strip("```").lstrip())])
                )

            case BlockType.PARAGRAPH:
                root.children.append(
                    text_to_html_nodes(block.replace("\n", " "), f"p")
                )

    return root


def copy_static_files():
    if not os.path.exists(STATIC_PATH_DIR) or not os.path.exists(CONTENT_PATH_DIR):
       print("Exiting...")

    if os.path.exists(PUBLIC_PATH_DIR):
        shutil.rmtree(PUBLIC_PATH_DIR)

    shutil.copytree(STATIC_PATH_DIR, PUBLIC_PATH_DIR)


def extract_title(markdown: str) -> str:
    
    header = markdown.strip("\n").split("\n", maxsplit=1)[0]
    if not header.startswith("# "):
        raise Exception("Could not extract title")

    return header.strip("# ") 


def read_contents(path: str) -> str:
    with open(path) as file:
        return file.read()


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = read_contents(from_path)
    template_file = read_contents(template_path)

    title = extract_title(from_file)
    html = markdown_to_html_node(from_file).to_html()

    page = (
        template_file
            .replace("{{ Title }}", title)
            .replace("{{ Content }}", html)
            .replace('href="/', f'href="{basepath}')
            .replace('src="/', f'src="{basepath}')
    )

    if not os.path.exists(os.path.split(dest_path)[0]):
        os.makedirs(os.path.split(dest_path)[0])

    with open(dest_path, "x") as file:
        file.write(page)


def generate_pages_recursively(from_dir: str, template_path: str, to_dir: str, basepath: str):
    paths = os.listdir(from_dir)

    for path in paths:
        if os.path.isfile(os.path.join(from_dir, path)):
            filename, extension = os.path.splitext(path)

            if extension == ".md":
                generate_page(
                    os.path.join(from_dir, f"{filename}.md"),
                    template_path,
                    os.path.join(to_dir, f"{filename}.html"),
                    basepath
                )
        else:
            generate_pages_recursively(
                os.path.join(from_dir, path), 
                template_path, 
                os.path.join(to_dir, path),
                basepath
            )


def main():
    basepath = "/"
    
    if len(sys.argv) > 2:
        print("Too many arguments passed. Usage: ./main.sh [basepath=/]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        basepath = sys.argv[1]

    copy_static_files()
    generate_pages_recursively(CONTENT_PATH_DIR, TEMPLATE_PATH, PUBLIC_PATH_DIR, basepath)


if __name__ == "__main__":
    main()
