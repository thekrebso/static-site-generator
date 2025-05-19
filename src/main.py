from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


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
