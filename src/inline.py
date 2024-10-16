from os.path import split
import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for node in old_nodes:
        if node.text_type != Text_type_TEXT:
            new_nodes.append(node)

        if node.text_type == Text_type_TEXT:
            if node.text.count(delimiter) % 2 != 0:
                raise Exception(f"Invalid markup in {node}")

            node_list = node.text.split(delimiter)

            if node.text.count(delimiter) % 2 != 0:
                raise Exception('Invalid markdown code')

            for index, segment in enumerate(node_list):
                if index % 2 != 0:
                    new_nodes.append(TextNode(segment, text_type))
                else:
                    new_nodes.append(TextNode(segment, Text_type_TEXT))

    return new_nodes

def process_all_delimiters(old_nodes):
    new_nodes = split_nodes_delimiter(old_nodes, '`', Text_type_CODE)
    new_nodes = split_nodes_delimiter(new_nodes, '**', Text_type_BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '*', Text_type_ITALIC)

    return new_nodes


def extract_markdown_images(text):
    images = re.findall(r'\!\[(.*?)\]\((.*?)\)', text)
    return images

def extract_markdown_links(text):
    links = re.findall(r'\[(.*?)\]\((.*?)\)', text)
    return links

def split_nodes_image(old_nodes):
    new_nodes =[]
    for node in old_nodes:
        if node.text_type == Text_type_TEXT:
            links = extract_markdown_images(node.text)
            links_dict = {}
            for text, link in links:
                links_dict[text] = link
            split_node = re.split(r'\!\[(.*?)\]\((.*?)\)', node.text)
            for item in split_node:
                if item in links_dict:
                    new_nodes.append(TextNode(item, Text_type_IMAGE, links_dict[item]))
                    split_node.remove(links_dict[item])
                else:
                    if item != '':
                        new_nodes.append(TextNode(item, Text_type_TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes =[]
    for node in old_nodes:
        if node.text_type == Text_type_TEXT:
            links = extract_markdown_links(node.text)
            links_dict = {}
            for text, link in links:
                links_dict[text] = link
            split_node = re.split(r'\[(.*?)\]\((.*?)\)', node.text)
            for item in split_node:
                if item in links_dict:
                    new_nodes.append(TextNode(item, Text_type_LINK, links_dict[item]))
                    split_node.remove(links_dict[item])
                else:
                    if item != '':
                        new_nodes.append(TextNode(item, Text_type_TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, Text_type_TEXT)
    new_nodes = split_nodes_image([text_node])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = process_all_delimiters(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    new_blocks = []
    for block in blocks:
        new_block = block.strip(' \n')
        new_blocks.append(new_block)
    for block in new_blocks:
        if block == '':
            new_blocks.remove(block)
    return new_blocks

def block_to_block_type(block):
    if re.match(r'#{1,6} ', block):
        return 'heading'
    if re.match(r'\`\`\`(.*?)\`\`\`', block):
        return 'code'
    if block.startswith('>'):
        lines = block.split('\n')
        for line in lines:
            if not line.startswith('>'):
                return 'paragraph'
        return 'quote'
    if block.startswith('* '):
        lines = block.split('\n')
        for line in lines:
            if not line.startswith('* '):
                return 'paragraph'
        return 'unordered_list'
    if block.startswith('- '):
        lines = block.split('\n')
        for line in lines:
            if not line.startswith('- '):
                return 'paragraph'
        return 'unordered_list'
    if block.startswith('1. '):
        lines = block.split('\n')
        i=1
        for line in lines:
            if line.startswith(f'{i}. '):
                i += 1
            else:
                return 'paragraph'
        return 'ordered_list'
    else:
        return 'paragraph'



