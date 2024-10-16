from inline import *
import unittest


class TestInline(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        old_nodes = [TextNode("This is text with a `code block` word", 'text'),
                     TextNode('This is bold', 'bold'),
                     TextNode('This is **italic**', 'text'),
                     TextNode('This is *bold*', 'text')
                     ]
        test_function = split_nodes_delimiter(old_nodes, '`', 'code')
        test_string = [TextNode('This is text with a ', 'TEXT', url=None), TextNode('code block', 'CODE', url=None), TextNode(' word', 'TEXT', url=None), TextNode('This is bold', 'BOLD', url=None), TextNode('This is **italic**', 'TEXT', url=None), TextNode('This is *bold*', 'TEXT', url=None)]
        self.assertEqual(test_string, test_function)

    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode("This is text with a `code block` word", 'text'),
                     TextNode('This is bold', 'bold'),
                     TextNode('This is *italic*', 'text'),
                     TextNode('This is **bold**', 'text')
                     ]
        test_function = split_nodes_delimiter(old_nodes, '**', 'bold')
        test_string = [TextNode('This is text with a `code block` word', 'TEXT', url=None), TextNode('This is bold', 'BOLD', url=None), TextNode('This is *italic*', 'TEXT', url=None), TextNode('This is ', 'TEXT', url=None), TextNode('bold', 'BOLD', url=None), TextNode('', 'text', url=None)]
        self.assertEqual(test_string, test_function)


    def test_invalid_markup(self):
        self.assertRaises(Exception)
        old_nodes = [TextNode("This is text with a `code block word", 'text'),
                     TextNode('This is bold', 'bold'),
                     TextNode('This is **bold**', 'italic'),
                     TextNode('This is *italic*', 'text')
                     ]

    def test_process_all_delimiters(self):
        old_nodes = [TextNode("This is text with a `code block` word", 'text'),
                     TextNode('This is bold', 'bold'),
                     TextNode('This is **bold**', 'text'),
                     TextNode('This is *italic*', 'text')
                     ]
        test_list = [TextNode('This is text with a ', 'TEXT', url=None), TextNode('code block', 'CODE', url=None), TextNode(' word', 'TEXT', url=None), TextNode('This is bold', 'BOLD', url=None), TextNode('This is ', 'TEXT', url=None), TextNode('bold', 'BOLD', url=None), TextNode('', 'TEXT', url=None), TextNode('This is ', 'TEXT', url=None), TextNode('italic', 'ITALIC', url=None), TextNode('', 'TEXT', url=None)]
        self.assertEqual(process_all_delimiters(old_nodes), test_list)


    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text_list = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(extract_markdown_images(text), text_list)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        test_list = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(extract_markdown_links(text), test_list)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            Text_type_TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes_list = [
             TextNode("This is text with a link ", Text_type_TEXT),
             TextNode("to boot dev", Text_type_LINK, "https://www.boot.dev"),
             TextNode(" and ", Text_type_TEXT),
             TextNode(
                 "to youtube", Text_type_LINK, "https://www.youtube.com/@bootdotdev"
             ),
         ]
        self.assertEqual(new_nodes, new_nodes_list)

    def test_split_nodes_image(self):
        node = TextNode("This is a text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", Text_type_TEXT)
        new_nodes = split_nodes_image([node])
        new_nodes_list = [
            TextNode('This is a text with a ', Text_type_TEXT),
            TextNode('rick roll', Text_type_IMAGE, 'https://i.imgur.com/aKaOqIh.gif'),
            TextNode(' and ', Text_type_TEXT),
            TextNode('obi wan', Text_type_IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg')
        ]
        self.assertEqual(new_nodes, new_nodes_list)

    def test_split_nodes_links_with_none(self):
        nodes = [TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            Text_type_TEXT),
            TextNode("This is a text with a rick roll https://i.imgur.com/aKaOqIh.gif and obi wan https://i.imgur.com/fJRm4Vk.jpeg", Text_type_TEXT)
            ]
        new_nodes = split_nodes_link(nodes)
        new_nodes_list = [
             TextNode("This is text with a link ", Text_type_TEXT),
             TextNode("to boot dev", Text_type_LINK, "https://www.boot.dev"),
             TextNode(" and ", Text_type_TEXT),
             TextNode(
                 "to youtube", Text_type_LINK, "https://www.youtube.com/@bootdotdev"
             ),
             TextNode(
                "This is a text with a rick roll https://i.imgur.com/aKaOqIh.gif and obi wan https://i.imgur.com/fJRm4Vk.jpeg",
                Text_type_TEXT)
         ]
        self.assertEqual(new_nodes, new_nodes_list)

    def test_split_nodes_images_and_none(self):
        nodes = [TextNode(
            "This is text with a link to boot dev https://www.boot.dev and to youtube https://www.youtube.com/@bootdotdev",
            Text_type_TEXT),
            TextNode("This is a text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", Text_type_TEXT)
            ]
        new_nodes = split_nodes_image(nodes)
        new_nodes_list = [
            TextNode("This is text with a link to boot dev https://www.boot.dev and to youtube https://www.youtube.com/@bootdotdev", Text_type_TEXT),
            TextNode('This is a text with a ', Text_type_TEXT),
            TextNode('rick roll', Text_type_IMAGE, 'https://i.imgur.com/aKaOqIh.gif'),
            TextNode(' and ', Text_type_TEXT),
            TextNode('obi wan', Text_type_IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg')
        ]
        self.assertEqual(new_nodes, new_nodes_list)

    def test_split_nodes_images_first(self):
        nodes = [
            TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", Text_type_TEXT)
            ]
        new_nodes = split_nodes_image(nodes)
        new_nodes_list = [
            TextNode('rick roll', Text_type_IMAGE, 'https://i.imgur.com/aKaOqIh.gif'),
            TextNode(' and ', Text_type_TEXT),
            TextNode('obi wan', Text_type_IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg')
        ]
        self.assertEqual(new_nodes, new_nodes_list)

    def test_split_nodes_links_first(self):
        nodes = [TextNode(
            "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            Text_type_TEXT),
            ]
        new_nodes = split_nodes_link(nodes)
        new_nodes_list = [
             TextNode("to boot dev", Text_type_LINK, "https://www.boot.dev"),
             TextNode(" and ", Text_type_TEXT),
             TextNode(
                 "to youtube", Text_type_LINK, "https://www.youtube.com/@bootdotdev"
             )
         ]
        self.assertEqual(new_nodes, new_nodes_list)

    def test_text_to_textnodes(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        new_nodes = [
            TextNode("This is ", Text_type_TEXT),
            TextNode("text", Text_type_BOLD),
            TextNode(" with an ", Text_type_TEXT),
            TextNode("italic", Text_type_ITALIC),
            TextNode(" word and a ", Text_type_TEXT),
            TextNode("code block", Text_type_CODE),
            TextNode(" and an ", Text_type_TEXT),
            TextNode("obi wan image", Text_type_IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", Text_type_TEXT),
            TextNode("link", Text_type_LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), new_nodes)

    def test_markdown_to_blocks(self):
        markdown = ('''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item''')
        blocks = ['# This is a heading',
                  'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                  '''* This is the first list item in a list block
* This is a list item
* This is another list item'''
                  ]
        self.assertEqual(markdown_to_blocks(markdown), blocks)

    def test_markdown_to_blocks_one_block(self):
        markdown = ('This is just a paragraph of text with no other blocks.')
        blocks = ['This is just a paragraph of text with no other blocks.']
        self.assertEqual(markdown_to_blocks(markdown), blocks)

    def test_markdown_to_blocks_whitespace(self):
        markdown = '''# This heading is followed by too many new lines


Before the new paragraph of text'''
        blocks = ['# This heading is followed by too many new lines', 'Before the new paragraph of text']
        self.assertEqual(markdown_to_blocks(markdown), blocks)

    def test_block_to_block_type_paragraph(self):
        block = 'This is just a paragraph of text with no other blocks.'
        block_type = 'paragraph'
        self.assertEqual(block_to_block_type(block), block_type)

    def test_block_to_block_type_heading(self):
        block = '#### This is a heading'
        block_type = 'heading'
        self.assertEqual(block_to_block_type(block), block_type)

    def test_block_to_block_type_code(self):
        block = '```this is a code block```'
        block_type = 'code'
        self.assertEqual(block_to_block_type(block), block_type)

    def test_block_to_block_type_quote(self):
        block = '>this is a quote block'
        block_type = 'quote'
        self.assertEqual(block_to_block_type(block), block_type)

    def test_block_to_block_type_quote_multiline(self):
        block = ('''>this is a quote block
>with multiple lines''')
        block_type = 'quote'
        self.assertEqual(block_to_block_type(block), block_type)

    def test_block_to_block_type_quote_false(self):
        block = ('''>this is not a quote block
>the multiple lines
don't all start correctly''')
        block_type = 'paragraph'
        self.assertEqual(block_to_block_type(block), block_type)


    def test_block_to_block_type_unordered_list_star(self):
        block = '''* this is a list
* without an order
* but multiple lines'''
        block_type = 'unordered_list'
        self.assertEqual(block_to_block_type(block), block_type)

    def test_block_to_block_type_unordered_list_false(self):
        block = '''* this is a list
without an order
* but multiple lines'''
        block_type = 'paragraph'
        self.assertEqual(block_to_block_type(block), block_type)

    def test_block_to_block_type_unordered_list_dash(self):
        block = '''- this is a list
- without an order
- but multiple lines'''
        block_type = 'unordered_list'
        self.assertEqual(block_to_block_type(block), block_type)


    def test_block_to_block_type_ordered_list(self):
        block = '''1. this is a list
2. with an order
3. but multiple lines'''
        block_type = 'ordered_list'
        self.assertEqual(block_to_block_type(block), block_type)


    def test_block_to_block_type_ordered_list_false(self):
        block = '''1. this is a list
2. with an order
2. but multiple lines'''
        block_type = 'paragraph'
        self.assertEqual(block_to_block_type(block), block_type)

