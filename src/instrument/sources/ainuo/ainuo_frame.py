# -*- encoding: utf-8 -*-

__all__ = {
    'An97Frame',
}

from constants import TUPLE_ON, TUPLE_OFF
from instrument.frame import FrameInstrument
from instrument.utils import *


STANDBY = 'STANDBY'  # 待机状态
PRESET = 'PRESET'  # 预值状态
RUN = 'RUN'  # 运行状态
SETTING = 'SETTING'  # 系统设置状态
ERROR = 'ERROR'  # 错误状态

BAUDRATE_TUPLE = (1200, 2400, 4800, 9600)
RW_DELAY_TUPLE = (0.4, 0.3, 0.2, 0.14)      # 串口写和读取之间的延迟, 与波特率相关, 如果出现通讯超时, 修改对应延迟参数
STATUS_TUPLE = (STANDBY, PRESET, RUN, SETTING, ERROR)
COMMAND_RESULT_DICT = {'=': 'Success', '!': 'Invalid', '?': 'Unsupported'}

CMD_START = 'CST'  # 开始即开启输入
CMD_STOP = 'CSP'  # 返回菜单或关闭输出
CMD_SET_IN = 'SNO'  # 设置输出参数
CMD_STATUS = 'RTE'  # 获取仪器状态
CMD_SET_OUT = 'RNT'  # 获取当前参数
CMD_SET_PRE = 'RNS'  # 设置预设参数
CMD_MODEL = 'RMO'  # 获取仪器型号信息
CMD_VER = 'RVE'  # 获取仪器软件版本


class An97Frame(FrameInstrument):

    def __init__(self, resource_name, address=1, baudrate=9600, timeout=0.15):
        super().__init__(resource_name, address, baudrate, timeout,
                         BAUDRATE_TUPLE, RW_DELAY_TUPLE)
        assert 0 < address < 255
        assert baudrate in self._supported_baudrate

    def idn(self):
        return '%s; %s' % (self._model(), self._version())

    def output(self, on_off):
        """
        电源输出开关, 在系统设置状态(setting), 预值状态(preset), 运行状态(run), 错误状态(error) output('OFF')都有效,
        仅当电源在待机状态(STAND_BY)下命令output('ON')有效
        :param on_off: 开关可选值{ON|1|OFF|0}
        :return:
            'Success': 命令执行成功
            'Invalid': 此状态下指令无效
            'Unsupported': 非法指令
        """
        if on_off in TUPLE_ON:
            self.write(self.__cmd('CST'))
        elif on_off in TUPLE_OFF:
            self.write(self.__cmd('CSP'))
        else:
            raise ParamException('unsupported on_off string %s' % on_off)
        response = self.read()
        return self.__parse_resp(response)

    def parameter(self, volt, freq, upper=5, lower=5, group=0, lock=1):
        """
        设置输出电压频率等参数, 仅当电源在预置或运行状态下命令有效
        :param volt: 电压值, 范围 1.-300.
        :param freq: 频率值, 范围 45.-65.以及400.
        :param upper: 电压波动上限值, 范围: 5.-30.
        :param lower: 电压波动下限值, 范围: 5.-30.
        :param group: 组, 范围: 0-6, 0表示没有组
        :param lock: 高档锁定, 范围: 0-1, 设置为1时, 电压参数在1-300连续可调, 否则, 以130为分界不连续
        :return:
            'Success': 命令执行成功
            'Invalid': 此状态下指令无效
            'Unsupported': 非法指令
        """
        self._logger.info('set parameter: %s, %s, %s, %s, %s, %s', volt, freq, upper, lower, group, lock)
        response = self.query(self.__cmd('SNO', volt, freq, upper, lower, group, lock))
        return self.__parse_resp(response)

    def status(self):
        """
        获取电源状态
        :return:
            'STAND_BY': 待机, 输出关断
            'PRESET': 预设
            'RUN': 运行, 输出开启
            'SETTING': 设置
            'ERROR': 错误
            'UNKNOWN': 未知状态, 可能仪器通讯出错
        """
        response = self.query(self.__cmd('RTE'))
        try:
            return STATUS_TUPLE[int(self.__parse_resp(response))]
        except ValueError:
            return 'UNKNOWN'

    def result(self):
        """
        获取电源的输出参数, 仅当电源在运行状态下命令有效
        :return:
            正确值为 电压 电流 频率 功率 值以逗号(,)分开
            'Invalid': 此状态下指令无效
            'Unsupported': 非法指令
        """
        response = self.query(self.__cmd('RNT'))
        return self.__parse_resp(response)

    def preset(self):
        """
        获取电源的预设输出参数, 仅当电源在预置状态下命令有效
        :return:
           正确值为 电压 频率 电压浮动上限值 电压浮动下限值 组 高档锁定 值以逗号(,)分开
            'Invalid': 此状态下指令无效
            'Unsupported': 非法指令
        """
        response = self.query(self.__cmd('RNS'))
        return self.__parse_resp(response)

    def _model(self):
        """
        获取电源的型号信息
        :return:
            正确数据为型号信息
            'Invalid': 此状态下指令无效
            'Unsupported': 非法指令
        """
        response = self.query(self.__cmd('RMO'))
        return self.__parse_resp(response)

    def _version(self):
        """
        获取电源的软件版本信息
        :return:
            正确数据为软件版本信息
            'Invalid': 此状态下指令无效
            'Unsupported': 非法指令
        """
        response = self.query(self.__cmd('RVE'))
        return self.__parse_resp(response)

    def __parse_resp(self, resp):
        """解析获取的结果"""
        start = 8
        end = len(resp) - 4
        if end < start:
            raise IOError('the data length is incorrect from serial')
        exec_str = hex_list_to_str(resp[start:end])[0]
        self._logger.info('Execute command result: %s', exec_str)
        sta = COMMAND_RESULT_DICT.get(exec_str)
        return sta if sta is not None else exec_str

    def __cmd(self, cmd_str, volt=None, freq=None, upper=None, lower=None, group=None, lock=None):
        """构建命令"""
        cmd = list()
        cmd.append(ord('{'))
        cmd.extend(value_to_hex(value=self._address, endian=BIG_ENDIAN, size=2, magnif=1))
        cmd.extend(ord(x) for x in cmd_str)
        cmd.append(ord('='))
        if volt is not None:
            volt = float('%.1f' % volt)
            if volt < 100:
                cmd.append(ord('0'))
            if volt < 10:
                cmd.append(ord('0'))
            volt_str = str(volt).replace('.', '')
            cmd.extend(ord(x) for x in volt_str)
            cmd.append(ord(','))
        if freq is not None:
            freq = float('%.1f' % freq)
            if freq < 100:
                cmd.append(ord('0'))
            freq_str = str(freq).replace('.', '')
            cmd.extend(ord(x) for x in freq_str)
            cmd.append(ord(','))
        if upper is not None:
            upper = int(upper)
            if upper < 10:
                cmd.append(ord('0'))
            upper_str = str(upper)
            cmd.extend(ord(x) for x in upper_str)
            cmd.append(ord(','))
        if lower is not None:
            lower = int(lower)
            if lower < 10:
                cmd.append(ord('0'))
            lower_str = str(lower)
            cmd.extend(ord(x) for x in lower_str)
            cmd.append(ord(','))
        if group is not None:
            cmd.append(ord(str(group)))
            cmd.append(ord(','))
        if lock is not None:
            cmd.append(ord(str(lock)))
            cmd.append(ord('*'))
        cmd.insert(1, len(cmd))
        count = 0
        for i in range(len(cmd) - 1):
            count = count + cmd[i + 1]
        cmd.extend(value_to_hex(value=count, endian=BIG_ENDIAN, size=1, magnif=1))
        cmd.append(ord('}'))
        return cmd
