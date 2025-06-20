"""
用于做文件相关的处理，如删除、移动等
"""

import json
import os
import shutil


def load_file(file_path, is_json=False, encoding="utf-8"):
    """
    加载文件内容
    :param file_path: 文件路径
    :param is_json: 是否为 JSON 格式文件
    :param encoding: 编码
    """
    with open(file_path, "r", encoding=encoding) as file:
        if is_json:
            return json.load(file)  # json.loads(file.read()) json 数据
        else:
            return file.read()  # 文本数据


def write_file(content, file_path, is_json=False):
    """
    写入文件
    :param content: 文件内容
    :param file_path: 文件路径
    :param is_json: 是否为 JSON 格式文件
    """
    with open(file_path, "w", encoding="utf-8") as file:
        if is_json:
            json.dump(content, file, indent=2, ensure_ascii=False)
        else:
            file.write(content)


def copy_tree(src, dst):
    """
    拷贝文件目录到指定的位置
    :param src: 目标源
    :param dst: 指定位置
    """
    if not os.path.exists(src) or not os.path.isdir(src):
        return
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def remove_trees(trees):
    """
    移除指定的目录，可以为多个
    :param trees: 目录路径
    """
    if len(trees) == 0:
        return
    for folder_path in trees:
        if not os.path.exists(folder_path):
            continue
        shutil.rmtree(folder_path)
