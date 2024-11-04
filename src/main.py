from textnode import *
from htmlnode import *
from split_nodes_delimiter import *
from text_to_textNodes import *
from markdown_to_blocks import *
from markdown_to_html import *
from generate_page import *
import os
import shutil

def copy_files(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
        os.mkdir(dest)
    else:
        os.mkdir(dest)
    
    files = os.listdir(source)

    for name in files:
        file = os.path.join(source, name)
        if os.path.isfile(file):
            shutil.copy(file, dest)
            print("Copied file " + file)
        else:
            new_source = os.path.join(source, name)
            new_destination = os.path.join(dest, name)
            copy_files(new_source, new_destination)
    

def main():
    shutil.rmtree("./public")
    source = "./static"
    destination = "./public"
    copy_files(source, destination)
    generate_pages_recursive("./content", "template.html", "./public")

main()
