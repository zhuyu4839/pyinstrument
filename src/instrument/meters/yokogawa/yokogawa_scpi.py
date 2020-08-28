# -*- encoding: utf-8 -*-
import time

from constants import TUPLE_ON_OFF
from errors import InstrumentError
from instrument import utils
from instrument.const import Ieee488Cmd, EMPTY, COMMAS
from .yokogawa_scpi_const import Wt310eCmd
from instrument.scpi import ScpiInstrument

__all__ = {
    'Wt310eScpi',
}


class Wt310eScpi(ScpiInstrument):
    """
    for WT310E/WT310EH/WT332E/WT333E Digital Power Meter
    """
    def __init__(self, resource_name, timeout=0):
        super().__init__(resource_name, timeout)

    def remote(self, on_off=None):
        if on_off in TUPLE_ON_OFF:
            return self.communicate_group('remote', remote=on_off)
        return self.communicate_group('remote')

    def tst(self):
        """
        自检测试, (*TST命令为耗时操作)
        :return: 自检测试状态, 非0为不通过, 具体查看仪器定义
        """
        self.write(Ieee488Cmd.TST)
        time.sleep(6)
        return self.query()

    # aoutput group

    def aoutput_group(self):
        """
        无硬件(/DA4 or /DA12)支持, 暂时未实现
        @return:
            None
        """
        raise InstrumentError('no /DA4 or /DA12 hardware supported')

    # end of aoutput group

    # communicate group

    def communicate_group(self, *names, **values):
        """
        仪器通讯参数的查询与设置
        @param names: (type tuple): 可选值如下:
            header: 是否在查询值前添加头
            lockout: 本地操作锁定
            remote: 本地操作模式和远程操作模式
            status: 返回特定行的状态
                返回值位的含义如下:
                    bit0: RS-232通讯校验错误
                    bit1: RS-232通讯帧错误
                    bit2: RS-232断字符错误
                    bit3 and higher: 始终为0
            verbose: 响应是否以完全拼写形式或缩写形式返回
            wait: 等待指定的扩展事件发生
        @param values: (type dict): 键值说明如下:
            header: (type str) 是否在查询值前添加头, 可选值 {ON|1|OFF|0}
            lockout: (type str) 是否本地操作锁定, 可选值 {ON|1|OFF|0}
            remote: (type str) 本地操作模式和远程操作模式切换, 可选值 {ON|1|OFF|0}
            verbose: (type str) 响应是否以完全拼写形式或缩写形式返回, 可选值 {ON|1|OFF|0}
            wait: (type int) 等待指定的扩展事件发生, 选值范围 0 to 65535, 详细参考官方文档
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values.items():
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_COMMUNICATE_SET.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_COMMUNICATE_GET.get(name))
        return self.query(query_cmd)

    # end of communicate group

    def display_group(self, *names, **values):
        """
        显示相关操作设置和查询
        @param names: (type tuple) 可选值如下:
            normals: 所有通用测量数据显示设置信息
            harmonics: 所有谐波测量数据显示设置信息
        @param values: (type dict), 字典说明如下:
                normal1: (type dict), 字典说明如下:
                        func: (type str), 可选值 {U|I|P|S|Q|TIME}
                        el: (type int), 当func为TIME时, el必须为None
                normal2: (type dict), 字典说明如下:
                        func: (type str), 可选值 {U|I|P|LAMB|PHI}
                normal3: (type dict), 字典说明如下:
                        func: (type str), 可选值 {U|I|P|UPP|UMP|IPP|IMP|PPP|PMP|WH|WHP|WHM|AH|AHP|AHM|MATH}
                        el: (type int), 当func为MATH时, el必须为None
                normal4: (type dict), 字典说明如下:
                        func: (type str), 可选值 {U|I|P|LAMB|FU|FI|UTHD|ITHD}
                harmonic1: (type dict), 字典说明如下:
                        func: (type str), 可选值 {ORD|U|I|P}
                        el: (type int), 当func为ORD时, el必须为None
                harmonic2: (type dict), 字典说明如下:
                        func: (type str), 可选值 {U|I|P|PHIU|PHII|UHDLF|IHDF|PHDF}
                harmonic3: (type dict), 字典说明如下:
                        func: (type str), 可选值 {U|I|P}
                harmonic4: (type dict), 字典说明如下:
                        func: (type str), 可选值 {U|I|P|LAMB|FU|FI|UTHD|ITHD}
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        for key, value in values.items():
            func = value.get('func')
            el = value.get('el')
            assert func is not None
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_DISPLAY_SET.get(key), func,
                                               COMMAS if el is not None else EMPTY,
                                               el if el is not None else EMPTY)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_DISPLAY_GET.get(name))
        return self.query(query_cmd)

    def harmonics_group(self, *names, **values):
        """
        谐波测量相关操作设置查询
        @param names: (type tuple) 可选值如下:
            measures: 所有谐波测量相关值, 包含PLL源, 分析的最大和最小谐波阶数, 用于计算THD(总谐波失真)的方程式,
            display: 所有显示谐波测量设置值, 包含显示状态和显示屏B中显示的谐波分量谐波测量数据的谐波阶次
        @param values: (type dict) 字典说明如下:
            harm_plls: (type str) 设置PLL源,可选值 {U1|U2|U3|I1|I2|I3}
            harm_order: (type str) 析的最大和最小谐波阶数
                    应为如 value1,value2的字符串, value1和value2范围1 to 50
            harm_thd: (type str) 用于计算THD(总谐波失真)的方程式
                    可选值 {TOTal|FUNDamental}
            disp_state: (type str) 显示状态
                    可选值 {ON|1|OFF|0}
            disp_order: (type int) 显示屏B中显示的谐波分量谐波测量数据的谐波阶次
                    范围 1 to 50 (harmonic order)
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values.items():
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_HARMONIC_SET.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_HARMONIC_GET.get(name))
        return self.query(query_cmd)

    def hold(self, on_off=None):
        """
        设置或查询输出保持功能的开/关状态,以进行显示,通信和其他类型的数据
        @param on_off: (type str)
            可选值 {ON|1|OFF|0}或None
        @return:
            保持功能的状态 '0\n'或'1\n'
        """
        if on_off in TUPLE_ON_OFF:
            self.write(':HOLD ?', on_off)
        # response ":HOLD 0\n" or ":HOLD 1\n"
        return self.query(':HOLD?')

    def input_voltage(self, *names, **values):
        """
        设置和查询电压测量的相关设置
        @param names: (type tuple) 可选值如下:
                range: 电压量程
                auto: 自动电压量程状态
                conf: 有效电压量程值
                poj: 出现电压峰值超范围时使用的跳转目标范围
        @param values: (type dict) 字典说明如下:
                range: (type float) 设置电压量程值
                    • 当波峰因数(crest factor)设置为3时
                        电压量程可选值 15, 30, 60, 150, 300, 600(V)
                    • 当波峰因数(crest factor)设置为6或6A时
                        电压量程可选值 7.5, 15, 30, 75, 150, 300(V)
                auto: (type str) 自动电压量程
                        可选值 {ON|1|OFF|0}
                conf: (type str) 有效电压量程设置
                        如此格式的字符串 {ALL|<Voltage>[,<Voltage>][,<Voltage>]...}
                poj: (type str) 出现电压峰值超范围时使用的跳转目标范围
                        可选值 {OFF|<Voltage>}, <Voltage>范围参考range
        return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values.items():
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_INPUT_VOLTAGE_SET.get(key), value)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_INPUT_VOLTAGE_GET.get(name))
        return self.query(query_cmd)

    def input_current(self, *names, **values):
        """
        设置和查询电流测量的相关设置
        注意: ext_conf, ext_poj, ratio, ratio_el1, ratio_el2, ratio_el3等几个参数仅安装了可选外部电流传感器(/EX1 or /EX2)时有效
        @param names: (type tuple) 可选值说明如下:
            range: 电流量程
            auto: 自动电流量程状态
            conf: 有效电流量程
            poj: 发生当前峰值超范围时使用的跳转目标范围
            ext_conf: 外部电流传感器有效量程
            ext_poj: 外部电流传感器发生当前峰值超范围时使用的跳转目标范围
            ratio: 外部电流传感器所有元件的转换率
            ratio_el1: 指定元素1的外部电流传感器转换率
            ratio_el2: 指定元素2的外部电流传感器转换率
            ratio_el3: 指定元素3的外部电流传感器转换率
        @param values: (type dict) 字典说明如下:
            range: (type float) 电流量程
                • 对于内部电流表而言
                    • 当波峰因数(crest factor)设置为3时, 范围说明如下:
                    <Current> = 5, 10, 20, 50, 100, 200, 500(mA),
                    1, 2, 5, 10, 20(A) (WT310E)
                    <Current> = 1, 2, 5, 10, 20, 40(A) (WT310EH)
                    <Current> = 0.5, 1, 2, 5, 10, 20(A) (WT332E, WT333E)
                    • 当波峰因数(crest factor)设置为6或6A时, 范围说明如下:
                    <Current> = 2.5, 5, 10, 25, 50, 100, 250(mA),
                                0.5, 1, 2.5, 5, 10(A) (WT310E)
                    <Current> = 0.5, 1, 2.5, 5, 10, 20(A) (WT310EH)
                    <Current> = 0.25, 0.5, 1, 2.5, 5, 10(A) (WT332E, WT333E)
                • 对于内部电流表而言
                    • 当波峰因数(crest factor)设置为3时, 范围说明如下:
                    <Voltage> = 2.5, 5, 10(V) (/EX1)
                    <Voltage> = 50, 100, 200, 500(mV), 1, 2(V) (/EX2)
                    • 当波峰因数(crest factor)设置为6或6A时, 范围说明如下:
                    <Voltage> = 1.25, 2.5, 5(V) (/EX1)
                    <Voltage> = 25, 50, 100, 250(mV), 0.5, 1(V) (/EX2)
            auto: (type str) 自动电流量程状态
                可选值 {ON|1|OFF|0}
            conf: (type str) 有效电流量程(内部电流表)
                如此格式的字符串 {ALL|<Current>[,<Current>][,<Current>]...}
            poj: (type str or float) 发生当前峰值超范围时使用的跳转目标范围
                可选值 {OFF|<Current>}, <Current>参考range参数
            ext_conf: (type str) 有效电流量程(外部电流表)
                如此格式的字符串 {ALL|<Current>[,<Current>][,<Current>]...}, <Current>参考range参数
            ext_poj: (type str) 发生当前峰值超范围时使用的跳转目标范围(外部电流表)
                可选值 {OFF|<Current>}, <Current>参考range参数
            ratio: (type float) 外部电流传感器所有元件的转换率
                值范围 0.001 to 9999.
            ratio_el1: (type float) 指定元素1的外部电流传感器转换率
                值范围 0.001 to 9999.
            ratio_el2: (type float) 指定元素2的外部电流传感器转换率
                值范围 0.001 to 9999.
            ratio_el3: (type float) 指定元素3的外部电流传感器转换率
                值范围 0.001 to 9999.
        return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values:
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_INPUT_CURRENT_SET.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_INPUT_CURRENT_GET.get(name))
        return self.query(query_cmd)

    def input_scaling(self, *names, **values):
        """
        设置和查询扫描设置相关参数
        @param names: (type tuple) 可选值如下:
                state: 扫描状态开关
                vt: 所有元素VT(电压与时间)比
                ct: 所有元素CT(电流与时间)比
                factor: 所有元素的功率系数
                vt_el1: 元素1的VT(电压与时间)比
                vt_el2: 元素2的VT(电压与时间)比
                vt_el3: 元素3的VT(电压与时间)比
                ct_el1: 元素1的CT(电流与时间)比
                ct_el2: 元素2的CT(电流与时间)比
                ct_el3: 元素3的CT(电流与时间)比
                factor_el1: 元素1的功率系数
                factor_el2: 元素2的功率系数
                factor_el3: 元素3的功率系数
        @param values: (type dict) 字典说明如下:
                state: (type str) 扫描状态开关
                    可选值 {ON|1|OFF|0}
                vt: (type float) 所有元素VT(电压与时间)比
                    可选范围 0.001 to 9999.
                ct: 所有元素CT(电流与时间)比
                    可选范围 0.001 to 9999.
                factor: 所有元素的功率系数
                    可选范围 0.001 to 9999.
                vt_el1: 元素1的VT(电压与时间)比
                    optional value range 0.001 to 9999.
                vt_el2: 元素2的VT(电压与时间)比
                    可选范围 0.001 to 9999.
                vt_el3: 元素3的VT(电压与时间)比
                    可选范围 0.001 to 9999.
                ct_el1: 元素1的CT(电流与时间)比
                    可选范围 0.001 to 9999.
                ct_el2: 元素2的CT(电流与时间)比
                    可选范围 0.001 to 9999.
                ct_el3: 元素3的CT(电流与时间)比
                    可选范围 0.001 to 9999.
                factor_el1: 元素1的功率系数
                    可选范围 0.001 to 9999.
                factor_el2: 元素2的功率系数
                    可选范围 0.001 to 9999.
                factor_el3: 元素3的功率系数
                    可选范围 0.001 to 9999.
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values:
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_INPUT_SCALING_SET.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_INPUT_SCALING_GET.get(name))
        return self.query(query_cmd)

    def input_filter(self, **values):
        """
        设置和查询输入过滤开关
        @param values: (type dict) 字典说明如下:
            line: (type str) 线性过滤开关
                可选值 {ON|1|OFF|0}
            freq: (type str) 频率过滤开关
                可选值 {ON|1|OFF|0}
        @return:
            依次返回线性过滤和频率过滤开关状态, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values:
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_INPUT_FILTER_SET.get(key), value)
        self.write(write_cmd)

        return self.query(':INPut:FILTer?')

    def input_others(self, *names, **values):
        """
        查询和设置其他输入参数
        @param names: (type tuple)
                crest_fac: 波峰因数
                wiring: 接线系统
                mode: 电压和电流测量模式
                rconf: 范围配置（有效范围选择）功能的开/关状态
                sync: 同步源
                peak_over: 峰值超范围信息, 返回值每位含义如下:
                -----------------------------------------
                | 7  | 6  | 5  | 4  | 3  | 2  | 1  | 0  |
                |    |    | I3 | U3 | I2 | U2 | I1 | U1 |
                -----------------------------------------
                check_range: 量程状态, 返回值每位含义如下:
                -----------------------------------------
                | 7  | 6  | 5  | 4  | 3  | 2  | 1  | 0  |
                | AP | AO | AH | AL | VP | VO | VH | VL |
                -----------------------------------------
                VL : 电压处于减小自动量程或更小的条件
                VH : 电压超出了提高自动量程的条件
                VO : 电压超量程
                VP : 电压峰值超量程
                AL : 电流处于减小自动量程或更小的条件
                AH : 电流超出了提高自动量程的条件
                AO : 电流超量程
                AP : 电流峰值超量程
        @param values: (type dict) 字典说明如下:
                crest_fac: (type str) 波峰因数
                    可选值 {3|6|A6}
                wiring: 接线系统
                    可选值 {(P1W2|P1W3|P3W3|P3W4|V3A3)}
                mode: 电压和电流测量模式
                    可选值 {RMS|VMEan|DC}
                rconf: 范围配置（有效范围选择）功能的开/关状态
                    可选值 {ON|1|OFF|0}
                sync: 同步源
                    可选值 {VOLTage|CURRent|OFF}
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values:
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_INPUT_OTHERS_SET.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_INPUT_OTHERS_GET.get(name))
        return self.query(query_cmd)

    # start integrate
    def integrate_group(self, *names, **values):
        """
        设置和查询积分相关参数
        @param names: (type tuple) 可选值说明如下:
            mode: 积分模式
            timer: 积分计时器
            state: 积分状态
        @param values: (type tuple) 字典说明如下:
            mode: (type str) 积分模式, 可选值 {NORMal|CONTinuous}
            timer: (type dict) 字典说明如下:
                hour: (type int) 小时位, 范围 0~10000, 默认0
                minute: (type int) 分钟位, 范围 0~59, 默认0
                second: (type int) 秒位, 范围 0~59, 默认0
            state: (type str) 积分状态
                可选值 {start|stop|reset}
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        mode = values.get('mode', None)
        if mode is not None:
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_INTEGRATE_SET.get('mode'), mode)
        timer = values.get('timer', None)
        if timer is not None:
            assert isinstance(timer, dict), 'timer must be a dict'
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_INTEGRATE_SET.get('timer'),
                                               timer.get('hour', 0), timer.get('minute', 0), timer.get('second', 0))
        state = values.get('state', None)
        if state is not None:
            if 'start' == state:
                write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_INTEGRATE.get('start'))
            elif 'stop' == state:
                write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_INTEGRATE.get('stop'))
            elif 'reset' == state:
                write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_INTEGRATE.get('reset'))
            else:
                self._logger.warn('the state "%s" expect "start", "stop" or "reset"', state)
        self.write(write_cmd)
        query_cmd = None
        if 'mode' in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_INTEGRATE.get('mode'))
        if 'timer' in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_INTEGRATE.get('timer'))
        if 'state' in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_INTEGRATE.get('state'))
        return self.query(query_cmd)

    # def mode(self, mode=None):
    #     """
    #     设置或查询积分模式
    #     @param mode: (type str) 集成模式, 可选值 {NORMal|CONTinuous}
    #     @return:
    #         (type str) 集成模式
    #     """
    #     if mode is not None:
    #         self.write(Wt310eCmd.DICT_INTEGRATE_SET.get('mode'), mode)
    #     return self.query(Wt310eCmd.DICT_INTEGRATE.get('mode'))
    #
    # def timer(self, hour=None, minute=None, second=None):
    #     """
    #     设置或查询积分计时器值
    #     @param hour: (type int) 小时位, 范围 0~10000
    #     @param minute: (type int) 分钟位, 范围 0~59
    #     @param second: (type int) 秒位, 范围 0~59
    #     @return:
    #         积分计时器值, 注意后面的换行字符'\n'
    #     """
    #     if hour is not None \
    #             or minute is not None \
    #             or second is not None:
    #         self.write(self.write(Wt310eCmd.DICT_INTEGRATE_SET.get('timer'),
    #                                 0 if hour is None else hour,
    #                                 0 if minute is None else minute,
    #                                 0 if second is None else second))
    #     return self.query(Wt310eCmd.DICT_INTEGRATE.get('timer'))
    #
    # def start(self):
    #     """
    #     Starts integration.
    #     return:
    #         None
    #     """
    #     self.write(Wt310eCmd.DICT_INTEGRATE.get('start'))
    #
    # def stop(self):
    #     """
    #     Stops integration.
    #     return:
    #         None
    #     """
    #     self.write(Wt310eCmd.DICT_INTEGRATE.get('stop'))
    #
    # def reset(self):
    #     """
    #     Resets the integrated value.
    #     return:
    #         None
    #     """
    #     self.write(Wt310eCmd.DICT_INTEGRATE.get('reset'))
    #
    # def state(self):
    #     """
    #     Queries the integration status.
    #     return:
    #         the integration status.
    #     """
    #     return self.query(Wt310eCmd.DICT_INTEGRATE.get('state'))
    # end of integrate

    def math(self, equation=None):
        """
        设置和查询用于计算的数学方程
        @param equation: (type str) 方程, 可选值 {EFFiciency|CFU(1-3)|CFI(1-3)|ADD|SUB|MUL|DIV|DIVA|DIVB|AVW(1-4))}
        @return:
            @type(str) 当前用于计算的数学方程, 注意后面的换行字符'\n'
        """
        if equation is not None:
            self.write(':MATH {}', equation)
        return self.query(':MATH?')

    def measure_group(self, **values):
        """
        设置和查询所有测量和数据输出计算相关参数
        @param values: (type dict) 字典说明如下:
                'state': 平均计算开关状态, 可选值 {ON|1|OFF|0}
                'type': 平均类型, 可选值 {LINear|EXPonent}
                    注意: 谐波测量功能（选件）的平均仅在类型设置为EXPonent(指数)时有效
                'count': 平均系数, 可选值 8, 16, 32, 64
                'max_hold': 最大值保持开关状态, 可选值 {ON|1|OFF|0}
        @return:
            依次返回state, type, count, max hold相关参数或状态值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values.items():
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_MEASURE_SET.get(key), value)
        self.write(write_cmd)

        return self.query(':MEASure?')

    def numeric_format(self, fmt=None):
        """
        设置和查询数字数据格式
        说明:
            • 输出的数字数据的格式因设置此命令的方式而异, 下面对不同的格式进行说明:
                (1) ASCii
                物理值以<NR3>(科学计数法)方式输出(仅经过的积分时间以<NR1>整数的格式输出).数据项之间用逗号分隔
                (2) FLOat
                在每个数字数据块的前面添加标题（例如: "＃240"或"＃3208"）.
                标头之后是IEEE单精度浮点（4字节）格式的物理值.
                各项数据的字节顺序是MSB在前
        @param fmt: (type str) 可选值 {ASCii|FLOat}, 功能参考说明
        @return:
            格式化数据, 注意后面的换行字符'\n'
        """
        if Wt310eCmd.REGEX_NUMERIC_FORMAT.match(fmt) is not None:
            self.write(Wt310eCmd.DICT_NUMERIC_SET.get('fmt'), fmt)
        return self.query(Wt310eCmd.DICT_NUMERIC_GET.get('fmt'))

    def numeric_normal(self, *names, **values):
        """
        设置和查询数字输出相关参数
        @param names: (type tuple):
                number: 查询由:NUMeric[:NORMal]:VALue?命令传输的数字数据项
                item<x>: 查询指定的数值数据输出项(功能，元素和谐波次数), <x>值为1-255
        @param values: (type dict):
                number: (type str or int) 设置由:NUMeric[:NORMal]:VALue?命令传输的数字数据项
                    可选值: {<NRf>|ALL}
                        <NRf> = 1 to 255(ALL)
                clear: (type str) 清除数字数据输出项目(将项目设置为NONE).
                    可选值/数据格式: {ALL|<NRf>[,<NRf>]}
                    ALL = Clear all items
                    First <NRf> = 1 to 255 (the number of the first item to clear)
                    Second <NRf> = 1 to 255 (the number of the last item to clear)
                delete: (type str) 删除数字数据输出项
                    数据格式: {<NRf>[,<NRf>]}
                    First <NRf> = 1 to 255 (the number of the first item to delete)
                    Second <NRf> = 1 to 255 (the number of the last item to delete)
                preset: (type int) 预设数值数据输出项目匹配
                    范围 1 to 4
                item<x>: (type str) 设置指定的数值数据输出项(功能，元素和谐波次数), <x>值为1-255
                    可选值/数据格式: {NONE|<Function>[,<Element>][,<Order>]}
                        NONE = No output item
                        <Function> = {U|I|P|S|Q|...}
                        <Element> = {<NRf>|SIGMa} (<NRf> = 1 to 3)
                        <Order> = {TOTal|DC|<NRf>} (<NRf> = 1 to 50)
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values.items():
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_NUMERIC_NORMAL_SET.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_NUMERIC_NORMAL_GET.get(name))
        return self.query(query_cmd)

    def numeric_normal_value(self, nrf=1):
        """
        查询数字数据头和数据值
        @param nrf: (type int) <NRf> = 1 to 255 (item number)
        @return:
            数字数据头和数据值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        # return self.query(':NUMeric:NORMal:HEADer? {};:NUMeric:NORMal:VALue? {}'.format(nrf, nrf))
        return self.query(utils.contact_spci_cmd(Wt310eCmd.DICT_NUMERIC_NORMAL_GET.get('header').format(nrf),
                                                 Wt310eCmd.DICT_NUMERIC_NORMAL_GET.get('value').format(nrf)))

    def numeric_list(self, *names, **values):
        """
        设置和查询谐波测量数字列表数据输出相关参数
        Sets or queries harmonic measurement numeric list data output settings.
        @param names: (type tuple), 可选值说明如下:
                number: 查询由:NUMeric:LIST:VALue?命令传送的数字列表数据项的数量
                order: 查询谐波测量数字列表数据的最大输出谐波阶数
                select: 查询谐波测量数字列表数据的输出分量
                item<x>: 查询指定谐波测量数字列表数据项的输出项(功能和元素), <x> = 1 to 32 (item number)
        @param values: (type dict) 字典说明如下:
                number: (type str or int) 设置由:NUMeric:LIST:VALue?命令传送的数字列表数据项的数量
                    可选值/范围: 1 to 32 or (ALL)
                order: (type str or int) 设置谐波测量数字列表数据的最大输出谐波阶数
                    可选值/范围: 1 to 50 or (ALL)
                select: (type str) 查询谐波测量数字列表数据的输出分量
                    可选值: {EVEN|ODD|ALL}
                preset: (type int) 预设谐波测量数值列表数据输出项目匹配
                    可选值范围: 1 to 4
                clear: (type str) 清除谐波测量数字列表数据输出项目(将项目设置为NONE)
                    可选值/格式: {ALL|<NRf>[,<NRf>]}
                    ALL = Clear all items
                    First <NRf> = 1 to 32 (the number of the first item to clear)
                    Second <NRf> = 1 to 32 (the number of the last item to clear)
                delete: (type str) 删除谐波测量数字列表数据输出项目
                    可选值/格式: {<NRf>[,<NRf>]}
                    First <NRf> = 1 to 32 (the number of the first item to delete)
                    Second <NRf> = 1 to 32 (the number of the last item to delete)
                item<x>: (type str) 指定谐波测量数字列表数据项的输出项功能和元素, <x> = 1 to 32 (item number)
                    可选值/格式: {NONE|<Function>,<Element>}
                    NONE = No output item
                    <Function> = {U|I|P|PHIU|PHII|UHDF|IHDF|PHDF}
                    <Element> = {<NRf>}(<NRf> = 1 to 3)
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values.items():
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_NUMERIC_LIST_SET.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_NUMERIC_LIST_GET.get(name))
        return self.query(query_cmd)

    def numeric_list_value(self, nrf=1):
        """
        查询谐波测量数值列表数据
        @param nrf: (type str) <NRf> = 1 to 32 (item number)
        @return:
            谐波测量数值列表数据, 注意后面的换行字符'\n'
        """
        return self.query(Wt310eCmd.DICT_NUMERIC_LIST_GET.get('value'), nrf)

    def numeric_hold(self, on_off=None):
        """
        设置和查询数字数据保持功能的开/关(保持/释放)状态
        @param on_off: (type str) 可选值 {ON|1|OFF|0}
        @return:
            数字数据保持功能的开/关(保持/释放)状态, 注意后面的换行字符'\n'
        """
        if on_off in TUPLE_ON_OFF:
            self.write(Wt310eCmd.DICT_NUMERIC_SET.get('hold'), on_off)
        return self.query(Wt310eCmd.DICT_NUMERIC_GET.get('hold'))

    def rate_group(self, *names, **values):
        """
        设置和查询处理数据更新间隔
        @param names: (type tuple) 可选值说明如下:
                time: 数据更新间隔
                auto: 数据更新间隔的状态设置为"auto"
                timeout: 数据更新间隔设置为"auto"的超时时间
                sync: 数据更新间隔设置为"auto"时的同步源
        @param values: (type dict) 字典说明如下:
                time: (type str or float) 数据更新间隔
                    可选值/格式 {AUTO|<NRf>(MS|S)}
                timeout: 数据更新间隔设置为"auto"的超时时间, 单位为(S)
                sync: 数据更新间隔设置为"auto"时的同步源
                    可选值 {U<1-3>|I<1-3>}
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values.items():
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_RATE_SET.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_RATE_GET.get(name))
        return self.query(query_cmd)

    # def recall_group(self, normal_block, list_block, *names, **values):

    def recall_number(self):
        """
        查询存储的测量数据的块数
        @return:
            存储的测量数据的块数, 注意后面的换行字符'\n'
        """
        return self.query(':RECall:NUMber?')

    def recall_normal(self, nrf=1):
        """
        查询指定块号的数字数据
        @param nrf: (type int) 1 ~ 9000 (block number)
        @return:
            指定块号的数字数据, 注意后面的换行字符'\n'
        """
        if int(self.recall_number()) > nrf:
            return self.query(':RECall:NORMal:VALue? {}'.format(nrf))

    def recall_list(self, nrf=1):
        """
        以指定的程序段号查询谐波测量的数字列表数据
        @param nrf: (type int) 1 ~ 600 (block number)
        @return:
            谐波测量的数字列表数据, 注意后面的换行字符'\n'
        """
        if int(self.recall_number()) > nrf:
            return self.query(':RECall:LIST:VALue? {}'.format(nrf))

    def recall_panel(self, nrf=1):
        """
        加载设置参数文件
        @param nrf: (type int) 1 ~ 4 (file number)
        @return:
            None
        """
        self.write(':RECall:PANel {}'.format(nrf))

    def status_group(self, *names, **values):
        """
        设置和查询用于进行与状态报告有关的参数
        @param names: (type tuple) 可选值说明如下:
                cond: 查询条件寄存器的内容
                eese: 查询扩展事件寄存器
                eesr: 查询扩展事件寄存器的内容并清除该寄存器
                err: 查询发生的最后一个错误的错误代码和消息(错误队列的顶部)
                qenable: 查询是否将错误消息以外的消息存储到错误队列中(ON)或不存储(OFF)
                qmsg: 查询是否将消息附加到STATus:ERRor?查询的响应
                spoll: 执行串行轮询
                filter<x>: 查询传输过滤器, <x> = 1 to 16
        @param values: (type dict) 字典说明如下:
                eese: (type int) 设置启用扩展事件寄存器
                    值范围: <Register> = 0 to 65535
                qenable: (type str) 设置是否将错误消息以外的消息存储到错误队列中(ON)或不存储(OFF)
                    可选值 <Boolean> = {ON|1|OFF|0}
                qmsg: (type str) 设置是否将消息附加到STATus:ERRor?查询的响应
                    可选值 <Boolean> = {ON|1|OFF|0}
                filter<x>: (type str) 设置传输过滤器. <x> = 1 to 16
                    可选值 {RISE|FALL|BOTH|NEVer}
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values:
            write_cmd = utils.contact_spci_cmd(Wt310eCmd.DICT_STATUS_SET.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(Wt310eCmd.DICT_STATUS_GET.get(name))
        return self.query(query_cmd)

    def store_state(self, on_off):
        """
        设置或查询存储开/关状态
        @param on_off: (type str) 可选值 {ON|1|OFF|0}
        @return:
            存储开/关状态, 注意后面的换行字符'\n'
        """
        if on_off in TUPLE_ON_OFF:
            self.write(Wt310eCmd.DICT_STORE_SET.get('state'), on_off)
        return self.query(Wt310eCmd.DICT_STORE_GET.get('state'))

    def store_interval(self, hour=None, minute=None, second=None):
        """
        设置或查询存储间隔
        @param hour: (type int) 小时, 0-99
        @param minute: (type int) 分钟, 0-99
        @param second: (type int) 秒拍, 0-99
        @return:
            储间隔, 注意后面的换行字符'\n'
        """
        if hour is not None \
                or minute is not None \
                or second is not None:
            self.write(self.write(Wt310eCmd.DICT_STORE_SET.get('interval'),
                                  0 if hour is None else hour,
                                  0 if minute is None else minute,
                                  0 if second is None else second))
        return self.query(Wt310eCmd.DICT_STORE_GET.get('interval'))

    def store_panel(self, nrf=1):
        """
        将设置参数保存到文件中
        @param nrf: (type int) 1 to 4 (file number)
        @return:
            None
        """
        self.write(Wt310eCmd.DICT_STORE_SET.get('panel'), nrf)

    def system_group(self, *names, **values):
        """
        设置和查询系统参数
        @params names: (type tuple) 可选值说明如下:
                model: 查询型号代码
                suffix: 查询后缀代码
                serial: 查询序列号
                firmware: 查询固件版本
                key_lock: 查询按键保护的开/关状态
                resolution: 查询数字数据显示分辨率
                commd: 查询命令类型
                mac_addr: 查询以太网MAC地址
        @params values: (type dict) 字典说明如下:
                key_lock: (type str) 查询按键保护的开/关状态
                    可选值 {ON|1|OFF|0}
                resolution: (type int) 设置数字数据显示分辨率
                    可选值范围 <NRf> = 4, 5 (digit)
                commd: 设置指令类型
                    可选值 {WT300E|WT300|WT200}
        @return:
            返回names中指定的查询值, 以分号(;)分割, 注意后面的换行字符'\n'
        """
        write_cmd = None
        for key, value in values.items():
            write_cmd = utils.contact_spci_cmd(write_cmd, Wt310eCmd.DICT_SYSTEM_SET.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Wt310eCmd.DICT_SYSTEM_GET.get(name))
        return self.query(query_cmd)

