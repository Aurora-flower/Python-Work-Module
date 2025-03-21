"""
辅助处理
"""
import time
import datetime


class SwitchCase:
    key = "default"  # 默认值
    params = ()

    def __init__(self, *params):
        self.params = params[1:]
        self.key = params[0] or "default"


def switch(*arg, key=""):
    switcher = SwitchCase(key, *arg)
    method = getattr(switcher, key, lambda: "无效方法")
    return method()


def get_dict(d, key, default=None):
    """
    获取字典中的值，如果 key 不存在，返回 default 值
    """
    try:
        return d[key]
    except (KeyError, TypeError):
        return default


def get_time(time_stamp, format_template="%Y-%m-%d %H:%M:%S"):
    # 将时间戳转换为日期时间
    dt = datetime.datetime.fromtimestamp(time_stamp)
    return dt.strftime(format_template)


def replace_in_range(s, start_index, tail_index, new_str):
    """
    替换字符串中指定范围的字符，其中尾部下标包含在内。
    :param s: 原始字符串
    :param start_index: 起始下标位置
    :param tail_index: 尾部下标位置（包含）
    :param new_str: 用于替换的字符串
    :return: 替换后的字符串
    """
    # 检查索引是否有效
    if start_index < 0 or tail_index >= len(s) or start_index > tail_index:
        raise ValueError("Invalid start or tail index.")

    # 将字符串分成三部分：前半部分、替换部分、后半部分
    new_s = s[:start_index] + new_str + s[tail_index + 1:]
    return new_s


if __name__ == '__main__':
    imag = get_time(time.time().imag)
    # now = get_time()
    print(time.localtime().tm_zone, imag, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
