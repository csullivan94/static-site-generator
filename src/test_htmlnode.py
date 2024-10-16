import unittest

from cryptography.hazmat.primitives.keywrap import aes_key_wrap

from htmlnode import *
from src.textnode import TextNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        child = HTMLNode()
        node = HTMLNode('a', 'This is the test value.', [child], {'href': 'https://www.google.com'})
        node1 = HTMLNode('a', 'This is the test value.', [child], {'href': 'https://www.google.com'})
        self.assertEqual(node, node1)

    def test_missing_members(self):
        node = HTMLNode('a', 'This is the test value.',props ={'href': 'https://www.google.com'})
        node1 = HTMLNode('a', 'This is the test value.', props={'href': 'https://www.google.com'})
        node2 = HTMLNode()
        node3 = HTMLNode()
        self.assertEqual(node2, node3)
        self.assertEqual(node.children, node1.children)

    def test_not_eq(self):
        child = HTMLNode()
        node = HTMLNode('a', 'This is the test value.', [child], {'href': 'https://www.google.com'})
        node1 = HTMLNode()
        self.assertNotEqual(node, node1)

    def test_props_to_html(self):
        props = {'key1':'value1', 'key2': 'value2'}
        node = HTMLNode(props=props)
        props_str = ' key1="value1" key2="value2"'
        self.assertEqual(node.props_to_html(), props_str)

    def test_repr(self):
        node = HTMLNode('a', 'text')
        expected_repr = 'HTMLNode(tag="a", value="text", children=[], props={})'
        self.assertEqual(repr(node), expected_repr)

class TestLeafNode(unittest.TestCase):

    def test_leaf(self):
        leaf = LeafNode('b', 'This is a leaf node.')
        expected_repr = 'LeafNode(tag="b", value="This is a leaf node.", props={})'
        self.assertEqual(expected_repr, repr(leaf))

    def test_leaf_props(self):
        leaf = LeafNode('a', 'This leaf has props.', {'href':'insert link here'})
        expected_repr = 'LeafNode(tag="a", value="This leaf has props.", props={\'href\': \'insert link here\'})'
        self.assertEqual(repr(leaf), expected_repr)

    def test_leaf_missing_value(self):
        with self.assertRaises(ValueError):
            leaf = LeafNode('b')

    def test_leaf_children(self):
        with self.assertRaises(TypeError):
            leaf = LeafNode('a', 'value', children=['test'])

    def test_leaf_to_html(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        leaf1 = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        leaf_html = '<p>This is a paragraph of text.</p>'
        leaf1_html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(leaf.to_html(), leaf_html)
        self.assertEqual(leaf1.to_html(), leaf1_html)

    def test_leaf_to_html_no_tags(self):
        leaf = LeafNode(value='This has no tag.')
        html = 'This has no tag.'
        self.assertEqual(leaf.to_html(), html)

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(
            "p", children =[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node1 = ParentNode(
            "p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(value="Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(value="Normal text"),
            ],
        )
        self.assertEqual(node, node1)

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(children=
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )


    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p")

    def test_to_html_str(self):
        node = ParentNode(
            "p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), html)

    def test_nested_to_html(self):
        node = ParentNode(
            "p",
            children=[
                LeafNode("b", "Bold text"),
                ParentNode("p", children=[LeafNode("b", "Bold text"),
                                          LeafNode(None, "Normal text"),
                                          LeafNode("i", "italic text"),
                                          LeafNode(None, "Normal text"),
                                          ]),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ],
        )
        html = '<p><b>Bold text</b><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), html)

