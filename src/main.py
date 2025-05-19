from textnode import TextNode, TextType


def main():
    textNode = TextNode("Some anchor text", TextType.LINK, "https://github.com")

    print(textNode)


if __name__ == "__main__":
    main()
