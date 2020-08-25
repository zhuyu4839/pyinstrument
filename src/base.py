# -*- encoding: utf-8 -*-
"""
@File    : base.py
@Time    : 2020/7/20 11:38
@Author  : blockish
@Email   : blockish@yeah.net
"""

from logger import get_logger


class Object(object):
    """
    Object对象, 包含日志属性_logger
    """
    def __init__(self, **kwargs):
        self._logger = get_logger(self.__class__.__name__)
        self.__kwargs__(**kwargs)

    def __kwargs__(self, **kwargs):
        pass
