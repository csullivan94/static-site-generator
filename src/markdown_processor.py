from textnode import *
from htmlnode import *
from inline import *



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_nodes = []
    for block in blocks:
        parent_nodes.append(parent_node_builder(block))
    return ParentNode('div', children = parent_nodes)


def parent_node_builder(block):
    if block_to_block_type(block) == 'paragraph':
        return paragraph_parent_node(block)
    if block_to_block_type(block) == 'heading':
        return heading_parent_node(block)
    if block_to_block_type(block) == 'code':
        return code_parent_node(block)
    if block_to_block_type(block) == 'quote':
        return quote_parent_node(block)
    if block_to_block_type(block) == 'unordered_list':
        return unordered_list_parent_node(block)
    if block_to_block_type(block) == 'ordered_list':
        return ordered_list_parent_node(block)

def heading_parent_node(block):
    count = block.count('#')
    text_nodes = text_to_textnodes(block.strip('# '))
    html_nodes =[]
    for node in text_nodes:
        if node.text != '':
            html_nodes.append(text_node_to_html_node(node))
    if len(text_nodes) == 1:
        return LeafNode(f'h{count}', block.strip('# ') )
    return ParentNode(f'h{count}', children= html_nodes)

def paragraph_parent_node(block):
    text_nodes = text_to_textnodes(block)
    if len(text_nodes) == 1 and text_nodes[0].text_type == Text_type_TEXT:
        return LeafNode('p', block)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode('p', children= html_nodes)

def code_parent_node(block):
    return ParentNode('pre', children=[LeafNode('code', block.strip('`'))])

def unordered_list_parent_node(block):
    lines = block.split('\n')
    text_nodes_lines = []
    for line in lines:
        if line.startswith('-'):
            text_nodes_lines.append(text_to_textnodes(line.split('- ', 1)[1]))
        if line.startswith('*'):
            text_nodes_lines.append(text_to_textnodes(line.split('* ', 1)[1]))
    html_nodes = []
    for line in text_nodes_lines:
        if len(line) == 1:
            for node in line:
                html_nodes.append(LeafNode('li', node.text))
        if len(line) > 1:
            children = []
            for node in line:
                if node.text != '':
                    children.append(text_node_to_html_node(node))
            html_nodes.append(ParentNode('li', children = children))
    return ParentNode('ul', children = html_nodes)

def ordered_list_parent_node(block):
    lines = block.split('\n')
    text_nodes_lines = []
    for line in lines:
        text_nodes_lines.append(text_to_textnodes(re.split(r'\d. ', line, 1)[1]))
    html_nodes = []
    for line in text_nodes_lines:
        if len(line) == 1:
            for node in line:
                html_nodes.append(LeafNode('li', node.text))
        if len(line) > 1:
            children = []
            for node in line:
                if node.text != '':
                    children.append(text_node_to_html_node(node))
            html_nodes.append(ParentNode('li', children = children))
    return ParentNode('ol', children = html_nodes)

def link_parent_node(block):
    pass

def quote_parent_node(block):
    block_lines = []
    lines = block.split('\n')
    for line in lines:
        block_lines.append(line.strip('> '))
    new_block = '\n'.join(block_lines)
    text_nodes = text_to_textnodes(new_block)
    if len(text_nodes) == 1:
        return LeafNode('blockquote', new_block)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode('blockquote', children= html_nodes)











