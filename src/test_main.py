import unittest

from textnode import TextType, TextNode
from main import text_node_to_html_node


class Test_TextNode_to_HTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link text", TextType.LINK, "this/is/link/url")
        html_node = text_node_to_html_node(node)

        if not isinstance(html_node.props, dict):
            self.fail()

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text")
        self.assertEqual(html_node.props["href"], "this/is/link/url")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "this/is/image/url")
        html_node = text_node_to_html_node(node)

        if not isinstance(html_node.props, dict):
            self.fail()

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "this/is/image/url")
        self.assertEqual(html_node.props["alt"], "This is an image node")

    def test_invalid(self):
        node = TextNode("This is an invalid node", None) # type: ignore
        self.assertRaises(Exception, text_node_to_html_node, node)


if __name__ == "__main__":
    unittest.main()
