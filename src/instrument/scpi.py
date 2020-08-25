# -*- encoding: utf-8 -*-
"""
@File    : scpi.py
@Time    : 2020/7/20 17:10
@Author  : blockish
@Email   : blockish@yeah.net
"""
from abc import ABC
from instrument import Instrument
from pyvisa.highlevel import ResourceManager

from instrument.const import Ieee488Const, SPACE, INTERROGATION, EMPTY
from errors import InstrumentException


class ScpiInstrument(Instrument, ABC):

    _rm = ResourceManager()

    def __init__(self, resource_name, timeout, **kwargs):
        super().__init__(resource_name, timeout, **kwargs)

    @staticmethod
    def resources():
        """
        获取当前连接的所有VISA设备资源名称(注意会把所有连接的串口都以SCPI资源名称返回)
        :return: 所有VISA设备资源名称
        """
        return ScpiInstrument._rm.list_resources()

    @staticmethod
    def close_rm():
        """
        关闭visa的资源管理器, 意味着其不能再使用;
        在所有资源使用完毕之后, 可以优雅的关闭visa资源管理器
        :return: None
        """
        ScpiInstrument._rm.close()

    def open(self, resource_name: str = None, reopen: bool = False):
        """
        打开visa仪器资源
        :param resource_name: 需要打开的仪器资源信息, 如果__init__函数指定resource_name, 则在此必须指定, 否则抛出异常
        :param reopen: 是否重新打开, 由于visa仪器连接电脑时如果中间有断线现象则此时使用reopen为True
        :return: None
        """
        if resource_name is None:
            if self._resource_name is None:
                raise InstrumentException('can\'t open a none resource name')
            else:
                visa_obj = self._rm.open_resource(self._resource_name)
                return visa_obj
        else:
            if self._resource_name != resource_name:
                self.close()
                self.open(resource_name, False)
            else:
                if reopen is True:
                    resource_name = self._resource_name
                    self.close()
                    self.open(resource_name, False)
                else:
                    pass  # nothing to do

    def write(self, cmd, *args, **kwargs):
        """
        写入命令
        :param cmd: 命令内容
        :param args: 命令参数
        :param kwargs: 命令参数
        :return: None
        """
        if cmd is not None:
            cmd = cmd.format(*args, **kwargs)
            self._logger.info('Execute command: %s', cmd)
            res = self._instrument.write(cmd)
            self._logger.debug('write command info: %s', res)
            # return res

    def read(self):
        """
        读命令
        :return: 设备返回的信息
        """
        return self._instrument.read()

    def query(self, cmd, *args, **kwargs):
        """
        查询信息
        :param cmd: 命令内容
        :param args: 命令参数
        :param kwargs: 命令参数
        :return: 设备返回的信息
        """
        if cmd is not None:
            cmd = cmd.format(*args, **kwargs)
        return self._instrument.query(cmd)

    def initialize(self):
        """
        初始化仪器
        1. 清除状态寄存器
        2. 获取仪器IDN信息
        3. 自检测试
        :return: None
        """
        self.cls()
        self._info = self.idn()
        self._logger.info(self.__str__())
        check = self.tst()
        if '0\n' != check:
            self._logger.warning('self-checking response non zero, value: %d', check)

    def cal(self):
        """
        校准命令(IEEE488标准)
        :return: None
        """
        self.write(Ieee488Const.CAL)

    def cls(self):
        """
        清除状态寄存器
        :return: None
        """
        self.write(Ieee488Const.CLS)

    def ese(self, nrf: int = None):
        """
        设置和读取标准事件状态使能(Standard Event Status Enable)寄存器
        :param nrf: 事件状态使能(Standard Event Status Enable)寄存器号, IEEE488规定位0-255, 具体参考当前仪器说明
        :return: 事件状态使能(Standard Event Status Enable)寄存器
        """
        if nrf is not None:
            self.write(Ieee488Const.ESE, SPACE, nrf)
        return self.query(Ieee488Const.ESE, INTERROGATION, EMPTY)

    def esr(self):
        """
        查询读取标准状态寄存器并清除它
        :return: 标准状态寄存器内容
        """
        return self.query(Ieee488Const.ESR)

    def idn(self):
        """
        获取仪器型号序列号等信息
        :return: 仪器型号序列号等信息
        """
        return self.query(Ieee488Const.IDN)

    def opc(self, query: bool = False):
        """
        当query为False时, 写入OPC命令, 此命令不影响其他命令, 只是当所有命令完成后, 在标准状态寄存器第0位置1, 此时返回None
        当query为True时, 当所有命令执行完成后才响应返回1
        :param query: 参见功能说明
        :return: 参见功能说明
        """
        if query is True:
            return self.query(Ieee488Const.OPC, INTERROGATION)
        else:
            self.write(Ieee488Const.OPC, EMPTY)

    def opt(self):
        """
        查询当前(批)命令执行结果状态,  中间以分号(;)分割
        :return: 参见功能说明
        """
        return self.query(Ieee488Const.OPT)

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
        if on_off is not None:
            self.write(Ieee488Const.PSC, SPACE, on_off)
        return self.query(Ieee488Const, INTERROGATION, EMPTY)

    def rcl(self, nrf: int = 1):
        """
        该命令调用用sav命令储存的状态
        :param nrf: 数字范围参考仪器手册
        :return: None
        """
        self.write(Ieee488Const.RCL, nrf)

    def rst(self):
        """
        出厂设置
        :return: None
        """
        self.write(Ieee488Const.RST)

    def sav(self, nrf: int = 1):
        """
        保持设置到指定存储位置, 以供rcl调用
        :param nrf: 数字范围参考仪器手册
        :return: None
        """
        self.write(Ieee488Const.SAV, nrf)

    def sre(self, nrf: int = None):
        """
        查询设定服务请求使能寄存器
        :param nrf: 数字范围参考仪器手册
        :return: 服务请求使能寄存器状态
        """
        if nrf is not None:
            self.write(Ieee488Const.SRE, SPACE, nrf)
        return self.query(Ieee488Const.SRE, INTERROGATION, EMPTY)

    def stb(self):
        """
        查询状态寄存器值
        :return: 状态寄存器值
        """
        return self.query(Ieee488Const.STB)

    def trg(self):
        """
        发送一个触发信号, 触发信号内容根据仪器而定
        :return: None
        """
        self.write(Ieee488Const.TRG)

    def tst(self):
        """
        自检测试
        :return: 自检测试状态, 非0为不通过, 具体查看仪器定义
        """
        return self.query(Ieee488Const.TST)

    def wai(self):
        """
        发送等待命令, 直到命令完成, 否则不接受任何指令
        :return: None
        """
        self.write(Ieee488Const.WAI)

