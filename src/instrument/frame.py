# -*- encoding: utf-8 -*-
"""
@File    : frame.py
@Time    : 2020/7/20 15:13
@Author  : blockish
@Email   : blockish@yeah.net
"""
import time
from abc import ABC
from typing import Union
import serial.tools.list_ports

from errors import ResourceException
from instrument import Instrument


class FrameInstrument(Instrument, ABC):

    def __init__(self,
                 resource_name: int,
                 address: int,
                 baudrate: int,
                 timeout: float,
                 supported_baudrate: Union[list, tuple],
                 rw_delay: Union[list, tuple], **kwargs):
        super().__init__(resource_name, timeout, **kwargs)
        self._address = address
        self._instrument.baudrate = baudrate
        self._supported_baudrate = supported_baudrate
        self._rw_delay = rw_delay

    @property
    def supported_baudrate(self):
        return self._supported_baudrate

    @property
    def rw_delay(self):
        return self._rw_delay

    @staticmethod
    def list_resources():
        """
        获取所有串口(帧协议)资源列表
        :return: 资源列表
        """
        port_list = list(serial.tools.list_ports.comports())
        ports = []
        for ser in port_list:
            ports.append(ser.device if ser.name is None else ser.name)
        return ports

    def read(self, retry=10):
        """
        串口读数据
        :param retry: type int, 重试次数
        :return: 二进制数据list
        """
        if retry < 1:
            retry = 1
        count = 0
        result = bytearray()
        while retry > count:
            size = self._instrument.inWaiting()
            if size == 0:
                time.sleep(self._rw_delay[self._supported_baudrate.index(self._instrument.baudrate)])
                count += 1
            else:
                break
        while size > 0:
            buff = bytearray(self._instrument.read(size))
            result += buff
            time.sleep(self._rw_delay[self._supported_baudrate.index(self._instrument.baudrate)])
            size = self._instrument.inWaiting()

        if len(result) == 0:
            raise IOError("can't read data after retrying %d times" % retry)

        self._logger.info("recv: %s" % " ".join(["%02X" % i for i in result]))

        return list(result)

    def write(self, cmd, *args, **kwargs):
        """
        写命令
        :param cmd: 命令数据
        :return: None
        """
        if cmd is None:
            self._logger.warning('write command is None')
            return
        self._logger.info("send: " + " ".join(["%02X" % i for i in cmd]))
        self._instrument.write(bytearray(cmd))
        # time.sleep(self._rw_delay[self._supported_baudrate.index(self._instrument.baudrate)])

    def query(self, cmd, *args, **kwargs):
        """
        查询数据
        :param cmd: 命令数据
        :return: 二进制数据list
        """
        if cmd is None:
            self._logger.warning('query command is None')
            return
        self.write(cmd)
        return self.read()

    def open(self, resource_name):
        """
        打开串口(帧协议)资源
        :param resource_name: 串口资源名称
        :return: None
        :raise ResourceException
        """
        try:
            if self._resource_name is None:
                self._resource_name = resource_name
                serial_obj = serial.Serial(port=resource_name)
            else:
                if resource_name != self._resource_name:
                    self.close()
                    self.open(resource_name)
            return serial_obj
        except Exception as e:
            raise ResourceException(e)


