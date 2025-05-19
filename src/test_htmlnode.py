import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html1(self):
        node = HTMLNode(None, None, None, None)
        
        html_props = node.props_to_html()
        
        self.assertEqual(html_props, '')

    def test_props_to_html2(self):
        node = HTMLNode(None, None, None, {})
        
        html_props = node.props_to_html()
        
        self.assertEqual(html_props, '')

    def test_props_to_html3(self):
        node = HTMLNode(None, None, None, {
            "href": "http://localhost",
        })

        html_props = node.props_to_html()

        self.assertEqual(html_props, ' href="http://localhost"')

    def test_props_to_html4(self):
        node = HTMLNode(None, None, None, {
            "href": "http://localhost",
            "target": "_blank"
        })

        html_props = node.props_to_html()

        self.assertEqual(html_props, ' href="http://localhost" target="_blank"')


if __name__ == "__main__":
    unittest.main()
