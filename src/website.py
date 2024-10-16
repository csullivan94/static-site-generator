import shutil
import os
from inline import *
from markdown_processor import *



def copy_static(base_path = './static', paths=None):
    if os.path.exists('./public'):
        shutil.rmtree('public')
        os.mkdir('public')
    if paths is None:
        paths = []
    if os.path.isdir(base_path):
        dir_list = os.listdir(base_path)
        for path in dir_list:
            new_path = os.path.join(base_path, path)
            paths.append(new_path)
            if os.path.isdir(new_path):
                copy_static(new_path, paths)
    for path in paths:
        if os.path.isdir(path):
            path_list = path.split('/')
            path_list[1] = 'public'
            new_path = '/'.join(path_list)
            if not os.path.exists(new_path):
                os.mkdir(new_path)
        if os.path.isfile(path):
            path_list = path.split('/')
            path_list[1] = 'public'
            new_path = '/'.join(path_list)
            if not os.path.exists(new_path):
                shutil.copy(path, new_path)
    return paths

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if '# ' in block:
            return block.strip('# ')
    if '# ' not in blocks:
        raise Exception('no title')


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    markdown = read_file(from_path)
    template = read_file(template_path)
    html_nodes = markdown_to_html_node(markdown)
    html_string = html_nodes.to_html()
    title = extract_title(markdown)
    html = template.replace('{{ Title }}', title).replace('{{ Content }}', html_string)
    dest_path_list = dest_path.split('/')
    dest_path_dir = '/'.join(dest_path_list[:-1])
    if os.path.exists(dest_path_dir):
        with open(dest_path, 'w') as f:
            f.write(html)
    else:
        os.makedirs(dest_path_dir)
        with open(dest_path, 'w') as f:
            f.write(html)

def read_file(file_path):
    open_file = open(file_path)
    content = open_file.read()
    open_file.close()
    return content

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    dir_path_content_list = os.listdir(dir_path_content)
    for item in dir_path_content_list:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            item_path_list = item_path.split('/')
            item_path_list[1] = 'public'
            dest_item_path = '/'.join(item_path_list)
            if not os.path.exists(dest_item_path):
                os.mkdir(dest_item_path)
                generate_page_recursive(item_path, template_path, dest_item_path)
        if os.path.isfile(item_path):
            item_path_list = item_path.split('/')
            item_path_list[1] = 'public'
            item_path_list[-1] = item_path_list[-1].replace('.md', '.html')
            dest_item_path = '/'.join(item_path_list)
            generate_page(item_path, template_path, dest_item_path)




