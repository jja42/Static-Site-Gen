import shutil
import os
import re
from markdown import markdown_to_html_node
from htmlnode import HTMLNode

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    from_path = os.path.join(base_dir,"content/index.md")
    template_path = os.path.join(base_dir,"template.html")
    dest_path = os.path.join(base_dir,"public/index.html")
    generate_page(from_path,template_path,dest_path)
    #copy_static()

def copy_static():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    static_path = os.path.join(base_dir, "static")
    public_path = os.path.join(base_dir, "public")

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
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path)
    markdown = file.read()
    file = open(template_path)
    template = file.read()
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}",title)
    template = template.replace("{{ Content }}", html)
    file = open(dest_path, "w")
    file.write(template)


if __name__ == "__main__":
    main()
