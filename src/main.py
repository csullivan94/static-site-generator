from htmlnode import *
from textnode import *
from website import *

def main():

    copy_static()
    generate_page_recursive('./content', './template.html', './public')


main()