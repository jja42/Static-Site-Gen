from textnode import TextNode, TextType
from htmlnode import HTMLNode
import shutil
import os

def main():
    copy_static()

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


if __name__ == "__main__":
    main()
