# -*- encoding: utf-8 -*-
"""
@File    : itech_frame.py
@Time    : 2020/8/6 21:23
@Author  : blockish
@Email   : blockish@yeah.net
"""
__all__ = {
    'It8500Frame',
    'It8500PlusFrame',
}

from abc import ABC

from errors import ParamException, InstrumentException
from instrument import utils
from instrument.eloads.itech.itech import It85xx
from instrument.frame import FrameInstrument
from constants import TUPLE_ON, TUPLE_OFF
from .itech_frame_const import It85xxCmd, It8500Cmd, It8500PlusCmd


class It8500Series(FrameInstrument, It85xx, ABC):

    def __init__(self, resource_name, address=0, baudrate=9600, timeout=0.1):
        assert 0 <= address < 32 or address == 0xff
        assert baudrate in It85xxCmd.SUPPORTED_BAUDRATE_TUPLE
        super().__init__(resource_name, address, baudrate, timeout, It85xxCmd.SUPPORTED_BAUDRATE_TUPLE,
                         It85xxCmd.RW_DELAY_TUPLE)

    def write(self, cmd: list, queryable: bool = False) -> None:
        """
            写命令
        :param cmd: 命令数据
        :param queryable: 对于有返回值的则queryable为True, 否则为false
        :return: None
        """
        super().write(self._command(cmd))
        if cmd is not None and queryable is False:
            data = self.read()
            assert It85xxCmd.VALIDATE == data[2]
            response = data[3]
            if response != 0x80:
                self._logger.error('command: %s, response of code: 0x%s', ('%02x' % cmd[2]), ('%02x' % response))
                if response == 0x90:  # 校验和错误
                    raise InstrumentException('Checksum error')
                elif response == 0xa0:  # 设置参数错误或参数溢出
                    raise InstrumentException('Parameter error or overflow')
                elif response == 0xb0:  # 命令不能被执行
                    raise InstrumentException('Can\'t execute the command')
                elif response == 0xc0:  # 命令是无效的
                    raise InstrumentException('Command is invalid')
                elif response == 0xd0:  # 命令是未知的
                    raise InstrumentException('Command is unknown')
                else:
                    raise InstrumentException('Unknown error')
            else:
                self._logger.info('write response code: 0x%s', ('%02x' % response))
            # return response

    def query(self, cmd: list) -> list:
        """
            查询返回值数据
        :param cmd: 命令数据
        :return: (type list)返回值数据
        """
        if cmd is None:
            self._logger.warning('query command is None')
            return
        self.write(cmd, queryable=True)
        return self.read()

    def _command(self, op_value):
        """构建命令"""
        if op_value is not None:
            assert isinstance(op_value, list)
            cmd = [*It85xxCmd.IT85XX_CMD]
            cmd[1] = self._address
            for i in range(len(op_value)):
                cmd[2 + i] = op_value[i]
            cmd_last = len(cmd) - 1
            chk = sum(cmd[:24])
            chk &= 0xFF
            cmd[cmd_last] = chk
            return cmd

    def remote(self, on_off) -> None:
        if on_off in TUPLE_ON:
            self.write([It85xxCmd.LOCAL_REMOTE_SET, 1])
            self.write([It85xxCmd.LOCAL_EN_SET, 1])
        elif on_off in TUPLE_OFF:
            self.write([It85xxCmd.LOCAL_REMOTE_SET, 0])
            self.write([It85xxCmd.LOCAL_REMOTE_SET, 0])
        else:
            self._logger.error('Error remote parameter, value is %s' % on_off)
            raise ParamException(
                'The param "on_off" expect value "ON", "OFF", "0" or "1" not: %s' % on_off)

    def initialize(self) -> None:
        super().initialize()
        self.cls()
        self._work_mode(FIXED)  # 初始化work mode为 fixed
        result = self.hardware_ranges()
        if result is not None:  # IT8500不支持hardware_ranges()方法
            self._max_volt = result['MAX_VOLTAGE']
            self._min_volt = result['MIN_VOLTAGE']
            self._max_curr = result['MAX_CURRENT']
            self._max_power = result['MAX_POWER']
            self._max_res = result['MAX_RESISTANCE']
            self._min_res = result['MIN_RESISTANCE']

    def idn(self) -> str:
        """
            获取仪器型号, 软件版本等信息
        :return: (type str) 仪器型号, 软件版本等信息
        """
        data = self.query([It85xxCmd.MODEL_VERSION_GET, ])  # 获取负载信息
        model = utils.hex_list_to_str(data[3:8])[0]
        ver = data[8:10]
        ver_1 = ver[1] >> 8
        ver_2 = ver[1] & 0x0f
        ver_3 = ver[0] >> 8
        ver_4 = ver[0] & 0x0f
        ver = ('' if ver_1 == 0 else str(ver_1)) + str(ver_2) + '.' + str(ver_3) + str(ver_4)
        sno = utils.hex_list_to_str(data[10:20])[0]
        self._info = '%s %s; %s; %s' % ('ITECH', model, ver, sno)
        self._logger.info('instrument info: %s', self._info)
        # return ret

    def sn(self):
        """
            获取当前电子负载的SN
        :return: (type str) SN
        """
        data = self.query([It85xxCmd.SN_GET, ])  # 获取负载序列号
        sn = utils.hex_list_to_str(data[3:22])[0]
        self._logger.info('SN: %s', sn)
        return sn

    def trg(self) -> None:
        """
            发送一个Bus触发信号, 注意IT8500与IT8500+区别
        :return: None
        """
        self.write([It85xxCmd.TRIG_BUS, ])

    def sav(self, nrf):
        """
        保存设置到指定存储区域, 方便快捷调用
        :param nrf: 存储区域, 范围1~9
        :return: None
        """
        self.write([It85xxCmd.SETTINGS_SAVE, nrf])

    def rcl(self, nrf):
        """
        从指定存储区域调用保存设置
        :param nrf: 存储区域, 范围1~9
        :return: None
        """
        self.write([It85xxCmd.SETTINGS_CALL, nrf])

    def load(self, on_off: str) -> None:
        """
            负载开启关断
        :param on_off: (type str): 可选值为 {ON|1|OFF|0}
        :return:
            None
        """
        cmd = It85xxCmd.DICT_LOAD_ON_OFF_SET.get(on_off)
        self.write(cmd)

    def short(self, on_off: str = None) -> bool:
        """
            负载短路开启关断
        :param on_off: (type str): 可选值为 {ON|1|OFF|0}
        :return:
            True or false
        """
        if on_off in TUPLE_ON:
            res = self._work_mode(SHORT)
        elif on_off in TUPLE_OFF:
            res = self._work_mode(FIXED)
        else:
            self._logger.error('Error remote parameter, value is %s' % on_off)
            raise ParamException(
                'The param "on_off" expect value "ON", "OFF", "0" or "1" not: %s' % on_off)
        return SHORT == res

    def _work_mode(self, mode: str = None) -> str:
        """
            设置获取负载的工作模式
                注意: 新IT8500系列不支持电池模式
        :param mode: (type str): 工作模式, 可选值 {fix|short|tran|list|batt}
        :return:
            (type str) fix|short|tran|list|batt
        """
        cmd = It85xxCmd.DICT_WORK_MODE_SET.get(mode)
        self.write(cmd)
        data = self.query([It85xxCmd.WORK_MODE_GET, ])
        return_mode = TUPLE_WORK_MODE[data[3]]
        self._logger.info('work mode changed to: "%s"', return_mode)
        return return_mode

    def list_mode(self, eload_mode: str = CC, curr_range: float = None, repeat: int = 1, *steps) -> tuple:
        """
            list模式操作
        :param eload_mode: (type srt): 电子负载工作模式, 可选值为{CC|CV|CW|CR}, 分别对应恒流, 恒压, 恒功率, 恒阻
                注意: 新IT8500 list模式只支持CC模式(我们目前的都是此系列)
        :param curr_range: (type float): IT8500+当前list模式最大可输入电流, CC模式时必须指定, IT8500必须指定为None
        :param repeat: (type int): list重复次数
        :param steps: (type tuple or list of dict): 设置list的每一步, 每一步为一个dict, 包含的键值如下:
                value (type float): 当前步负载工作模式值
                time (type float): 当前步持续时间, 单位为S
                slew (type float): 当eload_mode为CC模式时, 设定此值为当前步电流的上升下降斜率
        :return:
            (type int): 当前list的步数, (type int): 当前list的重复次数
        """
        step = len(steps)
        # 步数不能大于85
        assert 1 < step < 85, 'the steps must between 2 and 84'
        # 设置电子负载负载模式
        self._load_mode(eload_mode)
        # 设置电子负载list步数
        self.write(_value_command([It85xxCmd.LIST_STEP_SET, ], value=step, size=2, magnif=1))
        # 设置电流保护值
        if CC == eload_mode:
            assert curr_range is not None, 'must specify the current range'
            self.write(
                _value_command([It8500PlusCmd.LIST_CURR_RANGE_SET, ], value=curr_range, size=4, magnif=10000))
        cmd = list()
        # 设置电子负载list每步参数
        cmd.append(It85xxCmd.DICT_LIST_STEP.get(eload_mode))
        for i in range(step):
            _cmd = [*cmd]
            _value = steps[i].get('value')
            _time = steps[i].get('time')
            _cmd.extend(utils.value_to_hex(value=i + 1, size=2, magnif=1))
            _cmd.extend(utils.value_to_hex(value=_value, magnif=10000 if CC == eload_mode else 1000))
            _cmd.extend(utils.value_to_hex(value=_time, magnif=10000))
            if CC == eload_mode:
                _slew = steps[i].get(SLEW)
                _cmd.extend(utils.value_to_hex(value=_slew, size=2, magnif=10000))
            self.write(_cmd)
        # 设置电子负载list重复次数
        assert repeat is not None, 'must specify the repeat times'
        self.write(_value_command([It85xxCmd.LIST_REPEAT_SET, ], value=repeat, size=2, magnif=1))
        # 设置电子负载工作模式为list
        self._work_mode(LIST)

        step_data = self.query([It85xxCmd.LIST_STEP_GET, ])
        repeat_data = self.query([It85xxCmd.LIST_REPEAT_GET, ])

        return int(utils.hex_to_value(step_data[3:5], magnif=1)), int(utils.hex_to_value(repeat_data[3:5], magnif=1))

    def _tran_mode(self, is_new, eload_mode, level_a, time_a, level_b, time_b, tran) -> tuple:
        """
            TRAN模式操作, 注意: 当设置负载模式为CC时, 记得调用curr_slew()设置电流上升下降斜率
                            设置完成之后, 记得调用load()开启负载
        :param is_new: 是否为新指令, 针对于IT8500和IT8500+电流a, b值的时间设置最小值分别为0.1ms和0.01ms
        :param eload_mode: (type srt): 电子负载工作模式, 可选值为{CC|CV|CW|CR}, 分别对应恒流, 恒压, 恒功率, 恒阻
        :param level_a: (type float): A值
        :param time_a: (type float): A值持续时间, 单位为S, 当tran为toggle时, 此值无效
        :param level_b: (type float): B值
        :param time_b: (type float): B值持续时间, 单位为S, 当tran为toggle时, 此值无效
        :param tran: (type str): TRAN模式, 可选值为{continuous|pulse|toggle}
                注意:  eload_mode为CV或CW 时, tran只能为toggle
                       eload_mode为CR 时, tran只能为pulse或toggle
        :return: (type tuple)
            当前设置的level_A, time_A, level_B, time_B, 当前动态模式(0表示continuous, 1表示pulse, 2表示toggle)
        """
        # 设置负载模式
        self._load_mode(eload_mode)
        # 设置负载工作模式为transition
        self._work_mode(TRANSITION)
        # 设置transition参数
        cmd = []
        cmd.extend([
            It8500PlusCmd.DYN_CURR_SET if is_new is True else It85xxCmd.DYN_CURR_SET if CC == eload_mode else
            It85xxCmd.DYN_VOLT_SET if CV == eload_mode else
            It85xxCmd.DYN_POWER_SET if CW == eload_mode else
            It85xxCmd.DYN_RES_SET if CR == eload_mode else
            utils.raiser(ParamException('Unsupported load mode')), ])

        cmd.extend(utils.value_to_hex(value=level_a, endian='little', size=4,
                                      magnif=10000 if CC == eload_mode else 1000))
        cmd.extend(utils.value_to_hex(value=time_a, endian='little', size=4,
                                      magnif=100000 if is_new is True else 10000))
        cmd.extend(utils.value_to_hex(value=level_b, endian='little', size=4,
                                      magnif=10000 if CC == eload_mode else 1000))
        cmd.extend(utils.value_to_hex(value=time_b, endian='little', size=4,
                                      magnif=100000 if is_new is True else 10000))
        cmd.extend(
            [0, ] if CONTINUOUS == tran else
            [1, ] if PULSE == tran else
            [2, ] if TOGGLE == tran else
            utils.raiser(ParamException('Unsupported transition mode'))
        )
        self.write(cmd)
        # 读取相关参数
        data = self.query([
            It8500PlusCmd.DYN_CURR_GET if is_new is True else It85xxCmd.DYN_CURR_GET if CC == eload_mode else
            It85xxCmd.DYN_VOLT_GET if CV == eload_mode else
            It85xxCmd.DYN_POWER_GET if CW == eload_mode else
            It85xxCmd.DYN_RES_GET if CR == eload_mode else
            utils.raiser(ParamException('Unsupported load mode')), ])
        return_level_a = utils.hex_to_value(data=data[3:7], endian='little',
                                            magnif=10000 if CC == eload_mode else 1000)
        return_a_time = utils.hex_to_value(data=data[7:11], endian='little',
                                           magnif=100000 if is_new is True else 10000)
        return_level_b = utils.hex_to_value(data=data[11:15], endian='little',
                                            magnif=10000 if CC == eload_mode else 1000)
        return_time_b = utils.hex_to_value(data=data[15:19], endian='little',
                                           magnif=100000 if is_new is True else 10000)
        return_tran = data[19:20][0]
        return return_level_a, return_a_time, return_level_b, return_time_b, TUPLE_TRAN_MODE[return_tran]

    def _load_mode(self, mode: str):
        if mode is not None:
            # 设置工作模式为 fixed
            self._work_mode(FIXED)
            cmd = It85xxCmd.DICT_ELOAD_MODE.get(mode)
            self.write(cmd)
        data = self.query([It85xxCmd.LOAD_MODE_GET, ])
        return_mode = TUPLE_WORK_MODE[data[3]]
        self._logger.info('current e-load mode: "%s"', return_mode)
        return return_mode

    def load_mode(self, mode: str, value: float = None, lower: float = None, upper: float = None) -> tuple:
        """
            设置获取负载的负载模式
        :param mode: (type str): 工作模式, 可选值 {CC|CV|CW|CR}
        :param value: (type float) 对应模式的设置值
        :param lower: (type float) 对应模式的相应上下限限制:
            定电流时电压上下限; 定电压时电流上下限; 定功率时电压上下限; 定电阻时电压上下限;
        :param upper: (type float) 参考 lower
        :return
            ('CC', 'CV', 'CW' or 'CR'), value, lower, upper
        """
        return_mode = self._load_mode(mode)
        # 设置相关参数
        self.write(_value_command(It85xxCmd.CC_VALUE_SET if CC == mode else
                                  It85xxCmd.CV_VALUE_SET if CV == mode else
                                  It85xxCmd.CR_VALUE_SET if CR == mode else
                                  It85xxCmd.CW_VALUE_SET if CW == mode else
                                  utils.raiser(ParamException('Unsupported load mode')),
                                  value=value, endian='little', size=4,
                                  magnif=10000 if CC == mode else 1000))

        data = self.query(It85xxCmd.CC_VALUE_GET if CC == mode else
                          It85xxCmd.CV_VALUE_GET if CV == mode else
                          It85xxCmd.CR_VALUE_GET if CR == mode else
                          It85xxCmd.CW_VALUE_GET if CW == mode else
                          utils.raiser(ParamException('Unsupported load mode')))
        return_value = utils.hex_to_value(data=data[3:7], endian='little',
                                          magnif=10000 if CC == mode else 1000)
        return_lower, return_upper = (None, None)
        if lower is not None:
            self.write(_value_command(It8500PlusCmd.DICT_CM_LOWER_SET_SET.get(mode), upper,
                                      magnif=10000 if CC == mode else 1000))
            data = self.query(It8500PlusCmd.DICT_CM_LOWER_GET.get(mode))
            return_lower = utils.hex_to_value(data=data[3:7], endian='little',
                                              magnif=10000 if CC == mode else 1000)
        if upper is not None:
            self.write(_value_command(It8500PlusCmd.DICT_CM_UPPER_SET_SET.get(mode), upper,
                                      magnif=10000 if CC == mode else 1000))
            data = self.query(It8500PlusCmd.DICT_CM_UPPER_GET.get(mode))
            return_upper = utils.hex_to_value(data=data[3:7], endian='little',
                                              magnif=10000 if CC == mode else 1000)
        return return_mode, return_value, return_lower, return_upper

    def input_limit(self, volt=None, curr=None, power=None, res=None):
        """
        设置或读取最大输入值(电压, 电流, 功率)
        :param volt: 最大输入电压值(float精度为1mV)
        :param curr: 最大输入电流值(float精度为0.1mA)
        :param power: 最大输入功率值(float精度为1mW)
        :param res: 最大输入电阻值(仅IT8500+)(float精度为1mΩ)
        :return:
            最大输入电压值, 最大输入电流值, 最大输入功率值, 最大输入电阻值
        """
        if volt is not None:
            self.write(_value_command([It85xxCmd.MAX_INPUT_VOLT_SET, ], volt, magnif=1000))
        if curr is not None:
            self.write(_value_command([It85xxCmd.MAX_INPUT_CURR_SET, ], curr, magnif=10000))
        if power is not None:
            self.write(_value_command([It85xxCmd.MAX_INPUT_POWER_SET, ], curr, magnif=1000))
        if res is not None:
            self.write(_value_command([It8500PlusCmd.MAX_INPUT_RES_SET, ], res, magnif=1000))
        data = self.query([It85xxCmd.MAX_INPUT_VOLT_GET, ])
        return_volt = utils.hex_to_value(data[3:7], magnif=1000)
        data = self.query([It85xxCmd.MAX_INPUT_CURR_GET, ])
        return_curr = utils.hex_to_value(data[3:7], magnif=10000)
        data = self.query([It85xxCmd.MAX_INPUT_POWER_GET, ])
        return_power = utils.hex_to_value(data[3:7], magnif=1000)
        return_res = None
        if res is not None:
            data = self.query([It8500PlusCmd.MAX_INPUT_RES_GET, ])
            return_res = utils.hex_to_value(data[3:7], magnif=1000)
        return return_volt, return_curr, return_power, return_res

    def trigger_source(self, source: str = None) -> str:
        """
            设置电子负载的触发源
        :param source: (type str): 触发源, 可选值为{manu|ext|bus|hold}
        :return: (type str): 'MANual', 'EXTernal', 'BUS' or 'HOLD'
        """
        if source is not None:
            cmd = It85xxCmd.DICT_TRIG_MODE.get(source)
            self.write(cmd)
        data = self.query([It85xxCmd.TRIG_MODE_GET, ])
        return_src = TUPLE_TRIGGER_MODE[data[3]]
        self._logger.info('current trigger source: "%s"', return_src)
        return return_src

    def _content(self, is_plus):
        # 读取负载的输入电压,输入电流,输入功率及操作状态寄存器,查询状态寄存器,散热器温度,工作模式,当前LIST的步数,当前LIST的循环次数
        data = self.query([It85xxCmd.CONTENT_1_GET, ])
        in_volt = utils.hex_to_value(data[3:7], magnif=1000)
        in_curr = utils.hex_to_value(data[7:11], magnif=10000)
        in_power = utils.hex_to_value(data[11:15], magnif=1000)
        operation_register = data[15]
        query_register = data[16] | (data[17] << 8)
        temperature = data[20]
        work_mode = data[21]
        list_step = data[22]
        list_repeat = data[23] | (data[24] << 8)
        if is_plus is True:
            # 带载容量[3:7], 带载时间或上升/下降时间[7:11], 定时器剩余时间[11:15]
            data = self.query([It8500PlusCmd.CONTENT_2_GET, ])
            load_cap = utils.hex_to_value(data[3:7], magnif=10000)
            rf_time = utils.hex_to_value(data[7:11], magnif=10000)
            remain_time = utils.hex_to_value(data[11:15], magnif=1000)     # TODO magif?
            # 最大输入电压值[3:7], 最小输入电压值[7:11], 最大输入电流值[11:15], 最小输入电流值[15:19]
            data = self.query([It8500PlusCmd.CONTENT_3_GET, ])
            max_in_volt = utils.hex_to_value(data[3:7], magnif=1000)
            min_in_volt = utils.hex_to_value(data[7:11], magnif=1000)
            max_in_curr = utils.hex_to_value(data[11:15], magnif=10000)
            min_in_curr = utils.hex_to_value(data[15:19], magnif=10000)
            return in_volt, in_curr, in_power, operation_register, query_register, \
                temperature, work_mode, list_step, list_repeat, load_cap, rf_time, \
                remain_time, max_in_volt, min_in_volt, max_in_curr, min_in_curr
        else:
            return in_volt, in_curr, in_power, operation_register, query_register, \
                   temperature, work_mode, list_step, list_repeat


class It8500Frame(It8500Series):

    def __init__(self, resource_name, addr=0, baudrate=9600, timeout=0.1):
        super().__init__(resource_name, addr, baudrate, timeout)

    def content(self):
        """
        获取仪器所有状态值
        :return:
            (type float): 当前输入电压
            (type float): 当前输入电流
            (type float): 当前输入功率
            (type int): 当前操作状态寄存器值
            (type int): 当前查询状态寄存器值
            (type float): 当前散热器温度
            (type int): 当前电子负载工作模式 0: 'FIXed', 1: 'SHORt', 2: 'TRANsition', 3: 'LIST', 4: 'BATTery'
            (type int): 当前list执行的步数
            (type int): 当前list执行的重复次数
        状态寄存器和询状态寄存器位说明如下:
        operation status register:
--------------------------------------------------------------------------------------------------------------------------------------------------------
|    7   |             6             |       5      |             4           |       3       |       2       |      1       |            0            |
| :-----:|            :----:         |    :----:    |          :----:         |     :----:    |     :----:    |    :----:    |        :----:           |
| no use | FOR LOAD ON timer status  | SENSE status | local key enable status | output status | remote status | wait trigger | calibration mode status |
--------------------------------------------------------------------------------------------------------------------------------------------------------

        query status register
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|         12         |        11      |         10        |          9          |        8       |         7        |         6        |                5             |         4         |      3     |       2      |       1      |        0        |
|       :-----:      |     :----:     |      :----:       |       :----:        |      :----:    |       :----:     |      :----:      |            :----:            |      :----:       |   :----:   |    :----:    |    :----:    |      :----:     |
| auto test complete | auto test fail | auto test success | constant resistance | constant power | constant voltage | constant current | remote measure not connected | over temperature  | over power | over current | over voltage | reverse voltage |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        """
        return self._content(False)

    def tran_mode(self, eload_mode, level_a, time_a, level_b, time_b, tran) -> tuple:
        """
            TRAN模式操作, 注意: 设置完成之后, 记得调用load()开启负载
        :param eload_mode: (type srt): 电子负载工作模式, 可选值为{CC|CV|CW|CR}, 分别对应恒流, 恒压, 恒功率, 恒阻
        :param level_a: (type float): 电流A值
        :param time_a: (type float): A值持续时间, 最小值为0.1ms, 单位为S, 当tran为toggle时, 此值无效
        :param level_b: (type float): 电流B值
        :param time_b: (type float): B值持续时间, 最小值为0.1ms, 单位为S, 当tran为toggle时, 此值无效
        :param tran: (type str): TRAN模式, 可选值为{continuous|pulse|toggle}
                注意:  eload_mode为CV或CW 时, tran只能为toggle
                       eload_mode为CR 时, tran只能为pulse或toggle
        :return: (type tuple)
            当前设置的level_A, time_A, level_B, time_B, 当前动态模式(0表示continuous, 1表示pulse, 2表示toggle)
        """
        return super()._tran_mode(False, eload_mode, level_a, time_a, level_b, time_b, tran)

    def von_mode(self, von=None, voff=None):
        """
        设置负载的带载/卸载电压
        :param von: 带载电压(float 精度1mV)
        :param voff: 卸载电压(float 精度1mV)
        :return:
            带载电压, 卸载电压
        """
        if von is not None:
            self.write(_value_command([It8500Cmd.LOAD_VOLT_SET, ], von, magnif=1000))
        if voff is not None:
            self.write(_value_command([It8500Cmd.UNLOAD_VOLT_SET, ], voff, magnif=1000))
        data = self.query([It8500Cmd.LOAD_VOLT_GET, ])
        return_von = utils.hex_to_value(data[3:7], magnif=1000)
        data = self.query([It8500Cmd.UNLOAD_VOLT_GET, ])
        return_voff = utils.hex_to_value(data[3:7], magnif=1000)
        return return_von, return_voff


class It8500PlusFrame(It8500Series):

    def __init__(self, resource_name, addr=0, baudrate=9600, timeout=0.1):
        super().__init__(resource_name, addr, baudrate, timeout)

    def cls(self) -> None:
        """
        清除保护状态
        :return:
            None
        """
        self.write([It8500PlusCmd.PROT_STATUS_CLEAR, ])

    def trg(self) -> None:
        """
            发送一个任意触发信号, 不论设置的触发源为什么, 均产生触发
        :return:
            None
        """
        self.write([It8500PlusCmd.TRIGGER, ])

    def content(self):
        """
        获取仪器所有状态值
        :return:
            (type float): 当前输入电压
            (type float): 当前输入电流
            (type float): 当前输入功率
            (type int): 当前操作状态寄存器值
            (type int): 当前查询状态寄存器值
            (type float): 当前散热器温度
            (type int): 当前电子负载工作模式 0: 'FIXed', 1: 'SHORt', 2: 'TRANsition', 3: 'LIST', 4: 'BATTery'
            (type int): 当前list执行的步数
            (type int): 当前list执行的重复次数
            (type float): 带载容量
            (type float): 带载时间或上升/下降时间
            (type float): 定时器剩余时间
            (type float): 最大输入电压值
            (type float): 最小输入电压值
            (type float): 最大输入电流值
            (type float): 最小输入电流值
        状态寄存器和询状态寄存器位说明如下:
        operation status register:
--------------------------------------------------------------------------------------------------------------------------------------------------------
|    7   |             6             |       5      |             4           |       3       |       2       |      1       |            0            |
| :-----:|            :----:         |    :----:    |          :----:         |     :----:    |     :----:    |    :----:    |        :----:           |
| no use | FOR LOAD ON timer status  | SENSE status | local key enable status | output status | remote status | wait trigger | calibration mode status |
--------------------------------------------------------------------------------------------------------------------------------------------------------

        query status register
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|         12         |        11      |         10        |          9          |        8       |         7        |         6        |                5             |         4         |      3     |       2      |       1      |        0        |
|       :-----:      |     :----:     |      :----:       |       :----:        |      :----:    |       :----:     |      :----:      |            :----:            |      :----:       |   :----:   |    :----:    |    :----:    |      :----:     |
| auto test complete | auto test fail | auto test success | constant resistance | constant power | constant voltage | constant current | remote measure not connected | over temperature  | over power | over current | over voltage | reverse voltage |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        """
        return self._content(True)

    def tran_mode(self, eload_mode, level_a, time_a, level_b, time_b, tran) -> tuple:
        """
            TRAN模式操作, 注意: 当设置负载模式为CC时, 记得调用curr_slew()设置电流上升下降斜率
                            设置完成之后, 记得调用load()开启负载
        :param eload_mode: (type srt): 电子负载工作模式, 可选值为{CC|CV|CW|CR}, 分别对应恒流, 恒压, 恒功率, 恒阻
        :param level_a: (type float): A值
        :param time_a: (type float): A值持续时间, 最小值为0.01ms, 单位为S, 当tran为toggle时, 此值无效
        :param level_b: (type float): B值
        :param time_b: (type float): B值持续时间, 最小值为0.01ms, 单位为S, 当tran为toggle时, 此值无效
        :param tran: (type str): TRAN模式, 可选值为{continuous|pulse|toggle}
                注意:  eload_mode为CV或CW 时, tran只能为toggle
                       eload_mode为CR 时, tran只能为pulse或toggle
        :return: (type tuple)
            当前设置的level_A, time_A, level_B, time_B, 当前动态模式(0表示continuous, 1表示pulse, 2表示toggle)
        """
        return super()._tran_mode(True, eload_mode, level_a, time_a, level_b, time_b, tran)

    def get_ripple(self) -> tuple:
        """
            获取谐波参数
        :return:
            (type float): 谐波电压, (type float): 谐波电流
        """
        data = self.query([It8500PlusCmd.ALL_RIPPLE_GET, ])
        volt_data = utils.hex_to_value(data=data[3:7], endian='little', magnif=100000)
        curr_data = utils.hex_to_value(data=data[7:11], endian='little', magnif=1000000)
        return volt_data, curr_data

    def hardware_ranges(self) -> dict:
        """
            获取硬件量程
        :return:
            (type dict): 字典说明
                'MAX_CURRENT': max_curr, 最大电流
                'MAX_VOLTAGE': max_volt, 最大电压
                'MIN_VOLTAGE': min_volt, 最小电压
                'MAX_POWER': max_power, 最大功率
                'MAX_RESISTANCE': max_res, 最大电阻
                'MIN_RESISTANCE': min_res, 最小电阻
        """
        data = self.query([It8500PlusCmd.HARDWARE_RANGE_GET, ])
        max_curr = utils.hex_to_value(data[3:7], endian='little', magnif=10000)
        max_volt = utils.hex_to_value(data[7:11], endian='little', magnif=1000)
        min_volt = utils.hex_to_value(data[11:15], endian='little', magnif=1000)
        max_power = utils.hex_to_value(data[15:19], endian='little', magnif=1000)
        max_res = utils.hex_to_value(data[19:23], endian='little', magnif=1000)
        min_res = utils.hex_to_value(data[23:25], endian='little', magnif=1000)
        return {
            'MAX_CURRENT': max_curr,
            'MAX_VOLTAGE': max_volt, 'MIN_VOLTAGE': min_volt,
            'MAX_POWER': max_power,
            'MAX_RESISTANCE': max_res, 'MIN_RESISTANCE': min_res,
        }

    def auto_range(self, on_off=None) -> int:
        """
            设置电压表自动量程
        :param on_off: (type str): 自动量程开关, 可选参数 {ON|1|OFF|0}
        :return:
            电压表自动量程状态, True/False
        """
        cmd = It8500PlusCmd.DICT_VOLT_AUTO_RANGE_SET.get(on_off)
        self.write(cmd)
        return_data = self.query([It8500PlusCmd.VOLT_AUTO_RANGE_GET, ])
        return return_data[3] == 1

    def auto_test_mode(self, is_load=False, nrf=1, stop_cond=COMPLETE, *steps):
        """
            自动测试, 注意避免如下情况:
                 自动测试文件最后一步短路;
                 自动测试文件最后一步测试时输入电压小于设置之开始电压.
        :param is_load: (type bool)是否为加载文件, 如果为True, 则表示加载自动测试文件并直接进入自动测试, 否则为设置自动测试的步骤
        :param nrf: (type int)加载或保存的文件编号, 范围 1~10
        :param stop_cond: (type str) 停止条件, 可选值{complete|failure}, 分别表示测试完成时停止和测试失败时停止
        :param steps: (type list or tuple of dict)自动测试的步数, 最多支持10步, 每一步为一个dict,  其中字典说明如下:
            is_pause: (type bool)当前步是否暂停
            is_short: (type bool)当前步是否短路
            load_time: (type float)带载时间, 单位S
            test_time: (type float)测试时间, 单位S
            unload_time: (type float)卸载时间, 单位S
        :return: 当前自动测试的步数
        """
        if is_load is True:
            self.write([It8500PlusCmd.AUTO_TEST_CALL, nrf])
        elif is_load is False:
            step_count = 1
            for step in steps:
                # 1. 设置步
                self.write(_value_command([It8500PlusCmd.AUTO_TEST_STEP_SET, ], step_count, magnif=1))
                is_pause = step.get('stop', False)
                if is_pause is True:
                    self.write(_value_command([It8500PlusCmd.AUTO_TEST_PAUSE_STEP_SET, ], step_count, magnif=1))
                is_short = step.get('short', False)
                if is_short is True:
                    self.write(_value_command([It8500PlusCmd.AUTO_TEST_SHORT_STEP_SET, ], step_count, magnif=1))
                load_time = step.get('load_time', None)
                self.write(_value_command([It8500PlusCmd.AUTO_TEST_LOAD_TIME_SET, ], load_time, magnif=1000))
                test_time = step.get('test_time', None)
                self.write(_value_command([It8500PlusCmd.AUTO_TEST_TEST_TIME_SET, ], test_time, magnif=1000))
                unload_time = step.get('unload_time', None)
                self.write(_value_command([It8500PlusCmd.AUTO_TEST_UNLOAD_TIME_SET, ], unload_time, magnif=1000))

                link = step.get('link', 0)
                self.write([It8500PlusCmd.AUTO_TEST_LINK_SET, link, ])
                step_count += 1
            self.write([It8500PlusCmd.AUTO_TEST_STOP_SET, TUPLE_STOP_COND.index(stop_cond), ])
            self.write([It8500PlusCmd.AUTO_TEST_SAVE, ])
            return step_count - 1
        else:
            self._logger.warn('Invalid parameter %s', is_load)
            raise ParamException(
                'The param "is_load" expect value True or False not: %s' % is_load)

    def curr_protection(self, enable=True, curr=None, curr_del=None):
        """
        过电流保护设置或查询
        :param enable: 过电流保护使能
        :param curr: 过电流保护设置值
        :param curr_del: 过电流保护延时设置值
        :return: 过电流保护使能, 过电流保护设置值, 过电流保护延时设置值
        """
        if enable is False:
            self.write([It8500PlusCmd.PC_ENABLE_SET, 0])
        elif enable is True:
            self.write([It8500PlusCmd.PC_ENABLE_SET, 1])
            self.write(_value_command([It8500PlusCmd.P_CURR_SET, ], curr, magnif=10000))
            self.write(_value_command([It8500PlusCmd.PC_DELAY_SET, ], curr_del, magnif=1000))
        else:
            self._logger.warn('Invalid parameter %s', enable)
            raise ParamException(
                'The param "enable" expect value True or False not: %s' % enable)
        data = self.query([It8500PlusCmd.PC_ENABLE_GET, ])
        return_enable = data[3]
        data = self.query([It8500PlusCmd.P_CURR_GET, ])
        return_curr = utils.hex_to_value(data[3:7], magnif=10000)
        data = self.query([It8500PlusCmd.PC_DELAY_GET, ])
        return_curr_del = utils.hex_to_value(data[3:7], magnif=1000)
        return return_enable, return_curr, return_curr_del

    def power_protection(self, power=None, power_del=None):
        """
        设置或查询电子负载过功率保护相关参数
        :param power: 过功率保护设置值, 默认单位为W, 最小值为1mW
        :param power_del: 过功率保护延时设置值, 默认单位为S, 最小值为1ms
        :return: 过功率保护设置值, 过功率保护延时设置值
        """
        self.write(_value_command([It8500PlusCmd.SP_POWER_SET, ], power, magnif=1000))
        self.write(_value_command([It8500PlusCmd.SP_POWER_DELAY_SET, ], power, magnif=1000))
        data = self.query([It8500PlusCmd.SP_POWER_GET, ])
        return_pow = utils.hex_to_value(data[3:7], magnif=1000)
        data = self.query([It8500PlusCmd.SP_POWER_DELAY_GET, ])
        return_delay = utils.hex_to_value(data[3:7], magnif=1000)
        return return_pow, return_delay

    def von_mode(self, mode=None, value=None):
        """
        设置负载的VON模式
        根据 VON 带载电压值, 负载有两种表现模式, living 和 latch.
        当选择 living, 表示工作跟随状态:
            即待测电源电压上升且大于 Von Point 带载电压时, 负载开始带载测试.
            当待测电源电压下降且小于 Von Point 卸载电压时, 负载则卸载.
        当选择 latch, 表示工作带载点锁存带载状态:
            即待测电源电压上升且大于 Von Point 带载电压时, 负载开始带载测试.
            当待测电源电压下降且小于 Von Point 卸载电压时, 负载不会卸载.
        :param mode: VON模式
        :param value: VON电压(float 精度1mV), 设置为0即为最小电压值, 但此时电压值不为0
        :return:
            VON模式, VON电压
        """
        if mode in It8500PlusCmd.DICT_VON_MODE_SET:
            self.write([It8500PlusCmd.VON_MODE_SET, mode])
        if value is not None:
            self.write(_value_command([It8500PlusCmd.VON_VOLT_SET, ], value, magnif=1000))
        data = self.query([It8500PlusCmd.VON_MODE_GET, ])
        return_mode = TUPLE_VON_MODE[data[3]]
        data = self.query([It8500PlusCmd.VON_VOLT_GET, ])
        return_value = utils.hex_to_value(data[3:7], magnif=1000)
        return return_mode, return_value

    def cr_led_mode(self, on_off, cr=None, cr_volt=None):
        """
        CR_LED功能
        :param on_off: (type str) CR_LED功能开关, 当此值设置为OFF|0时, 后面的设置参数将忽略
        :param cr: (type float) CR_LED功能恒阻阻值, 默认单位为Ω, 最小值为1mΩ
        :param cr_volt: (type float) CR_LED功能关断电压, 默认单位为V, 最小值为1mV
        :return: CR_LED功能恒阻阻值, CR_LED功能关断电压
        """
        if on_off in TUPLE_ON:
            mode, value = self.load_mode(CR, cr)
            self.write([It8500PlusCmd.CR_LED_FUNC_SET, 1])
            self.write(_value_command([It8500PlusCmd.CR_LED_CUTOFF_VOLT_SET, ], cr_volt, magnif=1000))
            data = self.query([It8500PlusCmd.CR_LED_FUNC_GET, ])
            assert data[3] == 1
            data = self.query([It8500PlusCmd.CR_LED_CUTOFF_VOLT_GET, ])
            volt = utils.hex_to_value(data[3:7], magnif=1000)
            return value, volt
        elif on_off in TUPLE_OFF:
            self.write([It8500PlusCmd.CR_LED_FUNC_SET, 0])
            data = self.query([It8500PlusCmd.CR_LED_FUNC_GET, ])
            assert data[3] == 0
        else:
            self._logger.error('Error remote parameter, value is %s' % on_off)
            raise ParamException(
                'The param "on_off" expect value "ON", "OFF", "0" or "1" not: %s' % on_off)

    def curr_slew(self, **values) -> tuple:
        """
            设置电流上升下降斜率
        :param values: (type dict): 字典说明
                slew (type int): 上升和下降斜率
                fall (type int): 下降斜率
                rise (type int): 上升斜率
                注意: 如果字典中包含slew, 则fall和rise的值忽略
        :return:
            (type int): 上升斜率, (type int): 下降斜率
        """
        slew = values.get(SLEW)
        if slew is not None:
            self.__rise_slew_set(slew)
            self.__fall_slew_set(slew)
        else:
            rise = values.get(RISE)
            if rise is not None:
                self.__rise_slew_set(rise)
            fall = values.get(FALL)
            if fall is not None:
                self.__fall_slew_set(fall)
        rise_data = self.query([It8500PlusCmd.RISE_SLEW_GET, ])
        fall_data = self.query([It8500PlusCmd.FALL_SLEW_GET, ])
        rise_slew = utils.hex_to_value(rise_data[3:7], magnif=10000)
        fall_slew = utils.hex_to_value(fall_data[3:7], magnif=10000)
        self._logger.info('current rise slew is: %d, fall slew is: %d', rise_slew, fall_slew)
        return rise_slew, fall_slew

    def __rise_slew_set(self, rise_slew):
        """上升斜率设置"""
        self.write(
            _value_command(op=It8500PlusCmd.RISE_SLEW_SET, value=rise_slew, endian='little', size=4, magnif=10000))

    def __fall_slew_set(self, fall_slew):
        """下降斜率设置"""
        self.write(
            _value_command(op=It8500PlusCmd.FALL_SLEW_SET, value=fall_slew, endian='little', size=4, magnif=10000))


def _value_command(op, value, endian='little', size=4, magnif=1000):
    """辅助方法"""
    if op is None or value is None:
        return
    cmd = [*op]
    cmd.extend(utils.value_to_hex(value, endian, size, magnif))

    return cmd
