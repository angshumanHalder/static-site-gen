from block_md import markdown_to_html_node
import os


def extract_title(markdown):
    blocks = markdown.split("\n")
    for block in blocks:
        if block.startswith("# "):
            return block.strip("#").strip()

    raise ValueError("no title on markdown file")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    with open(dest_path, "w") as file:
        file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(
        f"Generating all pages from {dir_path_content} to {dest_dir_path} using {template_path}"
    )
    dir_paths = os.listdir(dir_path_content)
    for dir in dir_paths:
        dir_path = os.path.join(dir_path_content, dir)
        if os.path.isdir(dir_path):
            dst_path = os.path.join(dest_dir_path, dir)
            os.mkdir(dst_path)
            generate_pages_recursive(dir_path, template_path, dst_path)
        else:
            file_name = dir.split(".")[0]
            dst_path = os.path.join(dest_dir_path, f"{file_name}.html")
            generate_page(dir_path, template_path, dst_path)
