# -*- encoding: utf-8 -*-
"""
@File    : rigol_scpi.py
@Time    : 2020/7/31 12:02
@Author  : blockish
@Email   : blockish@yeah.net
"""
__all__ = {
    'Md3058Scpi',
}

from instrument import utils
from instrument.meters.rigol.rigol_scpi_const import *
from instrument.scpi import ScpiInstrument


class Md3058Scpi(ScpiInstrument):
    """
    For supporting RIGOL multimeter, model MD3058.
    Used RIGOL command set by default, and not supported AGILENT command set
    """

    def __init__(self, resource_name, timeout=0, cmdset=CMD_SET_RIGOL):
        super().__init__(resource_name, timeout)
        self.__cmdset = cmdset

    def initialize(self):
        self.write(CMD_SET, self.__cmdset)
        super().initialize()

    def function(self, func_mode=None):
        """
        设置或查询基本测量功能
        :param func_mode: (type str): 测量功能
                dc_volt: 直流电压测量
                ac_volt: 交流电压测量
                dc_curr: 直流电流测量
                ac_curr: 交流电流测量
                res: 2线法电阻测量
                fres: 4线法电阻测量
                freq: 频率测量
                per: 周期测量
                cont: 短路测量
                dio: 二极管测量
                cap: 电容测量
        :return:
            (type str): DCV, ACV, DCI, ACI, RESISTANCE, CAPACITANCE, CONTINUITY, FRESISTANCE, DIODE, FREQUENCY or PERIOD
            注意后面换行字符'\n'
        """
        self.write(Md3058RigolCmd.DICT_FUNC_SET.get(func_mode))
        return self.query(Md3058RigolCmd.FUNC_GET)

    def function2(self, func_mode=None):
        """
        设置和查询仪器双显功能
        :param func_mode: (type str): 双显功能
                dc_volt: 副显示屏为直流电压测量
                ac_volt: 副显示屏为交流电压测量
                dc_curr: 副显示屏为直流直流测量
                ac_curr: 副显示屏为交流直流测量
                freq: 副显示屏为频率测量
                per: 副显示屏为周期测量
                res: 副显示屏为2线电阻测量
                fres: 副显示屏为4线电阻测量
                cap: 副显示屏为电容测量
        :return:
            (type str): DCV, ACV, DCI, ACI, 2WR, CAP, 4WR, FREQ or PERI
            注意后面换行字符'\n'
        """
        self.write(Md3058RigolCmd.DICT_FUNC2_SET.get(func_mode))
        return self.query(Md3058RigolCmd.FUNC2_GET)

    def function2_value1(self):
        """
        查询主显示屏的测量值(当双显功能打开时，此指令才有效)
        :return:
            (type str): 主显示屏的测量值, 注意后面有换行字符'\n'
        """
        return self.query(':FUNCtion2:VALUe1?')

    def function2_value2(self):
        """
        查询副显示屏的测量值(当双显功能打开时，此指令才有效)
        :return:
            (type str): 副显示屏的测量值, 注意后面有换行字符'\n'
        """
        return self.query(':FUNCtion2:VALUe2?')

    def function2_state(self):
        """
        查询副显示功能状态
        :return:
            (type str): '0\n' or '1\n'
        """
        return self.query(':FUNCtion2:ON?')

    def function2_clear(self):
        """
        用于清除副显示屏
        :return:
            None
        """
        self.write(':FUNCtion2:CLEar')

    def measure(self, name=None, value=None):
        """
        当name和value都为None时, 查询当前的触发设置是否采集到一个新数据
        否则, 用于设置或查询测量参数或查询测量值
        :param name: (type str): 可选值为
                mode: 设置测量模式, 此时value值可选 {AUTO|MANU}
                dc_volt_value: 查询直流电压测量值, 此时value值应该为None
                dc_volt_range: 查询、设置直流电压测量量程, 此时value可选值和说明如下:
                    value为None时, 只返回查询电压测量量程
                    --------------------------------------
                    |    参数    |   量程    |   分辨率   |
                    |  :-----:  |  :-----:  |  :-----:   |
                    |     0     |   200 mV  |  100   nV  |
                    |     1     |   2    V  |  1     uV  |
                    |     2     |   20   V  |  10    uV  |
                    |     3     |   200  V  |  100   uV  |
                    |     4     |   1000 V  |  1     mV  |
                    |    MIN    |   200 mV  |  100   nV  |
                    |    MAX    |   1000 V  |  1     mV  |
                    |    DEF    |   20   V  |  10    uV  |
                    |    None   | 只返回电压测量量程 |
                    --------------------------------------
                dc_volt_imp: 查询、设置直流阻抗, 此时value可选值为{10M|10G|None}
                dc_volt_flt: 查询、设置直流电压测量时交流滤波的开关状态, 此时value可选值为{ON|OFF|1|0|None}
                ac_volt_value: 查询交流电压测量值, 此时value值应该为None
                        (不能用于双显功能)
                ac_volt_range: 查询、设置交流电压测量量程, 此时value可选值和说明如下:
                    -------------------------
                    |    参数    |   量程    |
                    |  :-----:  |  :-----:  |
                    |     0     |   200 mV  |
                    |     1     |   2    V  |
                    |     2     |   20   V  |
                    |     3     |   200  V  |
                    |     4     |   750  V  |
                    |    MIN    |   200 mV  |
                    |    MAX    |   750  V  |
                    |    DEF    |   20   V  |
                    |    None   | 只返回电压测量量程 |
                    -------------------------
                dc_curr_value: 查询直流电流测量值, 此时value值应该为None
                dc_curr_range: 查询、设置直流电流测量量程, 此时value可选值和说明如下:
                    --------------------------------------
                    |    参数    |   量程    |   分辨率   |
                    |  :-----:  |  :-----:  |   :-----:  |
                    |     0     |   200 uA  |   1    nA  |
                    |     1     |   2   mA  |   10   nA  |
                    |     2     |   20  mA  |   100  nA  |
                    |     3     |   200 mA  |   1    uA  |
                    |     4     |   2    A  |   10   uA  |
                    |     5     |   10   A  |   100  uA  |
                    |    MIN    |   200 uA  |   1    nA  |
                    |    MAX    |   10   A  |   100  uA  |
                    |    DEF    |   200 mA  |   1    uA  |
                    |    None   | 只返回电流测量量程 |
                    --------------------------------------
                dc_curr_flt: 查询、设置直流电流测量时交流滤波的开关状态, 此时value可选值为{ON|OFF|1|0|None}
                ac_curr_value: 查询交流电流测量值, 此时value值应该为None
                ac_curr_range: 查询、设置交流电流测量量程, 此时value可选值和说明如下:
                    -------------------------
                    |    参数    |   量程    |
                    |  :-----:  |  :-----:  |
                    |     0     |   20  mA  |
                    |     1     |   200 mA  |
                    |     2     |   2    A  |
                    |     3     |   10   A  |
                    |    MIN    |   20  mA  |
                    |    MAX    |   10   A  |
                    |    DEF    |   200 mA  |
                    |    None   | 只返回电流测量量程 |
                    -------------------------
                res_value: 查询2线电阻测量值, 此时value应该为None
                        (不能用于双显功能)
                res_range: 查询、设置2线电阻测量量程, 此时value可选值和说明如下:
                    -------------------------
                    |    参数    |   量程    |
                    |  :-----:  |  :-----:  |
                    |     0     |   200  Ω  |
                    |     1     |   2   kΩ  |
                    |     2     |   20  kΩ  |
                    |     3     |   200 kΩ  |
                    |     4     |   1   MΩ  |
                    |     5     |   10  MΩ  |
                    |     6     |   100 MΩ  |
                    |    MIN    |   200  Ω  |
                    |    MAX    |   100 MΩ  |
                    |    DEF    |   200 kΩ  |
                    |    None   | 只返回2线电阻测量量程 |
                    -------------------------
                fres_value: 查询4线电阻测量值, 此时value应该为None
                        (不能用于双显功能)
                fres_range: 查询、设置4线电阻测量量程, 此时value可选值和说明如下:
                    -------------------------
                    |    参数    |   量程    |
                    |  :-----:  |  :-----:  |
                    |     0     |   200  Ω  |
                    |     1     |   2   kΩ  |
                    |     2     |   20  kΩ  |
                    |     3     |   200 kΩ  |
                    |     4     |   1   MΩ  |
                    |     5     |   10  MΩ  |
                    |     6     |   100 MΩ  |
                    |    MIN    |   200  Ω  |
                    |    MAX    |   100 MΩ  |
                    |    DEF    |   200 kΩ  |
                    |    None   | 只返回4线电阻测量量程 |
                    -------------------------
                freq_value: 查询频率测量值, 此时value应该为None
                        (测量频率范围为 20Hz~1MHz, 该命令不能用于双显功能.)
                fv_range: 查询、设置频率测量时使用的交流电压量程, 此时value参照 ac_volt_range设置
                per_value: 查询周期测量值, 此时value应该为None
                        (周期测量范围为 1μs~50ms.)
                pv_range: 查询、设置周期测量时使用的交流电压量程, 此时value参照 ac_volt_range设置
                cont_value: 查询短路测量时的电阻值, 此时value应该为None
                cont_range: 查询、设置测量时短路测量时的极限电阻值, 此时value值范围1 Ω~2000 Ω
                dio_volt: 查询二极管测试时二极管两端电压, 此时value值应该为None
                            (测量二极管时的蜂鸣条件为 0.1 V≤Vmeasured≤2.4 V)
                cap_value: 查询电容测量值(不能用于双显功能)
                cap_range: 查询、设置电容测量量程, 此时value可选值和说明如下:
                    -------------------------
                    |    参数    |   量程    |
                    |  :-----:  |  :-----:  |
                    |     0     |   2   nF  |
                    |     1     |   20  nF  |
                    |     2     |   200 nF  |
                    |     3     |   2   uF  |
                    |     4     |   200 uF  |
                    |     5     |  10000 uF |
                    |    MIN    |   2   nF  |
                    |    MAX    |  10000 uF |
                    |    DEF    |   200 nF  |
                    |    None   | 只返回电容测量量程 |
                    -------------------------
        :param value: 参考name中的value说明
        :return:
            (type str): 查询当前的触发设置是否采集到一个新数据时, 返回 TRUE or FALSE
            否则, 返回相应的设置值或查询值, 注意后面有换行字符'\n'
        """
        if name is None \
                and value is None:
            return self.query(':MEASure?')
        if value is not None:
            self.write(Md3058RigolCmd.DICT_MEASURE_SET.get(name), value)
        return self.query(Md3058RigolCmd.DICT_MEASURE_GET.get(name))

    def measure_rate(self, mode, rate=None):
        """
        设置或查询测量模式下速率
        :param mode: (type str): 可选值说明
                dc_volt: 直流电压
                ac_volt: 交流电压
                dc_curr: 直流电流
                ac_curr: 交流电流
                res: 2线电阻测量方式
                fres: 4线电阻测量方式
                sensor: 传感器测量速率, 注意此时rate可选值只能为{M|S}
        :param rate: (type str): 可选值说明
                -------------------------------------------------
                |    rate   | rate of measure | fresh frequency |
                |   :-----: |     :-----:     |     :-----:     |
                |  F(fast)  |  123 reading/s  |      50Hz       |
                | M(medium) |   20 reading/s  |      20Hz       |
                |  S(slow)  |  2.5 reading/s  |      2.5Hz      |
                -------------------------------------------------
        :return:
            (type str): 实际速率, 注意后面有换行字符'\n'
        """
        if rate is not None:
            self.write(Md3058RigolCmd.DICT_MEASURE_RATE_SET.get(mode), rate)
        return self.query(Md3058RigolCmd.DICT_MEASURE_RATE_GET.get(mode))

    def trigger_mode(self, *names, **values):
        """
        设置或查询触发参数
        :param names: (type tuple): 查询的触发参数名
                source: 测量时使用的触发源
                inter: 自动触发积分时间
                hold: 自动触发保持功能, 单位ms
                sens: 自动触发延迟灵敏度
                count: 单次触发的采样数目
                ext: 外部触发的触发类型
                polar:  VMC 输出极性
                w_pulse:  VMC 输出脉宽
        :param values: (type dict): 设置的触发参数名, 字典说明
                source (type str): 测量时使用的触发源, 可选值为{AUTO|SINGLE|EXT}, 分别表示“自动触发”， “单次触发”， “外部触发”
                inter (type int): 自动触发积分时间
                    不同的测量速率下自动触发<value>取值不同：
                        快速测量时， 积分时间默认是 8 ms，可设置的范围是 8 ms~2000 ms；
                        中速测量时，积分时间默认是 50 ms，可设置的范围是 50 ms~2000 ms；
                        慢速测量时，积分时间默认是 400 ms，可设置的范围是 400 ms~2000 ms。
                hold (type str): 自动触发保持功能, 可选值 {ON|OFF|1|0}
                sens (type int): 自动触发延迟灵敏度, 参数说明如下:
                    -------------------------
                    |    参数    |  灵敏度   |
                    |  :-----:  |  :-----:  |
                    |   0(MIN)  |   0.01%   |
                    |     1     |    0.1%   |
                    |   2(DEF)  |    1%     |
                    |   3(MAX)  |    10%    |
                    -------------------------
                count: 单次触发的采样数目
                ext: 外部触发的触发类型
                polar:  VMC 输出极性
                w_pulse:  VMC 输出脉宽
        :return:
            (type str): 依次返回names中的查询参数值, 以分号(;)分割, 注意后面有换行字符'\n'
        """
        write_cmd = None
        query_cmd = None
        for key, cmd in Md3058RigolCmd.DICT_TRIGGER_SET.items():
            value = values.get(key)
            if value is not None:
                write_cmd = utils.contact_spci_cmd(write_cmd, cmd.format(value))
                if len(names) == 0:
                    query_cmd = utils.contact_spci_cmd(query_cmd, Md3058RigolCmd.DICT_TRIGGER_GET.get(key))
        self.write(write_cmd)

        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Md3058RigolCmd.DICT_TRIGGER_GET.get(name))
        return self.query(query_cmd)

    def manual_trigger(self):
        """
        发送一个手动触发信号
        :return:
            None
        """
        self.write(':TRIGger:SINGle:TRIGgered')

    def calculate(self, *names, **values):
        """
        设置或查询仪器运算功能的相关参数或查询运算值
        :param names: (type tuple): 可选值
                func: 数学运算功能
                st_min: 最小值
                st_max: 最大值
                st_avg: 平均值
                st_count: 当前计算所进行测量的次数
                st_stat: 统计运算功能的使能状态
                rel_offset: 相对运算的偏移值
                rel_stat: 相对运算功能的使能状态
                db_value:  dB 值
                db_ref:  dB 参考值
                db_stat: dB 运算的使能状态
                dbm_value:  dBm 值
                dbm_ref: dBm 参考电阻值
                dbm_stat: dBm 运算的使能状态
                pf_value: P/F值
                pf_low: P/F 运算下限值
                pf_up: P/F 运算上限值
                pf_stat:  P/F 运算的使能状态
        :param values: (type dict): 设置字典说明
                func (type str): 数学运算功能, 可选值 {NONE|REL|DB|DBM|MIN|MAX|AVERAGE|TOTAL|PF}
                st_stat (type str): 统计运算功能的使能状态, 可选值 {ON|OFF|1|0}
                rel_offset (type float): 相对运算的偏移值, 取值范围如下:
                    ----------------------------------------
                    | 测量类型 | 取值范围 | DEF对应值 | 单位 |
                    | :-----: | :-----:  |  :-----:  | :--: |
                    | 直流电压 | ±1200    |     0     |  V   |
                    | 交流电压 | 0~900    |     0     |  V   |
                    | 直流电流 | ±12      |     0     |  A   |
                    | 交流电流 | 0~12     |     0     |  A   |
                    |   电阻   | 0~1.2e+08 |     0     |  Ω   |
                    |   电容   | 0~1.2e-02 |     0     |  F   |
                    |   频率   | 0~1.2e+06 |     0     |  Hz  |
                    -----------------------------------------
                rel_stat (type str): 相对运算功能的使能状态, 可选值 {ON|OFF|1|0}
                db_ref (type float): dB 参考值, 取值范围 -120 dBm~+120 dBm
                db_stat (type str): dB 运算的使能状态, 可选值 {ON|OFF|1|0}
                dbm_ref (type float): dBm 参考电阻值, 取值范围 2~8000 Ω
                dbm_stat (type str): dBm 运算的使能状态, 可选值 {ON|OFF|1|0}
                pf_low (type float):  P/F 运算下限值, 取值范围如下:
                    -----------------------------
                    | 测量类型 | 取值范围 | 单位 |
                    |  :-----: | :-----:  | :--: |
                    | 直流电压 | ±1200    |  V   |
                    | 交流电压 | 0~900    |  V   |
                    | 直流电流 | ±12      |  A   |
                    | 交流电流 | 0~12     |  A   |
                    |   电阻   | 0~1.2e+08 |  Ω   |
                    |   电容   | 0~1.2e-02 |  F   |
                    |   周期   | 1.0e-06~100 | s  |
                    |   频率   | 0~1.2e+06 |  Hz  |
                    -----------------------------
                pf_up (type float): P/F 运算上限值, 值范围参考pf_low并大于pf_low
                pf_stat (type str): P/F 运算的使能状态, {ON|OFF|1|0}
        :return:
            (type str): 依次返回names中的查询参数值, 以分号(;)分割, 注意后面有换行字符'\n'
        """
        write_cmd = None
        query_cmd = None
        for key, cmd in Md3058RigolCmd.DICT_CALC_SET.items():
            value = values.get(key)
            if value is not None:
                write_cmd = utils.contact_spci_cmd(write_cmd, cmd.format(value))
                if len(names) == 0:
                    query_cmd = utils.contact_spci_cmd(query_cmd, Md3058RigolCmd.DICT_CALC_GET.get(key))

        self.write(write_cmd)

        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Md3058RigolCmd.DICT_CALC_GET.get(name))
        return self.query(query_cmd)
