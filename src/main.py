import shutil
import os
import re
from markdown import markdown_to_html_node

def main():
    dir_path_static = "./static"
    dir_path_public = "./public"
    dir_path_content = "./content"
    template_path = "template.html"
    copy_static(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


def copy_static(static_path, public_path):

    #print("Static path:", static_path)
    #print("Public path:", public_path)

    if(os.path.exists(public_path)):
        shutil.rmtree(public_path)

    os.mkdir(public_path)

    files_to_copy = []
    files_to_copy = copy_static_recursive(static_path)

    for file in files_to_copy:
        file_dir = os.path.relpath(file, static_path)
        copy_path = os.path.join(public_path,file_dir)
        copy_dir = os.path.dirname(copy_path)
        os.makedirs(copy_dir, exist_ok=True)
        shutil.copy(file,copy_path)
        print(f"{file} copied to {copy_path}")


def copy_static_recursive(current_path):
    directory_contents = os.listdir(current_path)
    content_list = []
    for content in directory_contents:
        path = os.path.join(current_path,content)
        #print(path)
        if(os.path.isfile(path)):
            content_list.append(path)
        elif(os.path.isdir(path)):
            content_list.extend(copy_static_recursive(path))
    return content_list

def extract_title(markdown):
    match = re.search(r'^#\s(.*)', markdown)
    if(match):
        title = match.group(1)
        return title
    else:
        raise Exception("Missing Title")
    
def generate_page(from_path, template_path, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}",title)
    template = template.replace("{{ Content }}", html)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    directory_contents = os.listdir(dir_path_content)
    for content in directory_contents:
        path = os.path.join(dir_path_content,content)
        dest_path = os.path.join(dest_dir_path,content)
        if(os.path.isfile(path)):
            if(content.endswith(".md")):
                dest_path = dest_path.replace(".md",".html")
                generate_page(path,template_path,dest_path)
        if(os.path.isdir(path)):
            generate_pages_recursive(path,template_path,dest_path)


if __name__ == "__main__":
    main()
