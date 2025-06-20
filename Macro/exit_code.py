from enum import Enum


class ExitCode(Enum):
    """
    退出码定义，用于表示不同的退出状态。
    """

    NULL = -1
    NORMAL = 0
    MISSING_PARAMETER = 100
    NOT_FOUND = 101
    INVALID = 102
    LIMITED_CONDITION = 104
