# -*- encoding: utf-8 -*-
"""
@File    : __init__.py
@Time    : 2020/7/20 11:41
@Author  : blockish
@Email   : blockish@yeah.net
"""
__all__ = {
    'Instrument',
}

import traceback
import warnings
from abc import abstractmethod, ABC

from base import Object
from constants import ON, OFF


class Ieee488:

    def cal(self):
        """
        校准命令(IEEE488标准)
        :return: None
        """
        warnings.warn('%s can\'t supported "cal" command', self.__class__)

    def cls(self):
        """
        清除状态寄存器
        :return: None
        """
        warnings.warn('%s can\'t supported "cls" command', self.__class__)

    def ese(self, nrf: int = None):
        """
        设置和读取标准事件状态使能(Standard Event Status Enable)寄存器
        :param nrf: 事件状态使能(Standard Event Status Enable)寄存器号, IEEE488规定位0-255, 具体参考当前仪器说明
        :return: 事件状态使能(Standard Event Status Enable)寄存器
        """
        warnings.warn('%s can\'t supported "ese" command', self.__class__)

    def esr(self):
        """
        查询读取标准状态寄存器并清除它
        :return: 标准状态寄存器内容
        """
        warnings.warn('%s can\'t supported "esr" command', self.__class__)

    def idn(self):
        """
        获取仪器型号序列号等信息
        :return: 仪器型号序列号等信息
        """
        warnings.warn('%s can\'t supported "idn" command', self.__class__)

    def opc(self, query: bool = False):
        """
        当query为False时, 写入OPC命令, 此命令不影响其他命令, 只是当所有命令完成后, 在标准状态寄存器第0位置1, 此时返回None
        当query为True时, 当所有命令执行完成后才响应返回1
        :param query: 参见功能说明
        :return: 参见功能说明
        """
        warnings.warn('%s can\'t supported "opc" command', self.__class__)

    def opt(self):
        """
        查询当前(批)命令执行结果状态,  中间以分号(;)分割
        :return: 参见功能说明
        """
        warnings.warn('%s can\'t supported "opt" command', self.__class__)

    def psc(self, on_off: str = None):
        """
        该命令用来控制当负载重上电时是否会产生一个服务请求.
        1 or ON: 当负载上电时, 状态位元组使能寄存器, 操作事件使能寄存器, 查
        询事件使能寄存器及标准事件使能寄存器的值被清零.
        0 or OFF: 状态位元组使能寄存器, 操作事件使能寄存器, 查询事件使能寄存
        器及标准事件使能寄存器的值被储存在非易失性存储器中, 供重上电时取出使用
        None: 只返回当前psc状态
        :param on_off: 可选值 {ON|1|OFF|0}
        :return: 当前psc状态0或1
        """
        warnings.warn('%s can\'t supported "psc" command', self.__class__)

    def rcl(self, nrf: int = 1):
        """
        该命令调用用sav命令储存的状态
        :param nrf: 数字范围参考仪器手册
        :return: None
        """
        warnings.warn('%s can\'t supported "rcl" command', self.__class__)

    def rst(self):
        """
        出厂设置
        :return: None
        """
        warnings.warn('%s can\'t supported "rst" command', self.__class__)

    def sav(self, nrf: int = 1):
        """
        保持设置到指定存储位置, 以供rcl调用
        :param nrf: 数字范围参考仪器手册
        :return: None
        """
        warnings.warn('%s can\'t supported "sav" command', self.__class__)

    def sre(self, nrf: int = None):
        """
        查询设定服务请求使能寄存器
        :param nrf: 数字范围参考仪器手册
        :return: 服务请求使能寄存器状态
        """
        warnings.warn('%s can\'t supported "sre" command', self.__class__)

    def stb(self):
        """
        查询状态寄存器值
        :return: 状态寄存器值
        """
        warnings.warn('%s can\'t supported "stb" command', self.__class__)

    def trg(self):
        """
        发送一个触发信号, 触发信号内容根据仪器而定
        :return: None
        """
        warnings.warn('%s can\'t supported "trg" command', self.__class__)

    def tst(self):
        """
        自检测试
        :return: 自检测试状态, 非0为不通过, 具体查看仪器定义
        """
        warnings.warn('%s can\'t supported "tst" command', self.__class__)

    def wai(self):
        """
        发送等待命令, 直到命令完成, 否则不接受任何指令
        :return: None
        """
        warnings.warn('%s can\'t supported "wai" command', self.__class__)


class Instrument(Object, Ieee488, ABC):

    def __init__(self, resource_name, timeout, **kwargs):
        super().__init__(**kwargs)
        self._resource_name = None
        self._info = None
        self._instrument = self.open(resource_name)
        self._instrument._timeout = timeout

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, err_type, err_val, err_tb):
        self.finalize()
        if err_type is not None:
            self._logger.error('Error exit:')
            self._logger.error('\terror type: %s, error value: %s, error trace back: %s', err_type, err_val, err_tb)

    def __str__(self):
        return '<IDN: {} at {}>'.format(self._info, self._resource_name)

    @property
    def resource_name(self):
        return self._resource_name

    @property
    def info(self):
        return self._info

    # @abstractmethod
    def initialize(self):
        self.remote(ON)
        self._info = self.idn()

    def finalize(self):
        self.remote(OFF)
        self.close()

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, cmd, *args, **kwargs):
        pass

    @abstractmethod
    def query(self, cmd, *args, **kwargs):
        pass

    # @abstractmethod
    def remote(self, on_off):
        warnings.warn('%s can\'t support "remote" method' % self.__class__)

    @abstractmethod
    def open(self, resource_name: str = None, reopen: bool = False):
        pass

    def close(self):
        """关闭仪器资源
        """
        if self._instrument is not None:
            try:
                self._instrument.close()
                self._instrument = None
                self._resource_name = None
            except IOError as e:
                self._logger.error(traceback.format_exc())


