from markdown_to_blocks import *
from markdown_to_html import *
import os
import pathlib

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in range(0, len(blocks)):
        if blocks[block].startswith("# "):
            title = blocks[block].strip("# ")
            return(title)
    raise Exception("There is no main header in this file")


def generate_page(from_loc, template_loc, dest_loc):
    print(f"Generating page from {from_loc} using {template_loc} to {dest_loc}.")
    source = open(from_loc, "r").read()
    template = open(template_loc, "r").read()
    source_html = markdown_to_html(source).to_html()
    title = extract_title(source)
    template = template.replace("{{ Title }}", title)
    final = template.replace("{{ Content }}", source_html)
    if not os.path.exists(os.path.dirname(dest_loc)):
        os.makedirs(os.path.dirname(dest_loc))
    final_file = open(dest_loc, "w")
    final_file.write(final)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = os.listdir(dir_path_content)
    
    for name in files:
        file = os.path.join(dir_path_content, name)
        if os.path.isfile(file):
            file_name = pathlib.PurePath(file).stem
            new_file = file_name + ".html"
            new_dest = os.path.join(dest_dir_path, new_file)
            generate_page(file, template_path, new_dest)
        else:
            destination = os.path.join(dest_dir_path, name)
            generate_pages_recursive(file, template_path, destination)
