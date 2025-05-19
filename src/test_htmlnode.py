import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_shouldWorkWithoutProps1(self):
        node = HTMLNode(None, None, None, None)
        
        html_props = node.props_to_html()
        
        self.assertEqual(html_props, '')

    def test_props_to_html_shouldWorkWithoutProps2(self):
        node = HTMLNode(None, None, None, {})
        
        html_props = node.props_to_html()
        
        self.assertEqual(html_props, '')

    def test_props_to_html_shouldWorkWithProp(self):
        node = HTMLNode(None, None, None, {
            "href": "http://localhost",
        })

        html_props = node.props_to_html()

        self.assertEqual(html_props, ' href="http://localhost"')

    def test_props_to_html_shouldWorkWithMultipleProps(self):
        node = HTMLNode(None, None, None, {
            "href": "http://localhost",
            "target": "_blank"
        })

        html_props = node.props_to_html()

        self.assertEqual(html_props, ' href="http://localhost" target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_to_html_shouldRaiseOnInvalidValue1(self):
        leafNode = LeafNode(None, None) # type: ignore
        self.assertRaises(ValueError, leafNode.to_html)

    def test_to_html_shouldRaiseOnInvalidValue2(self):
        leafNode = LeafNode("p", None) # type: ignore
        self.assertRaises(ValueError, leafNode.to_html)

    def test_to_html_shouldRaiseOnInvalidValue3(self):
        leafNode = LeafNode("p", "")
        self.assertRaises(ValueError, leafNode.to_html)

    def test_to_html_shouldWorkWithoutATag(self):
        leafNode = LeafNode(None, "This is a leaf node without tag")
        self.assertEqual(
            leafNode.to_html(),
            "This is a leaf node without tag"
        )

    def test_to_html_shouldWorkWithoutATagWithProps(self):
        leafNode = LeafNode(None, "This is a leaf node without tag but with props!?", { "color": "red" })
        self.assertEqual(
            leafNode.to_html(),
            "This is a leaf node without tag but with props!?"
        )

    def test_to_html_shouldWorkWithTag(self):
        leafNode = LeafNode("p", "This is a leaf node in p tag")
        self.assertEqual(
            leafNode.to_html(),
            "<p>This is a leaf node in p tag</p>"
        )

    def test_to_html_shouldWorkWithTagWithProps(self):
        leafNode = LeafNode("p", "This is a leaf node in p tag with props", { "color": "red", "background-color": "blue" })
        self.assertEqual(
            leafNode.to_html(),
            '<p color="red" background-color="blue">This is a leaf node in p tag with props</p>'
        )


if __name__ == "__main__":
    unittest.main()
