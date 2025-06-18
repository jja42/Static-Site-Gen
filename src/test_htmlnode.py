import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        html_node = HTMLNode("h1", "Text goes here", None, {"href": "https://www.google.com","target": "_blank"})
        self.assertIsNotNone(html_node.props_to_html())
    
    def test_not_props(self):
        html_node = HTMLNode("h1", "Text goes here")
        self.assertIsNone(html_node.props)

    def test_props_value(self):
        html_node = HTMLNode("h1", "Text goes here", None, {"href": "https://www.google.com","target": "_blank"})
        string = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(html_node.props_to_html(),string)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")