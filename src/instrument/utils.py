# -*- encoding: utf-8 -*-
import re
import time

from errors import ParamException
from instrument.const import SEMICOLON

BIG_ENDIAN = 'big'
LITTLE_ENDIAN = 'little'


def dict_add(d1, *others):
    """
    字典拼接(深度拷贝)
    :param d1: (type dict) 源字典
    :param others: (type tuple of dict) 其他的字典tuple
    :return: (type dict) 拼接后的字典
    """
    result = d1.copy()
    for other in others:
        result.update(other)
    return result


def value_to_hex(value, endian=LITTLE_ENDIAN, size=4, magnif=1000):
    """
    把一个数字转换为8位的二进制list, 如 [0xff, 0xff]
    :param value: (type int) 需要转换的数字
    :param endian: (type str) 大端小端选择, 可选值{big|little}
    :param size: (type int) 转换后的二进制list的大小
    :param magnif: (type int) 对数字value的数乘
    :return: (type list) 转换后的二进制list
    """
    value = int(value * magnif)
    hex_list = [value >> (8 * i) & 0xff for i in range(size)]
    __check_endian(hex_list, endian)
    return hex_list


def hex_to_value(data, endian=LITTLE_ENDIAN, magnif=1000):
    """
    把二进制list还原对应为数值
    :param data: (type list) 需要转换的二进制数据
    :param endian: (type str) 大端小端选择, 可选值{big|little}
    :param magnif: (type int) 转换后的数字数乘
    :return: (type float) 转换后的数值
    """
    __check_endian(data, endian)
    count = 0
    for i in range(len(data)):
        count += (data[i] << (i * 8))
    return count / magnif


def hex_list_to_str(data):
    """
    把ascii码list转换为对应的字符, 不能转换的ASCII码不转换
    :param data: (type list) 需要转换的二进制数据
    :return: (type list) 转换后的结果
    """
    pattern = re.compile('\'(.*)\'')
    data = str(bytearray(data))
    return pattern.findall(data)


def noneable(param):
    """
    用于判断非None参数, 如果参数为None, 则抛出异常
    :param param: 需要判断的参数
    :return: None
    """
    assert param is not None, 'None parameter error'


def get_regex(rex, flags):
    """
    获取正则对象
    :param rex: 正则表达式
    :param flags: 正则表达式flags
    :return: 正则对象
    """
    return re.compile(rex, flags)


def raiser(e):
    """
    抛出异常
    :param e: 需要抛出的异常
    :return: None
    """
    raise e


def contact_spci_cmd(cmd1, cmd2, *args, **kwargs):
    if cmd2 is None:
        return cmd1
    if cmd1 is None:
        return cmd2.format(*args, **kwargs)
    cmd1 += SEMICOLON + cmd2.format(*args, **kwargs)
    return cmd1


def set_query(obj, set_dict, get_dict, *names, **values):
    """
    set and query
    """
    write_cmd = None
    for key, value in values.items():
        # if len(names) == 0:
        #     query_cmd = contact_spci_cmd(query_cmd, get_dict.get(key))
        write_cmd = contact_spci_cmd(write_cmd, set_dict.get(key), value)

    obj.write(write_cmd)
    time.sleep(0.1)

    query_cmd = None
    for name in names:
        query_cmd = contact_spci_cmd(query_cmd, get_dict.get(name))
    return obj.query(query_cmd)


def __check_endian(data, endian):
    if endian == BIG_ENDIAN:
        data.reverse()
    elif endian == LITTLE_ENDIAN:
        pass
    else:
        raise ParamException('The endian expect value "%s" or "%s" not "%s"' % (BIG_ENDIAN, LITTLE_ENDIAN, endian))
