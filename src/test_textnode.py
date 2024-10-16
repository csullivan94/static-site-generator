import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", 'BOLD')
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode('testing', 'italic', 'url')
        node1 = TextNode('testing', 'bold', 'url')
        self.assertNotEqual(node, node1)

    def test_url(self):
        node = TextNode('testing', 'italic', None)
        node1 = TextNode('testing', 'italic')
        self.assertEqual(node, node1)


class TestTextToHTML(unittest.TestCase):

    def test_leaf_node_text(self):
        text = TextNode('This is plain unformatted text', 'text')
        expected_leaf = LeafNode(value='This is plain unformatted text')
        self.assertEqual(text_node_to_html_node(text), expected_leaf)

    def test_leaf_node_bold(self):
        text_bold = TextNode('This text is bold', 'bold')
        expected_leaf_bold = LeafNode('b', 'This text is bold')
        self.assertEqual(text_node_to_html_node(text_bold), expected_leaf_bold)

    def test_leaf_node_italic(self):
        text_italic = TextNode('This text is italic', 'italic')
        expected_leaf_italic = LeafNode('i', 'This text is italic')
        self.assertEqual(text_node_to_html_node(text_italic), expected_leaf_italic)

    def test_leaf_node_code(self):
        text_code = TextNode('This text is code', 'code')
        expected_leaf_code = LeafNode('code', 'This text is code')
        self.assertEqual(text_node_to_html_node(text_code), expected_leaf_code)

    def test_leaf_node_link(self):
        text_link = TextNode('This text is a link', 'link', 'url')
        expected_leaf_link = LeafNode('a', 'This text is a link', {'href':'url'})
        self.assertEqual(text_node_to_html_node(text_link), expected_leaf_link)

    def test_leaf_node_image(self):
        text_image = TextNode('This is an image', 'image', 'url')
        expected_leaf_image = LeafNode('img', '', {'src':'url', 'alt':'This is an image'})
        self.assertEqual(text_node_to_html_node(text_image), expected_leaf_image)

    def test_invalid_text_type(self):
        with self.assertRaises(Exception):
            text = TextNode('This node has an invalid text type', 'underline')
            text_node_to_html_node(text)

if __name__ == "__main__":
    unittest.main()