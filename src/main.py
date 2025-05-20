from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


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


def split_nodes_delimiter(old_nodes: list['TextNode'], delimiter: str, text_type: TextType):
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


def main():
    textNode1 = TextNode("Some bold text", TextType.BOLD)
    textNode2 = TextNode("Some anchor text", TextType.LINK, "https://github.com")
    htmlNode1 = HTMLNode(None, None, None, None)
    htmlNode2 = HTMLNode("h1", "this is a text inside a tag", [htmlNode1], { "target": "_blank" })

    print(textNode1)
    print(textNode2)
    print(htmlNode1)
    print(htmlNode2)



if __name__ == "__main__":
    main()
