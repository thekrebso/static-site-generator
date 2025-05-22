import unittest

from textnode import TextType, TextNode
from main import (
    text_node_to_html_node, 
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks
)


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


class Test_split_nodes_delimiter(unittest.TestCase):
    def test_inline_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        actual = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            actual,
            expected,
            f"\nExpected: {expected}\nActual: {actual}"
        )

    def test_inline_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        actual = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            actual,
            expected,
            f"\nExpected: {expected}\nActual: {actual}"
        )

    def test_inline_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        actual = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            actual,
            expected,
            f"\nExpected: {expected}\nActual: {actual}"
        )

    def test_inline_italic_unterminated(self):
        node = TextNode("This is text with a _italic word", TextType.TEXT)

        self.assertRaises(
            Exception, 
            split_nodes_delimiter,
            [node], "_", TextType.ITALIC
        )

    def test_inline_multiple_same(self):
        node = TextNode("This is text with a _italic_ word and another _italic_ word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and another ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        actual = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            actual,
            expected,
            f"\nExpected: {expected}\nActual: {actual}"
        )

    def test_inline_multiple_different(self):
        node = TextNode("This is text with a _italic_ word and a **bold** word", TextType.TEXT)
        
        expected_first_pass = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a **bold** word", TextType.TEXT),
        ]
        
        expected_second_pass = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        actual_first_pass = split_nodes_delimiter([node], "_", TextType.ITALIC)
        actual_second_pass = split_nodes_delimiter(actual_first_pass, "**", TextType.BOLD)

        self.assertEqual(
            actual_first_pass,
            expected_first_pass,
            f"\n----- First split -----\nExpected: {expected_first_pass}\nActual: {actual_first_pass}"
        )

        self.assertEqual(
            actual_second_pass,
            expected_second_pass,
            f"\n----- Second split -----\nExpected: {expected_second_pass}\nActual: {actual_second_pass}"
        )


class Test_extract_md_images(unittest.TestCase):
    def test_works1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]

        actual = extract_markdown_images(text)

        self.assertEqual(actual, expected, 
                         f"\nExpected: {expected}\nActual: {actual}")

    def test_works2(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [
            ("image", "https://i.imgur.com/zjjcJKZ.png")
        ]

        actual = extract_markdown_images(text)

        self.assertEqual(actual, expected, 
                         f"\nExpected: {expected}\nActual: {actual}")


class Test_extract_md_links(unittest.TestCase):
    def test_works(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]

        actual = extract_markdown_links(text)

        self.assertEqual(actual, expected, 
                         f"\nExpected: {expected}\nActual: {actual}")


class Test_split_nodes_image(unittest.TestCase):
    def test_without(self):
        node = TextNode(
            "This is text without any images",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text without any images", TextType.TEXT),
        ]

        actual = split_nodes_image([node])

        self.assertListEqual(actual, expected)

    def test_works1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]

        actual = split_nodes_image([node])

        self.assertListEqual(actual, expected)

    def test_works2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) in the middle of text",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" in the middle of text", TextType.TEXT)
        ]

        actual = split_nodes_image([node])

        self.assertListEqual(actual, expected)


class Test_split_nodes_link(unittest.TestCase):
    def test_without(self):
        node = TextNode(
            "This is text without any links",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text without any links", TextType.TEXT),
        ]

        actual = split_nodes_link([node])

        self.assertListEqual(actual, expected)

    def test_works1(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]

        actual = split_nodes_link([node])

        self.assertListEqual(actual, expected)

    def test_works2(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) in the middle of text",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" in the middle of text", TextType.TEXT),
        ]

        actual = split_nodes_link([node])

        self.assertListEqual(actual, expected)


class Test_text_to_textnodes(unittest.TestCase):
    def test_works(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        actual = text_to_textnodes(text)

        self.assertListEqual(actual, expected)


class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]

        actual = markdown_to_blocks(md)

        self.assertListEqual(
            actual,
            expected
        )


if __name__ == "__main__":
    unittest.main()
