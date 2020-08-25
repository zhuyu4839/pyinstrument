# -*- encoding: utf-8 -*-
"""
@File    : errors.py
@Time    : 2020/7/20 9:53
@Author  : blockish
@Email   : blockish@yeah.net
"""


class InstrumentException(Exception):
    """InstrumentException"""
    pass


class ParamException(Exception):
    """
    传入参数异常
    """
    pass


class ResourceException(Exception):
    """
    资源异常
    """
    pass


InstrumentError = InstrumentException
ParamError = ParamException
ResourceError = ParamException
