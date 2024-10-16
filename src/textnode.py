from htmlnode import *

Text_type_TEXT = 'TEXT'
Text_type_BOLD = 'BOLD'
Text_type_ITALIC = 'ITALIC'
Text_type_CODE = 'CODE'
Text_type_LINK = 'LINK'
Text_type_IMAGE = 'IMAGE'


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.url = url
        self.text_type = text_type.upper()

    def __eq__(self, textnode):
        if self.text == textnode.text and self.text_type == textnode.text_type and self.url == textnode.url:
            return True
        return False

    def __repr__(self):
        return f'TextNode(text={self.text}, text_type={self.text_type}, url={self.url})'

def text_node_to_html_node(text_node):
    if text_node.text_type == Text_type_TEXT:
        return LeafNode(value=text_node.text)
    if text_node.text_type == Text_type_BOLD:
        return LeafNode('b', text_node.text)
    if text_node.text_type == Text_type_ITALIC:
        return LeafNode('i', text_node.text)
    if text_node.text_type == Text_type_CODE:
        return LeafNode('code', text_node.text)
    if text_node.text_type == Text_type_LINK:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    if text_node.text_type == Text_type_IMAGE:
        return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
    raise Exception('Invalid text type')


