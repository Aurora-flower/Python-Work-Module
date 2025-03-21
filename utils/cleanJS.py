# !python
# -*- coding: utf-8 -*
"""
此脚本用于处理文件中函数的内容。

注意📢: 这里更多是针对 Cocos 引擎代码做的处理，如果需要通用，那么则需要细分逻辑。

后续可扩展功能:剔除指定后缀文件中的任意内容。

"""
import re
import os
import sys
import time
from enum import Enum

# Custom package
import Common

# 当前工作目录
cwd = os.getcwd()

# 接受的参数 - 项目路径，处理的目录名称
args = sys.argv[1:]

"""
API:

----
re.subn: 返回一个元组 (new_string, number_of_subs),
其中 new_string 是替换后的字符串, number_of_subs 是实际发生替换的次数。

----
re.MULTILINE
re.MULTILINE 标志使得正则表达式中的开始锚点 ^ 和结束锚点 $ 能够匹配每一行的开始和结束，而不仅仅是整个字符串的开始和结束。
这对于处理多行文本非常有用，因为它允许在每一行的开头和结尾进行匹配。

re.DOTALL
re.DOTALL 标志使得正则表达式中的点 . 能够匹配任何字符，包括换行符。
默认情况下，点 . 不匹配换行符。
当需要匹配包括换行符在内的所有字符时，这个标志非常有用。

----
re.IGNORECASE (re.I): 使匹配对大小写不敏感。
re.LOCALE (re.L): 做本地化识别 (locale-aware) 匹配。
re.MULTILINE (re.M): 多行匹配，影响 ^ 和 $ 锚点的行为，使其可以在每行的开始和结束匹配。
re.DOTALL (re.S): 使 . 匹配包括换行符在内的所有字符。
re.UNICODE (re.U): 根据 Unicode 字符集解析字符类，如 w, b 等。
re.VERBOSE (re.X): 允许正则表达式使用空白和注释，方便阅读和调试。

"""


def default_func(*params):
    print(*params, len(params))


class ExitCode(Enum):
    SUCCESS = 0
    FAIL = 1


def replace_character_string(content):
    """
    使用占位符替换处理 JS 文本中的字符串
    :param content: 文本内容
    :return: 处理完之后的文本
    """
    # r"(?<![\'\"`])([\'\"][^\'\"]*?[\'\"]|`[^`]*?`)(?!=[\'\"`])"
    string_pattern = re.compile(r"(?<![\'\"`])'.*?'|\".*?\"|`.*?`(?!=[\'\"`])", re.DOTALL)

    def replace_string(match):
        m = match.group()
        if len(m) > 2:
            return '*' * len(m)
        return m

    return re.sub(string_pattern, lambda x: replace_string(x), content)


def find_body_end(content, start_index=0, start_char="{", end_char="}"):
    """
    根据 '{' 或 '}' 获取获取函数体结束的位置，查找不到返回 -1。
    扩展为获取闭合内容结束位置。
    :param content: 文本内容
    :param start_index: 开始下标
    :param start_char: 开始符号
    :param end_char: 结束符号
    :return: 结束位置下标
    """
    deep = 0
    for i, char in enumerate(content[start_index:], start=start_index):
        if i == start_index and content[start_index] != start_char:
            continue
        if char == start_char:
            deep += 1
        elif char == end_char:
            deep -= 1
        if deep == 0:
            # if i == 0:
            #     print('find_body_end:', len(content), '\n' + '*'*50)
            return i
    len_start_body = len(re.findall(r'{', content, re.DOTALL))
    len_end_body = len(re.findall(r'}', content, re.DOTALL))
    print('compare:', len_start_body, len_end_body)
    return -1


def replace_reg_exp(content):
    reg_pattern = re.compile(r'/[^/\n]*?/[gimsuy]*', re.DOTALL)
    print('replace_reg_exp:', reg_pattern.findall(content))
    return content


def extract_content(content, pattern, start_char="{", end_char="}"):
    m_list = []
    positions = []
    replace_string_content = replace_character_string(content)
    # replace_reg_content = replace_reg_exp(replace_string_content)
    # ms = re.finditer(patterns, replace_reg_content)
    # ms = patterns.finditer(replace_string_content)
    ms = pattern.finditer(replace_string_content)
    for m in ms:
        m_list.append(m.group())
        # print('-' * 10, m.group())
        cb_start_index = m.start()
        body_cb_start_index = m.end()
        body_cb_end_index = -1
        positions.append([cb_start_index, body_cb_start_index, body_cb_end_index])

    for index, position in enumerate(positions, start=0):
        next_index = index + 1
        expect_length = next_index + 1
        is_exits_next = len(positions) >= expect_length
        if is_exits_next:
            # 当前到下一个匹配的位置组合
            slice_index = slice(index, expect_length)
            position_el = positions[slice_index]
            current_match_end = position_el[0][1]
            # next_match_start = position_el[-1][0]
            next_match_end = position_el[-1][0]
            position_range = [current_match_end, next_match_end]
        else:
            # position_range = [positions[-1][1], -1]
            position_range = [positions[-1][1], len(content)]
        slice_range = slice(*position_range)
        slice_content = content[slice_range]
        # replace_reg_exp(slice_content)
        rel_char_text = replace_character_string(slice_content)
        brace_index = find_body_end(rel_char_text, 0, start_char, end_char)
        if brace_index == -1:
            print('>' * 50, 'Warning:',
                  pattern,
                  '\n',
                  rel_char_text,
                  len(content) - 1,
                  index,
                  '\n',
                  f">>> {m_list[index]} <<<",
                  '\n',
                  slice_range
            )
            # continue
            break
        positions[index][2] = positions[index][1] + brace_index

        real_end_index = brace_index + 1
        start_rel_content = slice_content[:real_end_index]
        end_rel_content = slice_content[real_end_index:]
        insert_text = start_char + '$' * (len(start_rel_content) - 2) + end_char
        insert_content = insert_text + end_rel_content
        start, end = position_range
        text = content[:start] + insert_content
        if end != -1:
            text = text + content[end:]
        else:
            text = text + content[end]
        content = text

    def replace_placeholder():
        return ''

    placeholder_pattern = re.compile(r"\${2,}", re.MULTILINE)
    sub_content = re.sub(placeholder_pattern, lambda x: replace_placeholder(), content)
    return sub_content


def clean_property_func(content):
    """
    处理文件 - 删除函数体中的内容

    备注:
    格式 - `xxx.prototype.xxx = function(xxx) {xxxx}`
    """
    property_func_pattern = re.compile(
        r"^\w+\.\bprototype\b\.\w+\s*?=\s*?\bfunction\b\s*?\(.*?\)\s*?(?={)",
        re.MULTILINE
    )
    # print('clean_property_func:', property_func_pattern.findall(content))
    return extract_content(content, property_func_pattern)


def clean_vanilla_iife(content):
    # vanilla_iife_pattern = re.compile(
    #     r'\(\s*?function\s*?\(.*?\)\s*?\{.*?}\s*\)', re.DOTALL)
    return content


def clean_vanilla_callback(content):
    """
    处理文件 - 删除函数体中的内容

    备注:
    格式 - `function (xxx) {xxxx}`
    """
    vanilla_callback_pattern = re.compile(r"\bfunction\b\s*?\(.*?\)\s*?(?={)", re.MULTILINE)
    # print('clean_vanilla_callback:', vanilla_callback_pattern.findall(content))
    return extract_content(content, vanilla_callback_pattern)


def clean_vanilla_func(content):
    """
    处理文件 - 删除函数体中的内容

    备注:
    格式 - `function xxx(xxx) {xxxx}`
    """
    vanilla_func_pattern = re.compile(r"\bfunction\b\s*?\w+\s*?\(.*?\)\s*?(?={)", re.MULTILINE)
    # print('clean_vanilla_func:', vanilla_func_pattern.findall(content))
    return extract_content(content, vanilla_func_pattern)


def clean_vanilla_literal(name, content):
    """
    处理文件 - 删除字面量内容
    :param name:
    :param content:
    :return:
    """
    literal = name and rf'\b{name}\b' or r'\w+'
    literal_pattern = re.compile(rf"{literal}\.\w+\s*?=\s*?" + r"(?={)", re.MULTILINE)
    # print('clean_vanilla_literal:', literal_pattern.findall(content))
    return extract_content(content, literal_pattern)


def clean_property_literal(content):
    property_literal_pattern = re.compile(rf"\bproperties\b\s*?:\s*?" + r"(?={)", re.MULTILINE)
    # print('clean_property_literal:', property_literal_pattern.findall(content))
    return extract_content(content, property_literal_pattern)


def remove_multi_blank_row(content):
    multi_newline_pattern = re.compile(r"\n{3,}")
    return re.sub(multi_newline_pattern, "\n", content)


def remove_comments(content):
    single_comment = re.compile(r"\s+//[^\n]*", re.MULTILINE)
    multi_comment = re.compile(r"/\*.*?\*/", re.DOTALL)
    comment_patterns = (
        # 多行注释
        (multi_comment, False),

        # 单行注释
        (single_comment, True)
    )
    for pattern, mode in comment_patterns:
        # if mode:
        content = re.sub(pattern, "", content)
    return content


def remove_unused_declaration(content):
    return content


def remove_unused_import(content):
    quotes_pattern = re.compile((
        r"\b(?:var|let|const)\b\s*([^\s=]+)\s*=\s*\brequire\b\s*\((?:'[^']*'|\"[^\"]*\")\);?\n?"
    ))

    def replace_quotes(match):
        m = match.group()
        import_module = match.group(1)
        temp_content = content.replace(m, '')
        ms_len = len(re.findall(import_module, temp_content))
        if ms_len:
            return m
        else:
            return ''

    return re.sub(quotes_pattern, lambda x: replace_quotes(x), content)


def parser(file_path):
    """
    解析并处理 JS 文件内容
    :param file_path: 文件路径
    """
    file_name = os.path.basename(file_path)
    name = os.path.splitext(file_name)[0]
    print('parser...', name)
    # rvi_content = clean_vanilla_iife(rpf_content)

    raw_content = Common.load_file(file_path)
    rc_content = remove_comments(raw_content)
    rpf_content = clean_property_func(rc_content)
    rvf_content = clean_vanilla_func(rpf_content)
    rvc_content = clean_vanilla_callback(rvf_content)
    rvl_content = clean_vanilla_literal(name, rvc_content)
    rpl_content = clean_property_literal(rvl_content)
    rui_content = remove_unused_import(rpl_content)
    rbr_content = remove_multi_blank_row(rui_content)
    content = remove_unused_import(rbr_content)

    # Common.write_file(content, file_path)
    Common.write_file(content, file_name)


def clean_func_cite(project_folder, block_list=None, disabled_list=None, match_list=None, handle=default_func):
    """
    主函数，清理 JS 文件中的函数体内容，以及无用的引用。
    """
    count = 0

    for top, dirs, nondirs in os.walk(project_folder):
        if not len(nondirs) > 0:
            continue
        # for folder in dirs:
        #     full_path = os.path.join(top, folder)
        for file in nondirs:
            if file in disabled_list or file == '.DS_Store':
                continue
            folder_path = os.path.dirname(top)
            if block_list and len(block_list) > 0 and any(block in folder_path for block in block_list):
                break
            ext = Common.get_path_ext(file)
            if ext != Common.get_dict(Common.suffix, "js"):
                continue
            full_path = os.path.join(top, file)
            if file in match_list:
                handle(full_path)
                continue
            # 测试
            # if file in test_list:
            parser(full_path)

            count += 1

    # print("cleanJS:", cwd, args, project_folder, count)


if __name__ == "__main__":
    time_stamp_start = time.strftime("%Y-%m-%d %H:%M:%S")
    print("clean...", time_stamp_start)

    # ***** ***** ***** ***** 处理千年项目时的一些特殊定义 ***** ***** ***** *****
    config_file_name = "config.json"
    config_file = Common.join_path(cwd, config_file_name)
    if not os.path.exists(config_file):
        print(config_file)
        exit(ExitCode.FAIL)
    config_data = Common.load_file(config_file, True)
    raw_project_path = Common.join_path(Common.get_dict(config_data, "mainProjectGitPath"))
    raw_path = Common.join_path(raw_project_path, "Qiannian")
    temp_project_path = Common.join_path(
        "/Users/HuaYing/Desktop/resources/Test",  # cwd
        "tempProject")
    temp_path = Common.join_path(temp_project_path, "Qn")
    # copy_tree(raw_path, temp_path)

    # 删除无需处理与上传的目录
    trees = ["library", "build", "temp"]
    for idx, tree in enumerate(trees):
        trees[idx] = Common.join_path(raw_path, tree)
    Common.remove_trees(trees)

    # 文件重置处理 (置空)
    def reset_content(*params):
        if len(params) < 1:
            return
        file_path = params[0]
        file_name = os.path.basename(file_path)
        base, _ext = os.path.splitext(file_name)
        default_content = f"var {base} = {'{}'}; \nmodule.exports = {base};"
        Common.write_file(default_content, file_path)


    # 开始处理
    # script_folder = "/Users/HuaYing/Desktop/resources/Test/tempProject/Qn/assets/Script"
    script_folder = Common.join_path(temp_path, "assets/Script")

    # 报错测试列表
    test_list = [
        # 无法正确解析
        # 'protobuf.js',

        # 未清理干净
        # 'QNGoldEggEntrance.js',
        # 'QNRedPointSystem.js',

        # 存在引用需要替换 QNGlobal.xxx.xxx.xxx [^,\]\)]
        # 'QNAuctionPutUpView.js',
        # "QNAuctionSellModule.js",

        # 清理报错
        # 'QNSeasonRewardItem.js',

        # 部分格式处理错误
        # "xml-js.js",

        # 其他
        # 'LuaCommandUIView.js',
        # 'QNSelectPopItemView.js',
        # 'QNFlagBattleRankCell.js',
        # 'QNHandleUI.js',
        # 'QNEquipmentSkillExtractView.js',
        # 'QNMarriageView.js',
        # 'QNSkillRepracticeView.js',
        # 'QNEquipmentCultivateView.js',
        # 'QNArmoireDisplayRole.js'
        # 'QNEquipmentPropTransferView.js',
        # 'QNEquipmentSkillChangeView.js',
    ]
    block_folders = (
        '/.git/',
        "/library/",
        "/local/",
        "/packages/",
        "/settings/",
        "/temp/",
    )  # 黑名单 - 目录
    block_files = [
        'protobuf.js',  # 无法正确解析
        'xml-js.js',  # 无法正确解析
    ]  # 黑名单 - 文件
    match_files = ("QNGlobal.js", "QNNetEvent.js", "QNMessageConfig.js", "LuaGameExtend.js")  # 文件匹配，特殊处理 (置空)
    clean_func_cite(script_folder, block_folders, block_files, match_files, reset_content)

    # 成功打印
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print("clean success!", time_stamp)
