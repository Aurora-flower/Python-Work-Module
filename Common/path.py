"""
用于做路径相关的处理，如删除、移动等
"""
import os
from pathlib import Path

suffix = {
    "json": [".json", ".prefab", ".fire"],
    "js": ".js"
}


def get_path_ext(file_path):
    """
    获取文件路径的后缀
    :param file_path: 文件路径
    :return: 文件路径后缀名
    """
    # os.path.splitext(file_path)
    return Path(file_path).suffix


def replace_path_sep(path):
    """
    替换路径拼接符为统一格式的处理
    :param path: 需要处理的路径
    :return: 处理拼接符
    """
    sep = os.sep  # 文件分隔符
    sep_set = {
        "win": "\\",
        "mac": "/",
    }
    win_sep = sep_set.get("win")
    mac_sep = sep_set.get("mac")
    if sep == win_sep:
        path = path.replace(mac_sep, sep)
    elif sep == mac_sep:
        path = (path.replace(win_sep, sep).replace("//", mac_sep)
                # 为 mac 路径做的处理
                .replace(" ", f"{win_sep} "))
    return path


def join_path(*paths):
    """
    拼接路径，并做替换路径拼接符的处理
    :param paths: 需要拼接的路径
    :return: 拼接完成的路径

    备注:
    `normpath` - 规范化路径，去除多余的路径分隔符和解析相对路径
    """
    joined_path = os.path.join("", *paths)
    pending_path = os.path.normpath(joined_path)
    return replace_path_sep(pending_path)
