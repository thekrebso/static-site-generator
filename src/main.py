from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


def main():
    textNode1 = TextNode("Some bold text", TextType.BOLD)
    textNode2 = TextNode("Some anchor text", TextType.LINK, "https://github.com")
    htmlNode1 = HTMLNode(None, None, None, None)
    htmlNode2 = HTMLNode("h1", "this is a text inside a tag", [htmlNode1], { "target": "_blank" })
    leafNode1 = LeafNode(None, "This is a leaf node without tag")
    leafNode2 = LeafNode(None, "This is a leaf node without tag but with props!?", { "color": "red" })
    leafNode3 = LeafNode("p", "This is a leaf node in p tag")
    leafNode4 = LeafNode("p", "This is a leaf node in p tag with props", { "color": "red", "background-color": "blue" })

    print(textNode1)
    print(textNode2)
    print(htmlNode1)
    print(htmlNode2)

    print(leafNode1.to_html())
    print(leafNode2.to_html())
    print(leafNode3.to_html())
    print(leafNode4.to_html())


if __name__ == "__main__":
    main()
