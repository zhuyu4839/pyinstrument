# -*- encoding: utf-8 -*-
"""
@File    : logger.py
@Time    : 2020/7/20 9:50
@Author  : blockish
@Email   : blockish@yeah.net
"""
import os
import time

import colorlog
import logging
import sys
from logging import DEBUG, INFO, WARN, ERROR


LEVEL = {DEBUG: sys.stdout, INFO: sys.stdout, WARN: sys.stderr, ERROR: sys.stderr}
DEFAULT_FMT = '%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s'
COLOR_LOG_FMT = '%(log_color)s{}'
DEFAULT_FILE = 'log {}.log'.format(time.strftime('%Y-%m-%d', time.localtime()))
ROOT_LEVEL = DEBUG
CONSOLE_LEVEL = INFO
FILE_LEVEL = WARN


def __console_log(log, level, fmt):
    target = LEVEL.get(level, sys.stdout)
    handler = logging.StreamHandler(target)
    handler.setLevel(CONSOLE_LEVEL if level is None else level)
    handler.setFormatter(colorlog.ColoredFormatter(COLOR_LOG_FMT.format(DEFAULT_FMT))
                         if fmt is None else COLOR_LOG_FMT.format(fmt))
    log.addHandler(handler)
    return log


def __file_log(log, level, fmt, filename):
    file = os.path.join(os.getcwd(), DEFAULT_FILE if filename is None else filename)
    handler = logging.FileHandler(file, encoding='utf-8')
    handler.setLevel(FILE_LEVEL if level is None else WARN)
    handler.setFormatter(logging.Formatter(DEFAULT_FMT) if fmt is None else fmt)
    log.addHandler(handler)
    return log


def get_logger(name: str,
               fmt: str = None,
               console_level: int = None,
               file_level: int = None,
               filename: str = None,
               develop: bool = True):
    """
    获取日志对象, 包含日志文件记录和控制台日志打印
    :param name: 日志对象名称
    :param fmt: 日志格式, 同时指定控制台和文件记录格式
    :param console_level: 控制台日志LEVEL, 默认为INFO
    :param file_level: 文件日志LEVEL, 默认为WARN
    :param filename: 日志文件名, 默认为当前运行文件目录下 "log 年-月-日.log"
    :param develop: 是否是开发模式
    :return: 日志对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(ROOT_LEVEL)
    if not logger.handlers:
        if develop is True:
            __console_log(logger, console_level, fmt)
        __file_log(logger, file_level, fmt, filename)
    return logger


if __name__ == '__main__':
    lg = get_logger("test")
    lg.debug('debug')
    lg.info('info')
    lg.warning('warning')
    lg.error('error')
    lg.critical('critical')

