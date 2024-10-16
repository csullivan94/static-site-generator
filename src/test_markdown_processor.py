import unittest
from htmlnode import *
from textnode import *
from inline import *
from markdown_processor import *

class TestMarkdownProcessor(unittest.TestCase):


    def test_markdown_to_html_node_heading(self):
        markdown = '''### This is the heading

## This is a smaller heading'''
        html_node = HTMLNode('div', children=[
            LeafNode('h3', 'This is the heading'),
            LeafNode('h2', 'This is a smaller heading')
        ])
        self.assertEqual(markdown_to_html_node(markdown), html_node)

    def test_markdown_to_html_node_heading_bold(self):
        markdown = '''# This is a **bold heading**'''
        html_node = HTMLNode('div', children=[
            ParentNode('h1', children=[
                LeafNode(value='This is a '),
                LeafNode('b', 'bold heading')
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), html_node)


    def test_markdown_to_html_node_paragraph(self):
        markdown = '''Then I have a paragraph of text. Some of it will be in **bold** and some of it will be in *italic*. There might even be a [link](www.google.com).
'''
        html_node = HTMLNode('div', children=[
            ParentNode('p', children=[
                LeafNode(value='Then I have a paragraph of text. Some of it will be in '),
                LeafNode('b', 'bold'),
                LeafNode(value=' and some of it will be in '),
                LeafNode('i', 'italic'),
                LeafNode(value='. There might even be a '),
                LeafNode('a', 'link', {'href': 'www.google.com'}),
                LeafNode(value='.')
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), html_node)

    def test_markdown_to_html_node_paragraph_link(self):
        markdown = '['

    def test_markdown_to_html_node_paragraph_text(self):
        markdown = 'This paragraph is just plain text.'
        html_node = HTMLNode('div', children=[
            LeafNode('p', 'This paragraph is just plain text.')
        ])
        self.assertEqual(markdown_to_html_node(markdown), html_node)

    def test_markdown_to_html_node_code(self):
        markdown = '```This is some python code. print("hello world")```'
        html_node = HTMLNode('div', children=[
            ParentNode('pre', children=[
                LeafNode('code', 'This is some python code. print("hello world")')
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), html_node)

    def test_markdown_to_html_node_unordered(self):
        markdown = '''- There will be no bugs
- everything will work perfectly first time
- all the testcases will pass'''
        html_node = HTMLNode('div', children=[
            ParentNode('ul', children=[
                LeafNode('li', 'There will be no bugs'),
                LeafNode('li', 'everything will work perfectly first time'),
                LeafNode('li', 'all the testcases will pass')
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), html_node)

    def test_markdown_to_html_node_unordered_italic(self):
        markdown = '''- There will be no bugs
- everything will work perfectly first time
- *all* the testcases will pass'''
        html_node = HTMLNode('div', children=[
            ParentNode('ul', children=[
                LeafNode('li', 'There will be no bugs'),
                LeafNode('li', 'everything will work perfectly first time'),
                ParentNode('li', children=[
                    LeafNode('i', 'all'),
                    LeafNode(value=' the testcases will pass')
                    ])
                ])
            ])
        self.assertEqual(markdown_to_html_node(markdown), html_node)

    def test_markdown_to_html_node_unordered_star(self):
            markdown = '''* There will be no bugs
* everything will work perfectly first time
* all the testcases will pass'''
            html_node = HTMLNode('div', children=[
                ParentNode('ul', children=[
                    LeafNode('li', 'There will be no bugs'),
                    LeafNode('li', 'everything will work perfectly first time'),
                    LeafNode('li', 'all the testcases will pass')
                ])
            ])
            self.assertEqual(markdown_to_html_node(markdown), html_node)

    def test_markdown_to_html_node_unordered_italic_star(self):
            markdown = '''* There will be no bugs
* everything will work perfectly first time
* *all* the testcases will pass'''
            html_node = HTMLNode('div', children=[
                ParentNode('ul', children=[
                    LeafNode('li', 'There will be no bugs'),
                    LeafNode('li', 'everything will work perfectly first time'),
                    ParentNode('li', children=[
                        LeafNode('i', 'all'),
                        LeafNode(value=' the testcases will pass')
                    ])
                ])
            ])
            self.assertEqual(markdown_to_html_node(markdown), html_node)

    def test_markdown_to_html_node_ordered(self):
        markdown = '''1. There will be no bugs
2. everything will work perfectly first time
3. all the testcases will pass'''
        html_node = HTMLNode('div', children=[
            ParentNode('ol', children=[
                LeafNode('li', 'There will be no bugs'),
                LeafNode('li', 'everything will work perfectly first time'),
                LeafNode('li', 'all the testcases will pass')
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), html_node)


    def test_markdown_to_html_node_quote(self):
        markdown = '''>Then I have a paragraph of text.
>Some of it will be in **bold** and some of it will be in *italic*.'''
        html_node = HTMLNode('div', children=[
            ParentNode('blockquote', children=[
                LeafNode(value='''Then I have a paragraph of text.
Some of it will be in '''),
                LeafNode('b', 'bold'),
                LeafNode(value=' and some of it will be in '),
                LeafNode('i', 'italic'),
                LeafNode(value='.')
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), html_node)

    def test_markdown_to_html_node_quote_text(self):
        markdown = '>This paragraph is just plain text.'
        html_node = HTMLNode('div', children=[
            LeafNode('blockquote', 'This paragraph is just plain text.')
        ])
        self.assertEqual(markdown_to_html_node(markdown), html_node)