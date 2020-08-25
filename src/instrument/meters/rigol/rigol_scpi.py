# -*- encoding: utf-8 -*-
"""
@File    : rigol_scpi.py
@Time    : 2020/7/31 12:02
@Author  : blockish
@Email   : blockish@yeah.net
"""
__all__ = {
    'MD3058',
}

from instrument.scpi import ScpiInstrument


class MD3058(ScpiInstrument):
    """
    For supporting RIGOL power meter, model MD3058.
    Used RIGOL command set by default, and not supported AGILENT command set
    """
    pass

