from copystatic import copy_contents_from_src_dst
from gen_page import generate_pages_recursive
import os

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    copy_contents_from_src_dst(dir_path_static, dir_path_public)
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
    )


main()
