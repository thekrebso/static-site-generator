import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        leafNode = LeafNode("img", "", { "src": "/path", "alt": "alt text" })
        self.assertEqual(
            leafNode.to_html(),
            '<img src="/path" alt="alt text"></img>'
        )

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


class TestParentNode(unittest.TestCase):
    def test_to_html_shouldRaiseWithoutATag1(self):
        leafNode = LeafNode(None, "Leaf node without a tag")
        parentNode = ParentNode(None, [leafNode]) # type: ignore
        self.assertRaises(ValueError, parentNode.to_html)

    def test_to_html_shouldRaiseWithoutATag2(self):
        leafNode = LeafNode(None, "Leaf node without a tag")
        parentNode = ParentNode("", [leafNode]) # type: ignore
        self.assertRaises(ValueError, parentNode.to_html)
        
    def test_to_html_shouldRaiseWithoutChildren1(self):
        parentNode = ParentNode("p", None) # type: ignore
        self.assertRaises(ValueError, parentNode.to_html)

    def test_to_html_shouldRaiseWithoutChildren2(self):
        parentNode = ParentNode("p", []) # type: ignore
        self.assertRaises(ValueError, parentNode.to_html)
    
    def test_to_html_shouldWorkWithoutNestedChildred(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        )

    def test_to_html_shouldWorkWithNestedChildren(self):
        leafNode1 = LeafNode(None, "This is a leaf node without tag")
        leafNode2 = LeafNode("p", "This is a leaf node in p tag")

        parentNode1 = ParentNode("div", [leafNode1, leafNode2], { "font-size": "12" })

        leafNode3 = LeafNode("p", "This is a leaf node in p tag with props", { "color": "red", "background-color": "blue" })
        parentNode2 = ParentNode("body", [leafNode3, parentNode1], { "font-size": "16" })

        self.assertEqual(
            parentNode2.to_html(),
            '<body font-size="16"><p color="red" background-color="blue">This is a leaf node in p tag with props</p><div font-size="12">This is a leaf node without tag<p>This is a leaf node in p tag</p></div></body>'
        )

    def test_to_html_shouldWorkWithMultipleNestedChildren(self):
        leafNode1 = LeafNode("b", "Bold text")
        leafNode2 = LeafNode(None, "Normal text")

        parentNode1 = ParentNode("p", [leafNode1])
        parentNode2 = ParentNode("div", [parentNode1], { "color": "red", "font-size": "12" })
        parentNode3 = ParentNode("div", [parentNode2, leafNode2])
        parentNode4 = ParentNode("body", [parentNode3], { "font-size": "16" })

        self.assertEqual(
            parentNode4.to_html(),
            '<body font-size="16"><div><div color="red" font-size="12"><p><b>Bold text</b></p></div>Normal text</div></body>'
        )


if __name__ == "__main__":
    unittest.main()
