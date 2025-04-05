import os
import shutil


def copy_contents_from_src_dst(src, dst):
    if not os.path.exists(src):
        raise FileNotFoundError("No folder exists at the location specified")
    if not os.path.exists(dst):
        os.mkdir(dst)
    elif os.path.exists(dst):
        shutil.rmtree(dst)
        os.mkdir(dst)

    copy(src, dst)


def copy(src, dst):
    src_dirs = os.listdir(src)
    for dir in src_dirs:
        src_path = os.path.join(src, dir)
        if os.path.isdir(src_path):
            dst_path = os.path.join(dst, dir)
            os.mkdir(dst_path)
            copy(src_path, dst_path)
        else:
            dst_path = os.path.join(dst, dir)
            shutil.copy(src_path, dst_path)
