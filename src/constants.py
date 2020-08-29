# -*- encoding: utf-8 -*-
"""
@File    : constants.py
@Time    : 2020/7/31 12:06
@Author  : blockish
@Email   : blockish@yeah.net
"""

ON = 'ON'
OFF = 'OFF'
ONE = '1'
ZERO = '0'

RUN = 'run'
STOP = 'stop'

TUPLE_ON = (ON, ONE)
TUPLE_OFF = (OFF, ZERO)
TUPLE_ON_OFF = (*TUPLE_ON, * TUPLE_OFF)


if __name__ == '__main__':
    print(TUPLE_ON_OFF)
    print(int('1\n'))

