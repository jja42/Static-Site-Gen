from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)
    html_node = HTMLNode("h1", "Text goes here")
    print(html_node)

if __name__ == "__main__":
    main()
