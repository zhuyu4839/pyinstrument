# -*- encoding: utf-8 -*-
from constants import TUPLE_ON, TUPLE_OFF, ON
from errors import ParamException
from instrument import utils
from instrument.frame import FrameInstrument
from .ainuo_const import An8721pCmd

__all__ = {
    'An8721pFrame',
}


class An8721pFrame(FrameInstrument):
    """
    Ainuo power meter model AN8721P
    """

    def __init__(self, resource_name, address=1, baudrate=9600, timeout=0.15):
        assert 0 < address < 255
        assert baudrate in An8721pCmd.BAUDRATE_TUPLE
        super().__init__(resource_name, address, baudrate, timeout,
                         An8721pCmd.BAUDRATE_TUPLE, An8721pCmd.RW_DELAY_TUPLE)

    def idn(self):
        return 'AN8721P'

    def remote(self, on_off):
        """
        Override(远程操作开关)
        :param on_off: (type str) 可选值 {ON|1|OFF|0}
        :return:
            如果指令执行成功返回True,否则返回False
        """
        if on_off in TUPLE_ON:
            param = (0x01, )
        elif on_off in TUPLE_OFF:
            param = (0x00, )
        else:
            raise ParamException('not support parameter %s' % on_off)
        resp = self.query(self.__cmd(An8721pCmd.KEY_LOCK, param))
        return An8721pCmd.SUCCESS == self.__parse_resp(resp, 1)

    def start(self):
        """
        启动测量, 相当于按前面板的Start键
        :return:
            执行成功返回True, 否则返回False
        """
        resp = self.query(self.__cmd(An8721pCmd.START))
        return An8721pCmd.SUCCESS == self.__parse_resp(resp, 1)

    def stop(self):
        """
        停止测量, 相当于按前面板的Stop键
        :return:
            执行成功返回True, 否则返回False
        """
        resp = self.query(self.__cmd(An8721pCmd.STOP))
        return An8721pCmd.SUCCESS == self.__parse_resp(resp, 1)

    def clear(self):
        """
        清除测量值
        :return:
            执行成功返回True, 否则返回False
        """
        resp = self.query(self.__cmd(An8721pCmd.CLEAR))
        return An8721pCmd.SUCCESS == self.__parse_resp(resp, 1)

    def params_query(self, *names):
        """
        查询测量结果
        :param names:
            (type tuple): 可选查询值为:
                'nor': 查询所有常规测量值, 当name中包含该参数后, 执行完此查询立即返回
                'volt': 查询电压值
                'curr': 查询电流值
                'act_p': 查询有功功率值
                'app_p': 查询视在功率值
                'react_p': 查询无功功率值
                'p_fact': 查询功率因数值
                'ang': 查询角度值
                'freq': 查询频率值
                'ene_t': 查询电能量时间
                'ene': 查询电能量
                'et_thr': 查询电能量时间(达到门限后)

        :return:
            (type tuple or list):
                当names中包含'nor', 返回值为 电压 电流 功率 功率因素 频率 时间 电能量 依次组成的tuple
                否则返回以names中的值为顺序的查询值组成的list
        """
        if 'nor' in names:
            resp = self.query(An8721pCmd.NORMALS)
            return utils.hex_to_value(resp[6:10], endian=utils.BIG_ENDIAN, magnif=100), \
                utils.hex_to_value(resp[10:14], endian=utils.BIG_ENDIAN, magnif=10000), \
                utils.hex_to_value(resp[14:22], endian=utils.BIG_ENDIAN, magnif=1000), \
                utils.hex_to_value(resp[22:25], endian=utils.BIG_ENDIAN, magnif=1000), \
                utils.hex_to_value(resp[25:28], endian=utils.BIG_ENDIAN, magnif=1000), \
                utils.hex_to_value(resp[28:32], endian=utils.BIG_ENDIAN, magnif=1), \
                utils.hex_to_value(resp[32:40], endian=utils.BIG_ENDIAN, magnif=100)
        result = []
        for name in names:
            resp = self.query(An8721pCmd.QUERY_DICT.get(name))
            result.append(self.__parse_resp(resp, magnif=An8721pCmd.MAGNIFY_DICT.get(name)))
        return result

    def warning_buzzer(self, on_off):
        """
        设置报警蜂鸣器开关
        :param on_off: 可选值为 {ON|1|OFF|0}
        :return:
            如果指令执行成功返回True,否则返回False
        """
        if on_off in TUPLE_ON:
            param = (0x00,)
        elif on_off in TUPLE_OFF:
            param = (0x01,)
        else:
            raise ParamException('not support parameter: %s' % on_off)
        resp = self.query(self.__cmd(An8721pCmd.WARNING_BUZZER, param))
        return An8721pCmd.SUCCESS == self.__parse_resp(resp, 1)

    def warning_all_setting(self, group, volt_up, volt_low, volt_thr, curr_up, curr_low, curr_thr,
                            pow_up, pow_low, pow_thr, delay):
        """
        设置所有的报警参数(所有参数均应该设置合理值)
        :param group: (type int): 报警组号
        :param volt_up: (type float): 电压报警上限, 单位V
        :param volt_low: (type float): 电压报警下限, 单位V
        :param volt_thr: (type float): 电压报警门限, 单位V
        :param curr_up: (type float): 电流报警上限, 单位A
        :param curr_low: (type float): 电流报警下限, 单位A
        :param curr_thr: (type float): 电流报警门限, 单位A
        :param pow_up: (type float): 功率报警上限, 单位W
        :param pow_low: (type float): 功率报警下限, 单位W
        :param pow_thr: (type float): 功率报警门限, 单位W
        :param delay: (type float): 报警延时, 单位S
        :return:
            如果指令执行成功返回True,否则返回False
        """
        param = []
        param.extend(utils.value_to_hex(value=group, endian=utils.BIG_ENDIAN, size=1, magnif=1))
        param.extend(utils.value_to_hex(value=volt_up, endian=utils.BIG_ENDIAN, size=2, magnif=100))
        param.extend(utils.value_to_hex(value=volt_low, endian=utils.BIG_ENDIAN, size=2, magnif=100))
        param.extend(utils.value_to_hex(value=volt_thr, endian=utils.BIG_ENDIAN, size=2, magnif=100))
        param.extend(utils.value_to_hex(value=curr_up, endian=utils.BIG_ENDIAN, size=2, magnif=1000))
        param.extend(utils.value_to_hex(value=curr_low, endian=utils.BIG_ENDIAN, size=2, magnif=1000))
        param.extend(utils.value_to_hex(value=curr_thr, endian=utils.BIG_ENDIAN, size=2, magnif=1000))
        param.extend(utils.value_to_hex(value=pow_up, endian=utils.BIG_ENDIAN, size=3, magnif=100))
        param.extend(utils.value_to_hex(value=pow_low, endian=utils.BIG_ENDIAN, size=3, magnif=100))
        param.extend(utils.value_to_hex(value=pow_thr, endian=utils.BIG_ENDIAN, size=3, magnif=100))
        param.extend(utils.value_to_hex(value=delay, endian=utils.BIG_ENDIAN, size=1, magnif=10))

        resp = self.query(self.__cmd(An8721pCmd.WARNING_PARAMETERS, param))
        return An8721pCmd.SUCCESS == self.__parse_resp(resp, 1)

    def warning_setting(self, group=None, volt_up=None, volt_low=None, volt_thr=None, curr_up=None, curr_low=None,
                        curr_thr=None, pow_up=None, pow_low=None, pow_thr=None, delay=None):
        """
        设置报警参数
        :param group: (type int): 报警组号
        :param volt_up: (type float): 电压报警上限, 单位V
        :param volt_low: (type float): 电压报警下限, 单位V
        :param volt_thr: (type float): 电压报警门限, 单位V
        :param curr_up: (type float): 电流报警上限, 单位A
        :param curr_low: (type float): 电流报警下限, 单位A
        :param curr_thr: (type float): 电流报警门限, 单位A
        :param pow_up: (type float): 功率报警上限, 单位W
        :param pow_low: (type float): 功率报警下限, 单位W
        :param pow_thr: (type float): 功率报警门限, 单位W
        :param delay: (type float): 报警延时, 单位S
        :return:
            (type int): 设置成功参数的个数
        """
        count = 0
        if group is not None:
            param = (utils.value_to_hex(value=group, endian=utils.BIG_ENDIAN, size=1, magnif=1))
            res = self.query(self.__cmd(An8721pCmd.WARNING_GROUP, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning group failed')
        if volt_up is not None:
            param = (utils.value_to_hex(value=volt_up, endian=utils.BIG_ENDIAN, size=2, magnif=100))
            res = self.query(self.__cmd(An8721pCmd.WARNING_VOLTAGE_UPPER, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning voltage upper failed')
        if volt_low is not None:
            param = (utils.value_to_hex(value=volt_low, endian=utils.BIG_ENDIAN, size=2, magnif=100))
            res = self.query(self.__cmd(An8721pCmd.WARNING_VOLTAGE_LOWER, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning voltage lower failed')
        if volt_thr is not None:
            param = (utils.value_to_hex(value=volt_thr, endian=utils.BIG_ENDIAN, size=2, magnif=100))
            res = self.query(self.__cmd(An8721pCmd.WARNING_VOLTAGE_THRESHOLD, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning voltage threshold failed')
        if curr_up is not None:
            param = (utils.value_to_hex(value=curr_up, endian=utils.BIG_ENDIAN, size=2, magnif=1000))
            res = self.query(self.__cmd(An8721pCmd.WARNING_CURRENT_UPPER, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning current upper failed')
        if curr_low is not None:
            param = (utils.value_to_hex(value=curr_low, endian=utils.BIG_ENDIAN, size=2, magnif=1000))
            res = self.query(self.__cmd(An8721pCmd.WARNING_CURRENT_LOWER, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning current lower failed')
        if curr_thr is not None:
            param = (utils.value_to_hex(value=curr_thr, endian=utils.BIG_ENDIAN, size=2, magnif=1000))
            res = self.query(self.__cmd(An8721pCmd.WARNING_CURRENT_THRESHOLD, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning current threshold failed')
        if pow_up is not None:
            param = (utils.value_to_hex(value=pow_up, endian=utils.BIG_ENDIAN, size=2, magnif=100))
            res = self.query(self.__cmd(An8721pCmd.WARNING_POWER_UPPER, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning power upper failed')
        if pow_low is not None:
            param = (utils.value_to_hex(value=pow_low, endian=utils.BIG_ENDIAN, size=2, magnif=100))
            res = self.query(self.__cmd(An8721pCmd.WARNING_POWER_LOWER, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning power lower failed')
        if pow_thr is not None:
            param = (utils.value_to_hex(value=pow_thr, endian=utils.BIG_ENDIAN, size=2, magnif=100))
            res = self.query(self.__cmd(An8721pCmd.WARNING_POWER_THRESHOLD, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning power threshold failed')
        if delay is not None:
            param = (utils.value_to_hex(value=delay, endian=utils.BIG_ENDIAN, size=1, magnif=10))
            res = self.query(self.__cmd(An8721pCmd.WARNING_DELAY, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set warning delay time failed')
        return count

    def normal_all_setting(self, volt_r, curr_r, calc_m, calc_p, volt_ratio, curr_ratio, curr_thr,
                           e_time, buzzer=ON):
        """
        设置所有常规参数值(所有参数均应该设置合理值)
        :param volt_r: (type int): 电压量程, 范围0-4, 0: LOW 档，1: HI 档，2: 保留，3: 保留，4: 自动
        :param curr_r: (type int): 电流量程, 范围0-4, 0: LOW 档，1: HI 档，2: 保留，3: 保留，4: 自动
        :param calc_m: (type int): 计算模式, 范围0-2; 0: RMS，1: DC，2: MEAN
        :param calc_p: (type int): 计算周期, 范围 0-2，0: 0.25(S)，1: 0.5(S)，2: 1.0(S)
        :param volt_ratio: (type float): 电压变比, 范围0-1000
        :param curr_ratio: (type float): 电流变比, 范围1-1000
        :param curr_thr: (type float): 电能量累积电流门限, 范围1-22, 单位A
        :param e_time: (type float): 电能量计时时间, 范围0-35999940, 单位S
        :param buzzer: (type str): 蜂鸣器开关, 可选值为{ON|1|OFF|0}, 默认值为ON
        :return:
            如果指令执行成功返回True,否则返回False
        """
        param = []
        param.extend(utils.value_to_hex(value=volt_r, endian=utils.BIG_ENDIAN, size=1, magnif=1))
        param.extend(utils.value_to_hex(value=curr_r, endian=utils.BIG_ENDIAN, size=1, magnif=1))
        param.extend(utils.value_to_hex(value=calc_m, endian=utils.BIG_ENDIAN, size=1, magnif=1))
        param.extend(utils.value_to_hex(value=calc_p, endian=utils.BIG_ENDIAN, size=1, magnif=1))
        param.extend(utils.value_to_hex(value=volt_ratio, endian=utils.BIG_ENDIAN, size=2, magnif=10))
        param.extend(utils.value_to_hex(value=curr_ratio, endian=utils.BIG_ENDIAN, size=2, magnif=10))
        param.extend(utils.value_to_hex(value=curr_thr, endian=utils.BIG_ENDIAN, size=2, magnif=1000))
        param.extend(utils.value_to_hex(value=e_time, endian=utils.BIG_ENDIAN, size=4, magnif=1))
        param.extend(utils.value_to_hex(value=1 if buzzer in TUPLE_ON else 0 if buzzer in TUPLE_OFF
                                        else utils.raiser(ParamException('Parameter buzzer expect {ON|1|OFF|0}')),
                                        endian=utils.BIG_ENDIAN, size=1, magnif=1))

        resp = self.query(self.__cmd(An8721pCmd.PARAMETERS, param))
        return An8721pCmd.SUCCESS == self.__parse_resp(resp, 1)

    def normal_setting(self, volt_r=None, curr_r=None, calc_m=None, calc_p=None, volt_ratio=None,
                       curr_ratio=None, curr_thr=None, e_time=None):
        """
        设置常规参数值
        :param volt_r: (type int): 电压量程, 范围0-4, 0: LOW 档，1: HI 档，2: 保留，3: 保留，4: 自动
        :param curr_r: (type int): 电流量程, 范围0-4, 0: LOW 档，1: HI 档，2: 保留，3: 保留，4: 自动
        :param calc_m: (type int): 计算模式, 范围0-2; 0: RMS，1: DC，2: MEAN
        :param calc_p: (type int): 计算周期, 范围 0-2，0: 0.25(S)，1: 0.5(S)，2: 1.0(S)
        :param volt_ratio: (type float): 电压变比, 范围0-1000
        :param curr_ratio: (type float): 电流变比, 范围1-1000
        :param curr_thr: (type float): 电能量累积电流门限, 范围1-22, 单位A
        :param e_time: (type float): 电能量计时时间, 范围0-35999940, 单位S
        :return:
            (type int): 设置成功参数的个数
        """
        count = 0
        if volt_r is not None:
            param = (utils.value_to_hex(value=volt_r, endian=utils.BIG_ENDIAN, size=1, magnif=1))
            res = self.query(self.__cmd(An8721pCmd.VOLTAGE_RANGE, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set voltage range failed')
        if curr_r is not None:
            param = (utils.value_to_hex(value=curr_r, endian=utils.BIG_ENDIAN, size=1, magnif=1))
            res = self.query(self.__cmd(An8721pCmd.CURRENT_RANGE, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set current range failed')
        if calc_m is not None:
            param = (utils.value_to_hex(value=calc_m, endian=utils.BIG_ENDIAN, size=1, magnif=1))
            res = self.query(self.__cmd(An8721pCmd.CALCULATION_MODE, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set calculator model failed')
        if calc_p is not None:
            param = (utils.value_to_hex(value=calc_p, endian=utils.BIG_ENDIAN, size=1, magnif=1))
            res = self.query(self.__cmd(An8721pCmd.CALCULATION_PERIOD, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set calculator period failed')
        if volt_ratio is not None:
            param = (utils.value_to_hex(value=volt_ratio, endian=utils.BIG_ENDIAN, size=2, magnif=10))
            res = self.query(self.__cmd(An8721pCmd.VOLTAGE_RATIO, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set voltage ratio failed')
        if curr_ratio is not None:
            param = (utils.value_to_hex(value=curr_ratio, endian=utils.BIG_ENDIAN, size=2, magnif=10))
            res = self.query(self.__cmd(An8721pCmd.CURRENT_RATIO, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set current ratio failed')
        if curr_thr is not None:
            param = (utils.value_to_hex(value=curr_thr, endian=utils.BIG_ENDIAN, size=2, magnif=1000))
            res = self.query(self.__cmd(An8721pCmd.CURRENT_THRESHOLD, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set current threshold failed')
        if e_time is not None:
            param = (utils.value_to_hex(value=e_time, endian=utils.BIG_ENDIAN, size=4, magnif=1))
            res = self.query(self.__cmd(An8721pCmd.TIME, param))
            if An8721pCmd.SUCCESS == res:
                count += 1
            else:
                self._logger.warn('set energy calculator time failed')
        return count

    def zero_threshold(self, on_off):
        """
        设置零值门限开关
        :param on_off: (type str): 可选值为 {ON|1|OFF|0}
        :return:
            如果指令执行成功返回True,否则返回False
        """
        if on_off in TUPLE_ON:
            param = (0x00,)
        elif on_off in TUPLE_OFF:
            param = (0x01,)
        else:
            raise ParamException('not support parameter: %s' % on_off)
        resp = self.query(self.__cmd(An8721pCmd.ZERO_THRESHOLD, param))
        return An8721pCmd.SUCCESS == self.__parse_resp(resp, 1)

    def volt_shield(self, volt):
        """
        设置电压屏蔽值
        :param volt: (type float): 电压值, 范围0-36, 单位V
        :return:
            如果指令执行成功返回True,否则返回False
        """
        resp = self.query(self.__cmd(An8721pCmd.VOLTAGE_SHIELD,
                                     utils.value_to_hex(volt, endian=utils.BIG_ENDIAN, size=3, magnif=100)))
        return An8721pCmd.SUCCESS == self.__parse_resp(resp, 1)

    def curr_shield(self, curr):
        """
        设置电流屏蔽值
        :param curr: (type float): 电压值, 范围0-100, 单位mA
        :return:
            如果指令执行成功返回True,否则返回False
        raise:
            IOException
        """
        resp = self.query(self.__cmd(An8721pCmd.CURRENT_SHIELD,
                                     utils.value_to_hex(curr, endian=utils.BIG_ENDIAN, size=2, magnif=1)))
        return An8721pCmd.SUCCESS == self.__parse_resp(resp, 1)

    def __cmd(self, cmd, param=None):
        """构建命令"""
        param_len = 0 if param is None else len(param)
        length = param_len + 8
        res = [0x7b, ]
        res.extend(utils.value_to_hex(length, endian=utils.BIG_ENDIAN, size=2, magnif=1))
        res.append(self._address)
        res.extend(cmd)
        res.extend(param if param is not None else ())
        count = 0
        for i in range(len(res) - 1):
            count = count + res[i + 1]
        res.extend(utils.value_to_hex(value=count, endian=utils.BIG_ENDIAN, size=1, magnif=1))
        res.append(0x7d)
        return res

    def __parse_resp(self, resp, magnif=1):
        """解析结果"""
        length = len(resp)
        start = 6
        end = length - 2
        if end < start:
            raise IOError()
        result = utils.hex_to_value(resp[start:end], utils.BIG_ENDIAN, magnif)
        self._logger.info('Execute command result: %s', result)
        return result



















