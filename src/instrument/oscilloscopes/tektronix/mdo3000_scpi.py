# -*- encoding: utf-8 -*-
import time
import warnings
from datetime import datetime
from typing import Union, Tuple

from constants import TUPLE_ON, TUPLE_ON_OFF
from errors import InstrumentException, ParamException
from instrument.scpi import ScpiInstrument
from .mdo3000_scpi_const import *

__all__ = {
    'Mdo3000Scpi',
}


def ch_trans(ch):
    if ch in Mdo3000Cmd.CHANNEL_COLOR_DICT:
        ch = Mdo3000Cmd.CHANNEL_COLOR_DICT.get(ch)
    else:
        ch = "".join(list(filter(str.isdigit, ch)))
    return ch


class Mdo3000Scpi(ScpiInstrument):

    def __init__(self, resource_name, timeout=0):
        super().__init__(resource_name, timeout)
        self.__bandwidth = None
        self.__analog_max_sample = None
        self.__analog_channels = None
        self.__record_length = None

    def remote(self, on_off):
        self.write(Mdo3000Cmd.DICT_REMOTE.get(on_off))
        return self.query('LOCk?')

    def initial(self):
        super().initialize()
        self.__bandwidth = float(self.config_query(BANDWIDTH))
        self.__analog_max_sample = float(self.config_query(ANALOG_SAMPLE_RATE))
        self.__analog_channels = int(self.config_query(ANALOG_CHANNEL_NUMBER))
        self.__record_length = tuple(int(x) for x in self.config_query(RECORD_LENGTH).split(','))

    @property
    def analog_max_sample(self):
        return self.__analog_max_sample

    @property
    def analog_channels(self):
        return self.__analog_channels

    @property
    def bandwidth(self):
        return self.__bandwidth

    @property
    def record_length(self):
        return self.__record_length

    """======================================================================================== """

    def acquire(self, state, mode=None, stop_after=None, num=None, **fast_acq):
        """
        设置和查询采集相关参数
        :param state: (type str) 采集使能, 可选值 {ON|RUN|1|OFF|STOP|0}
        :param mode: (type str) 采集模式, 可选值 {sam|peak|hir|ave|env}, 分别表示取样, 峰值, 高分辨率, 平均值, 包络
        :param stop_after: (type str) 采集完成后策略, 可选值 {runs|seq}, 分别表示 运行, 序列
        :param num: (type int) 当mode为ave(平均)时, 表示平均计算的波形个数, 此时num范围0~512且为2的指数幂
                            当mode为env(平均)时, 表示平均计算的包络个数, 此时num范围1~2000, 大于2000表示无限个
        :param fast_acq: (type dict): 快速采集设置, 字典说明如下:
                fast_state: 快速采集模式使能, 可选值 {0|1|OFF|ON}
                fast_pale: 快速采集模式的调色板, 可选值 {NORMal|TEMPErature|SPECTral|INVERTed}
        :return:
            (type str): 采集使能, 采集模式, 采集完成后策略, 当mode为'ave', 'env'时的波形或包络数, 快速采集模式使能, 快速采集模式的调色板,
            以分号(;)分割, 注意后面的换行字符'\n'
        """
        re_dict = {}

        if state in Mdo3000Cmd.TUPLE_ACQ_STATE:
            self.write(Mdo3000Cmd.ACQ_STATE_SET, state)

        state = self.query(Mdo3000Cmd.ACQ_STATE_GET)
        re_dict.update(state=state)

        if mode in Mdo3000Cmd.TUPLE_ACQ_MODE:
            self.write(Mdo3000Cmd.ACQ_MODE_SET, mode)

            re_mode = self.query(Mdo3000Cmd.ACQ_MODE_GET)
            re_dict.update(mode=re_mode)

            if mode == 'ave':  # 平均模式
                self.write(Mdo3000Cmd.ACQ_AVG_NUM_SET, num)
                num = self.query(Mdo3000Cmd.ACQ_AVG_NUM_GET)
                re_dict.update(num=num)
            elif mode == 'env':  # 包络模式
                self.write(Mdo3000Cmd.ACQ_ENV_NUM_SET, num)
                num = self.query(Mdo3000Cmd.ACQ_ENV_NUM_GET)
                re_dict.update(num=num)

        if stop_after in Mdo3000Cmd.TUPLE_ACQ_STOP_AFTER:
            self.write(Mdo3000Cmd.ACQ_STOP_AFTER_SET, stop_after)

        stop_after = self.query(Mdo3000Cmd.ACQ_STOP_AFTER_GET)
        re_dict.update(stop_after=stop_after)

        fast_state = fast_acq.get('fast_state')
        fast_pale = fast_acq.get('fast_pale')

        if fast_state in TUPLE_ON:
            self.write(Mdo3000Cmd.ACQ_FAST_STATE_SET, fast_state)
            if fast_pale in Mdo3000Cmd.TUPLE_ACQ_FAST_PALETTE:
                self.write(Mdo3000Cmd.ACQ_FAST_PALETTE_SET, fast_pale)

        fast_state = self.query(Mdo3000Cmd.ACQ_FAST_STATE_GET)
        re_dict.update(fast_state=fast_state)
        fast_pale = self.query(Mdo3000Cmd.ACQ_FAST_PALETTE_GET)
        re_dict.update(fast_pale=fast_pale)

        return re_dict

    """======================================================================================== """

    def alias(self, state, alias_op=None, label=None, seq=None):
        """
        设置和查询别名参数
        :param state: (type str) 别名使能, 可选值 {ON|1|OFF|0}
        :param alias_op: (type str): 可选值 {def|del|del_all}
                def: 定义别名(the alias label must be less than or equal to 12 characters
                and alias sequence must be less than or equal to 256 characters)
                del: 删除别名
                del_all: 删除所有别名
        :param label: (type str) 定义或删除别名的标签(别名必须不大于12个字符)
        :param seq: (type str) 别名代表的命令序列(必须不大于256个字符)
        :return:
            (type str): 别名使能值 '0\n' or '1\n'
            (type str): 所有的别名, 以逗号(,)分割, 注意后面的换行字符'\n'
        """
        if state in TUPLE_ON_OFF:
            self.write(Mdo3000Cmd.ALIAS_STATE_SET, state)

        if 'def' == alias_op and \
                label is not None and \
                seq is not None:
            self.write(Mdo3000Cmd.ALIAS_DEFINE_SET, '"' + label + '"', '"' + seq + '"')
        elif 'del' == alias_op and \
                label is not None:
            self.write(Mdo3000Cmd.ALIAS_DELETE, label)
        elif 'del_all' == alias_op:
            self.write(Mdo3000Cmd.ALIAS_DELETE_ALL)

        state = self.query(Mdo3000Cmd.ALIAS_STATE_GET)
        r_alias = self.query(Mdo3000Cmd.ALIAS_CATALOG_GET, label)
        return state, r_alias

    """======================================================================================== """

    def auto_set(self, op_type=None):
        """
        自动设置, 相当与前面板AutoSet
        :param op_type: (type str) 可选值 {ON|1|OFF|0|exec|undo}
                {ON|1|OFF|0}为设置前面板自动设置键使能开关
                exec: 执行自动设置
                undo: 取消执行自动设置
        :return:
            (type str): 当op_type为None时, 前面板自动设置键使能状态 '0\n' or '1\n'
        """
        if op_type is None:
            return self.query(Mdo3000Cmd.AUTO_SET_GET)
        if op_type in TUPLE_ON_OFF:
            self.write(Mdo3000Cmd.AUTO_SET_ENABLE_SET, op_type)
            return self.query(Mdo3000Cmd.AUTO_SET_ENABLE_GET)
        elif op_type in Mdo3000Cmd.TUPLE_AUTO_SET:
            self.write(Mdo3000Cmd.AUTO_SET_SET, op_type)
            while self.is_busy():
                time.sleep(0.1)

    """======================================================================================== """

    def is_busy(self):
        """
        示波器忙状态
        :return:
            (type bool): 'True\n'表示示波器正忙于处理一个执行时间很长的命令
                        'False\n'表示示波器不忙于处理执行时间较长的命令
        """
        return '1\n' == self.query('BUSY?')

    """======================================================================================== """

    def channel_setting(self, ch, amp_en=None, volt_fact=None, bandwidth=None, coup=None, deskew=None,
                        offset=None, invert=None, pos=None, scale=None, y_unit=None, term=None, label=None):
        """
        查询或设置模拟通道参数
        :param ch: (type str) 通道号或者通道颜色, 可选值 {1|2|3|4|yellow|blue|purple|green}
        :param amp_en: (type str) 是否测试电流, 可选值 {ON|OFF|0|1}
        :param volt_fact: (type float) 测量电流时, 电压转换为电流的因子
        :param bandwidth: (type float) 通道带宽, 是一个离散的值
        :param coup: (type str) 耦合方式, 可选值 {AC|DC|DCREJect}分别表示直流, 交流, 直流拒绝耦合(需要探头支持)
        :param deskew: (type float) 相差校正时间, 单位为s, 范围-100E-9~100E-9
        :param offset: (type float) 通道Y轴零点相对与坐标轴Y轴零点的偏移值, 范围说明如下:
                --------------------------------------------------------------
                |                           | Offset range |            |
                |           :-----:         |    :-----:   |    :--:    |
                |    V/Div Setting          | 1 MΩ Input   | 50 Ω Input |
                | 1 mV/div — 50 mV/div      |     ±1 V     |   ±1 V     |
                | 50.5 mV/div — 99.5 mV/div |     ±0.5 V   |   ±0.5 V   |
                | 100 mV/div — 500 mV/div   |     ±10 V    |   ±5 V     |
                | 505 mV/div — 995 mV/div   |     ±5 V     |   ±5 V     |
                | 1 V/div — 5 V/div         |     ±100 V   |   ±5 V     |
                | 5.05 V/div — 10 V/div     |     ±50 V    |   N/A      |
                --------------------------------------------------------------
                note: For 50 Ω input, 1 V/div is the maximum setting.
        :param invert: (type str) 反转使能, 可选值 {ON|OFF|0|1}
        :param pos: (type float) 设置相对零点在屏幕的偏移位置
        :param scale: (type float) 垂直缩放, 单位V, 表示V/div
        :param y_unit: (type str) Y轴单位
        :param term: (type str or float) 终端电阻值, 可选值 {FIFty|MEG|<NR3>}
                FIFty: 50 Ω
                MEG : 1 MΩ
                <NR3>: 其他数值, 单位 Ω
        :param label: (type str) 当前通道显示的标签
        :return:
            当前ch通道的所有参数, 注意后面的换行字符'\n'
        """
        assert ch is not None, 'required a channel'
        if isinstance(ch, str):
            ch = ch_trans(ch)
        cmd = None

        if amp_en in TUPLE_ON_OFF:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_AMP_VOLT_EN_SET, ch, amp_en)
        if volt_fact is not None:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_AMP_VOLT_FACT_SET, ch, volt_fact)
        if bandwidth is not None:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_BANDWIDTH_SET, ch, bandwidth)
        if coup in Mdo3000Cmd.TUPLE_COUPING:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_COUPLING_SET, ch, coup)
        if deskew is not None:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_DESKEW_SET, ch, deskew)
        if offset is not None:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_OFFSET_SET, ch, offset)
        if invert in TUPLE_ON_OFF:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_INVERT_SET, ch, invert)
        if pos is not None:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_POSITION_SET, ch, pos)
        if scale is not None:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_SCALE_SET, ch, scale)
        if y_unit in TUPLE_Y_UNITS:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_YUNITS_SET, ch, '%s%s%s' % ('"', y_unit, '"'))
        if term is not None:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_TERMINATION_SET, ch, term)
        if label is not None:
            cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_LABEL_SET, ch, label)
        # cmd = utils.contact_spci_cmd(cmd, Mdo3000Cmd.CH_INFO_GET, ch)

        self.write(cmd)
        time.sleep(0.5)
        return self.query(Mdo3000Cmd.CH_INFO_GET, ch)

    """======================================================================================== """

    def prob_setting(self, ch, *names, **values):
        """
        探头设置
        :param ch: (type str) 探头所在的通道号或者通道颜色, 可选值 {1|2|3|4|yellow|blue|purple|green}
        :param names: (type tuple) 需要查询的探头参数名或执行的命令, 可选值:
                 auto_zero: 自动调零, 由于执行该命令需要将探头接到参考值, 故names中包含该值时, 执行完命令后直接返回
                 cal_state: 获取探头校准状态, 非0值为校准状态NG
                 deg: 执行探头(针对电流探头, 且需要探头支持)消磁
                 deg_state: 查询探头消磁状态, 非0值为消磁状态NG
                 range: 获取探头的量程(需要探头支持)
                 gain: 获取探头增益值, 0.1倍增益表示衰减10倍
                 id: 获取探头的ID
                 sn: 获取探头的序列号Series Number
                 type: 获取探头的类型, other表示未知类型探头
                 model: 获取探头型号
                 prop_delay: 获取探头的传播延迟时间, 单位 s
                 deskew: 获取探头的相差校正时间, 单位 s
                 res: 获取探头电阻
                 signal: 获取探头的输入旁路设置, BYPASS or PASS
                 units: 获取探头的测量单位
        :param values:  (type dict) 探头设置字典, 说明如下
                cal (type str): 设置和执行探头自动校准动作, 可选值为 {init|exec}, 分别表示初始化和初始化校准,
                    由于执行该命令需要将探头接到校准电平, 如果values字典中包含该键值, 则执行操作直接返回
                range (type float): 强制设置探头量程(需要探头支持)
                gain (type float): 设置探头增益值, 0.1倍增益表示衰减10倍
                prop_delay (type float): 设置探头传播延迟时间, 单位为 s
                signal (type float): 设置探头的输入旁路, 可选值为 {byp|pass}
        :return:
            (type str): 返回names中查询的相关值, 注意后面的换行字符'\n'
        """
        assert ch is not None, 'required a channel'
        if isinstance(ch, str):
            ch = ch_trans(ch)
        if PROBE_AUTO_ZERO in names:
            self.write(Mdo3000Cmd.PROBE_OPERATION_DICT.get(PROBE_AUTO_ZERO), ch)
            return
        # 是否是自动调零命令

        try:
            cal_op = values.pop(PROBE_CALIBRATE)
            result = self.query(Mdo3000Cmd.PROBE_CALIBRATABLE_GET, ch)
            if '1' == result:
                if INITIALIZE == cal_op:
                    self.write(Mdo3000Cmd.PROBE_CALIBRATE_SET, ch, cal_op)
                    time.sleep(2)

                self.write(Mdo3000Cmd.PROBE_SET_DICT.get(PROBE_CALIBRATE), ch, EXECUTE)
                time.sleep(5)
                return
            else:
                warnings.warn('The probe of channel %s not support calibrate operation', ch)
        except KeyError:
            pass
        # 是否是校准命令

        if PROBE_DEGAUSS in names:
            self.write(Mdo3000Cmd.PROBE_OPERATION_DICT.get(PROBE_DEGAUSS), ch)
            time.sleep(2)
        state = self.query(Mdo3000Cmd.PROBE_OPERATION_DICT.get(PROBE_DEGAUSS_STATE), ch)
        self._logger.debug('the state of degauss: %s', state)
        # 消磁

        write_cmd = None
        for key, value in values.items():
            if key in Mdo3000Cmd.PROBE_SET_DICT and PROBE_CALIBRATE != key:
                write_cmd = utils.contact_spci_cmd(write_cmd, Mdo3000Cmd.PROBE_SET_DICT.get(key), ch, value)
        self.write(write_cmd)
        # 设置相关参数

        read_cmd = None
        for op in names:
            if op in Mdo3000Cmd.PROBE_OPERATION_DICT \
                    and PROBE_DEGAUSS != op \
                    and PROBE_AUTO_ZERO != names:
                read_cmd = utils.contact_spci_cmd(read_cmd, Mdo3000Cmd.PROBE_OPERATION_DICT.get(op), ch)

        if read_cmd is not None:
            return self.query(read_cmd)
        # 查询相关参数

    """======================================================================================== """

    def clear_menu(self):
        """
        清除菜单显示, 相当于按下前面板Menu Off按钮, 此功能只在remote为OFF时才有效
        :return:
            None
        """
        self.write('CLEARM')

    """======================================================================================== """

    def cursor_setting(self, *names, **values):
        """
        设置和查询光标相关参数
        :param names: (type tuple) 查询相关参数, 可选值说明:
                func: 获取光标的功能模式
                      在波形功能模式下，光标连接到所选波形;
                      在屏幕功能模式下，光标连接到显示区域
                h_delta: 获取两个水平光标之间的垂直差
                h_pos1: 获取水平条光标1相对于地面的值，该位置以垂直单位（通常为V）
                h_pos2: 获取水平条光标2相对于地面的值，该位置以垂直单位（通常为V）
                h_unit: 获取水平方向光标值的单位
                mode: 获取光标模式, 该模式是指光标是否联动
                source: 获取光标的源, 通常返回为通道编号或AUTO, 当光标的源为AUTO时, 光标读数适用于当前选定的波形
                v_alt1: 获取垂直光标1的备用读数
                v_alt2: 获取垂直光标2的备用读数
                v_delta: 获取两个垂直光标之间的水平差
                v_hpos1: 获取垂直光标1的指定垂直条刻度的垂直值
                v_hpos2: 获取垂直光标2的指定垂直条刻度的垂直值
                v_pos1: 获取垂直条光标1的水平位置值
                v_pos2: 获取垂直条光标1的水平位置值
                v_unit: 获取垂直方向光标值的单位
                v_vdelta: 获取两个垂直条光标刻度之间的垂直差
                pr_delta: 获取光标的极坐标差(ΔY/ΔX), 计算公式为(cursor 2 Y - cursor 1 Y) ÷ (cursor 2 X - cursor 1 X)
                pr_pos1: 获取光标1的极坐标半径
                pr_pos2: 获取光标2的极坐标半径
                pr_unit: 获取光标的极坐标半径单位
                pt_delta: 获取XY光标极轴角增量
                pt_pos1: 获取光标X1(水平)或光标Y1(垂直)极坐标
                pt_pos2: 获取光标X2(水平)或光标Y2(垂直)极坐标
                pt_unit: 获取光标极坐标单位
                p_delta: 获取光标X位置和光标Y位置之间的差异(ΔX × ΔY), 计算公式为(X2 - X1) × (Y2 - Y1)
                p_pos1: 获取X1或Y1光标的位置, 计算公式为 X1 × Y1
                p_pos2: 获取X2或Y2光标的位置, 计算公式为 X2 × Y2
                p_unit: 获取光标坐标单位
                r_delta: 光标X位置和光标Y位置之差的比值(ΔY/ΔX), 计算公式为(Y2 - Y1) / (X2 - X1)
                r_pos1: 获取指定光标的X1（水平）或Y1（垂直）位置
                r_pos2: 获取指定光标的X2（水平）或Y2（垂直）位置
                r_unit: 获取用于比率测量的光标X和光标Y单位
                readout: 获取XY光标读数选择
                rx_delta: 获取直角坐标中的光标X增量值
                rx_pos1: 获取光标1的X直角坐标
                rx_pos2: 获取光标2的X直角坐标
                rx_unit: 获取光标X直角坐标单位
                ry_delta: 获取直角坐标中的光标Y增量值
                ry_pos1: 获取光标1的Y直角坐标
                ry_pos2: 获取光标2的Y直角坐标.
                ry_unit: 获取光标Y直角坐标单位
        :param values: (type dict) 字典说明如下:
                func (type str): 设置光标的功能模式, 可选值 {SCREEN|WAVEform|OFF}, 分别表示屏幕功能模式, 波形功能模式, 关
                h_pos1 (type float): 设置水平条光标1相对于地面的位置
                h_pos2 (type float): 设置水平条光标2相对于地面的位置
                h_unit (type str): 设置水平光标的单位, 可选值为, {BASE|PERcent}
                h_use (type str): 设置水平条光标测量比例, 此命令只在光标打开时有效, 可选值为 {CURrent|HALFgrat}
                mode (type str): 设置是否光标联动, 可选值 {TRACk|INDependent}, 分别表示为 联动和取消联动
                source (type str): 设置光标源, 可选值为 {CH<x>|REF<x>|MATH|BUS<x>|D<x>|RF_AMPlitude|RF_FREQuency|RF_PHASe|AUTO}
                v_pos1 (type float): 设置垂直光标1的水平位置
                v_pos2 (type float): 设置垂直光标2的水平位置
                v_unit (type str): 设置垂直光标的单位, 可选值 {SEConds|HERtz|DEGrees|PERcent}, 分别表示 秒, 赫兹, 角度, 百分比
                v_use (type float): 设置垂直条光标测量比例, 此命令只在光标打开时有效, 可选值 {CURrent|HALFgrat|FIVEdivs}
                readout (type str): 设置XY光标读数选择, 可选值 {RECTangular|POLARCord|PRODuct|RATio}
                    RECTangular: 将XY读数指定为直角坐标。
                    POLARCord: 将XY读数指定为极坐标
                    PRODuct:  以X*Y格式指定XY读数
                    RATio:  以X:Y格式指定XY读数
                rx_pos1 (type float): 指定光标1直角坐标X
                rx_pos2 (type float): 指定光标2直角坐标X
                ry_pos1 (type float): 指定光标1直角坐标Y
                ry_pos2 (type float): 指定光标2直角坐标Y
        :return:
            (type str): 分别返回names中的查询值, 以分号(;)分割
        """
        write_cmd = None
        for key, value in values:
            if key in Mdo3000Cmd.CURSOR_SET_DICT:
                write_cmd = utils.contact_spci_cmd(write_cmd, Mdo3000Cmd.CURSOR_SET_DICT.get(key), value)
        if write_cmd is not None:
            self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Mdo3000Cmd.CURSOR_GET_DICT.get(name))
        if query_cmd is not None:
            return self.query(query_cmd)

    """======================================================================================== """

    def date_time_setting(self, *names, **values):
        """
        设置和查询示波器的时间
        :param names: (type tuple) 可选值 {d|t}, 分别表示 日期, 时间
        :param values: (type dict) 时间日期设置字典, 说明如下:
                d (type str): 日期格式必须保证为 yyyy-MM-dd
                t (type str): 时间格式必须保证为 HH:mm:ss
        :return:
            (type str): 分别返回names中的查询值, 以分号(;)分割
        """
        write_cmd = None
        for key, value in values.items():
            #             assert value is not None
            if key in Mdo3000Cmd.DATE_TIME_SET_DICT:
                write_cmd = utils.contact_spci_cmd(write_cmd, Mdo3000Cmd.DATE_TIME_SET_DICT.get(key),
                                                   '"' + value + '"')

        read_cmd = None
        for op in names:
            if op in Mdo3000Cmd.DATE_TIME_GET_DICT:
                read_cmd = utils.contact_spci_cmd(read_cmd, Mdo3000Cmd.DATE_TIME_GET_DICT.get(op))

        cmd = utils.contact_spci_cmd(write_cmd, read_cmd)
        self.write(cmd)
        if read_cmd is not None:
            return self.read()

    """======================================================================================== """

    def measure(self, measures, upper=4, gating='SCREen', method='AUTO', sleep=.1, statistics=None):
        """
        测量操作, 对应于示波器上添加测量, 此命令是耗时操作, 处理计算期间示波器无法接受其他指令
        :param measures: (type dict) 需要添加测量的字典, 说明如下:
                source (type str): (必须指定) 需要添加的测量源, 可选值为 {CH<x>|REF<x>|MATH|BUS<x>|D<x>|RF_AMPlitude|RF_FREQuency|RF_PHASe}
                meas_type (type str): (必须指定) 测量类型, 可选值
                                {AMPlitude|AREa|BURst|CARea|CMEan|CRMs|DELay|FALL|FREQuency
                                |HIGH|HITS|LOW|MAXimum|MEAN|MEDian|MINImum|NDUty|NEDGECount
                                |NOVershoot|NPULSECount|NWIdth|PEAKHits|PEDGECount|PDUty
                                |PERIod|PHAse|PK2Pk|POVershoot|PPULSECount|PWIdth|RISe|RMS
                                |SIGMA1|SIGMA2|SIGMA3|STDdev|TOVershoot|WAVEFORMS}
                state (type str): (可选)激活状态, 此状态控制添加的测量是否生效激活
                ref_method (type str): (可选) 指定计算时引用波形参考方式, 可选值 {ABSolute|PERCent},
                        注意: 此设置会影响立即测量和四个周期测量, 要更改单个测量的参数, 请使用MEASUrement:MEAS<x>:REFLevel命令.
                ref_abs_high (type float): (可选) 当ref_method设置为ABSolute时, 指定引用波形绝对计算参考高值(100%)
                        注意: 此设置会影响立即测量中与参考值相关的计算和四个周期测量
                ref_abs_mid (type float): (可选) 当ref_method设置为ABSolute时, 指定引用波形绝对计算参考中间值(50%)
                        注意: 此设置会影响周期, 频率, 延时以及所有循环测量的计算值, 同时还影响立即测量中与参考值相关的计算和四个周期测量
                targ_ref_abs_mid (type float): (可选) 当ref_method设置为ABSolute时, 指定目标波形绝对计算参考中间值(50%)
                        注意: 此设置会影响周期, 频率, 延时以及所有循环测量的计算值, 同时还影响立即测量中与参考值相关的计算和四个周期测量
                ref_abs_low (type float): (可选) 当ref_method设置为ABSolute时, 指定引用波形绝对计算参考低值(10%)
                        注意: 此设置会影响立即测量中与参考值相关的计算和四个周期测量
                ref_per_high (type float): (可选) 当ref_method设置为PERCent时, 指定引用波形百分比计算参考高值(100%)
                        注意: 此设置会影响立即测量中与参考值相关的计算和四个周期测量
                ref_per_mid (type float): (可选) 当ref_method设置为PERCent时, 指定引用波形百分比计算参考中间值(50%)
                        注意: 此设置会影响周期, 频率, 延时以及所有循环测量的计算值, 同时还影响立即测量中与参考值相关的计算和四个周期测量
                targ_ref_per_mid (type float): (可选) 当ref_method设置为PERCent时, 指定目标波形百分比计算参考中间值(50%)
                        注意: 此设置会影响周期, 频率, 延时以及所有循环测量的计算值, 同时还影响立即测量中与参考值相关的计算和四个周期测量
                ref_per_low (type float): (可选) 当ref_method设置为PERCent时, 指定引用波形百分比计算参考低值(10%)
                        注意: 此设置会影响立即测量中与参考值相关的计算和四个周期测量
                target (type str) (type str): (当meas_type为DELay或PHAse时必须指定), 指定目标波形, 可选值 {CH<x>|REF<x>|MATH|BUS<x>|D<x>|RF_AMPlitude|RF_FREQuency|RF_PHASe}
                direction (type str): (optional) 当meas_type为DELay时, 设置延迟测量时到目标波形边缘起点的方向, 可选值 {BACKWards|FORWards}
                sour_edge (type str): (optional) 当meas_type为DELay时, 设置源波形的边缘类型, 可选值 {FALL|RISe}
                targ_edge (type str): (optional) 当meas_type为DELay时, 设置目标波形的边缘类型, 可选值 {FALL|RISe}
        :param upper: (type int) 可添加测量的上限, MDO3000系列最大支持添加4个测量
        :param gating: (type str) 测量选通设置, 可选值 {OFF|SCREen|CURSor}
                    OFF: 关闭测量选通, 即所有采样点
                    SCREen: 开启测量选通为屏幕上所有的点
                    CURSor: 开启测量选通为垂直光标中间所有的点, 不管光标在不在屏幕上显示
        :param method: (type str) (可选) 测量的计算方法, 可选值 {AUTO|HIStogram|MINMax}
                            HIStogram: 使用直方图统计最大最小值
                            MINMax:使用波形记录的最高值和最低值. 此选项最适合检查没有公共值的大而平的部分的波形, 如正弦波和三角波
                            AUTO: 示波器自动选择以上最佳的一种方式
        :param sleep: (type float) 每次发送测量命令给示波器采样计算的延迟时间, 需要根据采集长度决定该时间
        :param statistics: (type dict) 测量统计设置字典,可包含的键值说明如下:
                mode (type str): (可选) 设置统计的状态, 可选值为 {OFF|ALL}
                weight (type int): (可选) 设置测量统计的平均值和标准差取样次数, 范围 2~1000
                reset (type bool): (可选) 重置测量统计
        :return:
            (type tuple of str): 返回每一个测量的 值, 最大值, 最小值, 平均值, 标准差, 单位(依次):以分号(;)分割,
                    测量统计的状态和取样次数:以分号(;)分割
        """
        assert isinstance(measures, tuple) or isinstance(measures, list), \
            'the argument "measurements" must be a tuple or list of dict'

        if len(measures) > upper:
            self._logger.warning('size of measurement rather than upper limit %d', upper)

        for i in range(upper):
            self.write('MEASUrement:MEAS{}:STATE {}', i + 1, 'OFF')
        self.write('MEASUrement:GATing {}', gating)
        self.write('MEASUrement:METHod {}', method)

        query_cmd = None
        count = 0
        for measure in measures:
            count = count + 1
            if count > upper:
                # the size rather than 4, ignored all next #
                break
            assert isinstance(measure, dict), 'the element of "measurements" must be a dict'

            try:
                state = measure.get('state')
                assert state in TUPLE_ON_OFF, 'the state only be "on" or "off"'
                self.write('MEASUrement:MEAS{}:STATE {}', count, state)
                if state in TUPLE_ON:
                    self.__set_meas_param(count, immed=False, **measure)
            except InstrumentException as e:
                raise e
        time.sleep(sleep)
        for i in range(count):
            val = i + 1
            query_cmd = utils.contact_spci_cmd(query_cmd,
                                               'MEASUrement:MEAS{}:VALue?;:' +
                                               'MEASUrement:MEAS{}:MAXimum?;:' +
                                               'MEASUrement:MEAS{}:MINImum?;:' +
                                               'MEASUrement:MEAS{}:MEAN?;:' +
                                               'MEASUrement:MEAS{}:STDdev?;:' +
                                               'MEASUrement:MEAS{}:UNIts?',
                                               val, val, val, val, val, val)
        self.write(query_cmd)

        return self.read(), self.measure_statistics(statistics)

    """======================================================================================== """

    def measure_indicator(self, state, sleep) -> Union[None, Tuple]:
        """
        设置并读取测量指示器的值
        :param state: (type int or str)
            测量指示器状态, 可选值为{<x>|OFF}, x表示测量指示器的测量序号, MDO3000系列最大支持4个测量, 即x为1, 2, 3, 4
        :param sleep: (type float)
            添加测量指示器后的读取数据的延迟时间, 与记录长度有关
        :return: (type tuple of str)
            当state为OFF时, 返回None, 否则返回
            指示器的水平点的值(以分号(;)分割), 指示器的垂直点的值(以分号(;)分割)
        """
        if isinstance(state, int):
            self.write('MEASUrement:INDICators:STATE {}'.format('MES{}'), state)
        else:
            self.write('MEASUrement:INDICators:STATE {}', state)
            return
        time.sleep(sleep)
        num_horz = self.query('MEASUrement:INDICators:NUMHORZ?')
        num_vert = self.query('MEASUrement:INDICators:NUMVERT?')
        query_cmd = None
        for i in range(num_horz):
            query_cmd = utils.contact_spci_cmd(query_cmd, 'MEASUrement:INDICators:HORZ{}?', i)
        horz = self.query(query_cmd)
        query_cmd = None
        for i in range(num_vert):
            query_cmd = utils.contact_spci_cmd(query_cmd, 'MEASUrement:INDICators:VERT{}?', i)
        vert = self.query(query_cmd)

        return horz, vert

    """======================================================================================== """

    def measure_statistics(self, statistics) -> str:
        """
        测量统计
        :param statistics: (type dict) 测量统计设置字典,可包含的键值说明如下:
            mode (type str): (可选) 设置统计的状态, 可选值为 {OFF|ALL}
            weight (type int): (可选) 设置测量统计的平均值和标准差取样次数, 范围 2~1000
            reset (type bool): (可选) 重置测量统计
        :return: (type str)
            测量统计的状态和取样次数:以分号(;)分割
        """
        if isinstance(statistics, dict):
            mode = statistics.get('mode', None)
            if mode is not None:
                self.write('MEASUrement:STATIstics:MODe {}', mode)
            weight = statistics.get('weight', None)
            if weight is not None:
                self.write('MEASUrement:STATIstics:WEIghting {}', weight)
            reset = statistics.get('reset', None)
            if reset is True:
                self.write('MEASUrement:STATIstics RESET')
        return self.query('MEASUrement:STATIstics?')

    """======================================================================================== """

    def measure_immed(self, gating='SCREen', method='AUTO', sleep=.1, **measure):
        """
        立即测量操作, 此命令是耗时操作, 处理计算期间示波器无法接受其他指令
        :param gating: (type str) 测量选通设置, 可选值 {OFF|SCREen|CURSor}
                    OFF: 关闭测量选通, 即所有采样点
                    SCREen: 开启测量选通为屏幕上所有的点
                    CURSor: 开启测量选通为垂直光标中间所有的点, 不管光标在不在屏幕上显示
        :param method: (type str) (可选) 测量的计算方法, 可选值 {AUTO|HIStogram|MINMax}
                            HIStogram: 使用直方图统计最大最小值
                            MINMax:使用波形记录的最高值和最低值. 此选项最适合检查没有公共值的大而平的部分的波形, 如正弦波和三角波
                            AUTO: 示波器自动选择以上最佳的一种方式
        :param sleep: (type float) 每次发送立即测量命令给示波器采样计算的延迟时间, 需要根据采集长度决定该时间
        :param measure: (type dict) 立即测量设置字典, 说明如下:
                source (type str): (必须指定) 需要添加的测量源, 可选值为 {CH<x>|REF<x>|MATH|BUS<x>|D<x>|RF_AMPlitude|RF_FREQuency|RF_PHASe}
                meas_type (type str): (必须指定) 测量类型, 可选值
                                {AMPlitude|AREa|BURst|CARea|CMEan|CRMs|DELay|FALL|FREQuency
                                |HIGH|HITS|LOW|MAXimum|MEAN|MEDian|MINImum|NDUty|NEDGECount
                                |NOVershoot|NPULSECount|NWIdth|PEAKHits|PEDGECount|PDUty
                                |PERIod|PHAse|PK2Pk|POVershoot|PPULSECount|PWIdth|RISe|RMS
                                |SIGMA1|SIGMA2|SIGMA3|STDdev|TOVershoot|WAVEFORMS}
                state (type str): (可选)激活状态, 此状态控制添加的测量是否生效激活
                ref_method (type str): (可选) 指定计算时引用波形参考方式, 可选值 {ABSolute|PERCent},
                        注意: 此值会受测量设置的值影响, 注意及时更新
                ref_abs_high (type float): (可选) 当ref_method设置为ABSolute时, 指定引用波形绝对计算参考高值(100%)
                        注意: 此值会受测量设置的值影响, 注意及时更新
                ref_abs_mid (type float): (可选) 当ref_method设置为ABSolute时, 指定引用波形绝对计算参考中间值(50%)
                        注意: 此值会受测量设置的值影响, 注意及时更新
                targ_ref_abs_mid (type float): (可选) 当ref_method设置为ABSolute时, 指定目标波形绝对计算参考中间值(50%)
                        注意: 此值会受测量设置的值影响, 注意及时更新
                ref_abs_low (type float): (可选) 当ref_method设置为ABSolute时, 指定引用波形绝对计算参考低值(10%)
                        注意: 此值会受测量设置的值影响, 注意及时更新
                ref_per_high (type float): (可选) 当ref_method设置为PERCent时, 指定引用波形百分比计算参考高值(100%)
                        注意: 此值会受测量设置的值影响, 注意及时更新
                ref_per_mid (type float): (可选) 当ref_method设置为PERCent时, 指定引用波形百分比计算参考中间值(50%)
                        注意: 此值会受测量设置的值影响, 注意及时更新
                targ_ref_per_mid (type float): (可选) 当ref_method设置为PERCent时, 指定目标波形百分比计算参考中间值(50%)
                        注意: 此值会受测量设置的值影响, 注意及时更新
                ref_per_low (type float): (可选) 当ref_method设置为PERCent时, 指定引用波形百分比计算参考低值(10%)
                        注意: 此值会受测量设置的值影响, 注意及时更新
                target (type str) (type str): (当meas_type为DELay或PHAse时必须指定), 指定目标波形, 可选值 {CH<x>|REF<x>|MATH|BUS<x>|D<x>|RF_AMPlitude|RF_FREQuency|RF_PHASe}
                direction (type str): (optional) 当meas_type为DELay时, 设置延迟测量时到目标波形边缘起点的方向, 可选值 {BACKWards|FORWards}
                sour_edge (type str): (optional) 当meas_type为DELay时, 设置源波形的边缘类型, 可选值 {FALL|RISe}
                targ_edge (type str): (optional) 当meas_type为DELay时, 设置目标波形的边缘类型, 可选值 {FALL|RISe}
        :return:
            (type str) 返回当前立即测量的值和单位
        """
        try:
            self.write('MEASUrement:GATing {}', gating)
            self.write('MEASUrement:METHod {}', method)
            self.__set_meas_param(count=None, immed=True, **measure)
        except InstrumentException as e:
            raise e

        self.write('MEASUrement:IMMed:VALue?;:MEASUrement:IMMed:UNIts?')
        time.sleep(sleep)
        return self.read()

    """======================================================================================== """

    def __set_meas_param(self, count, immed=False, **measure):
        """测量和立即测量参数设置辅助方法"""

        source = measure.get('source')  # 测量源
        meas_type = measure.get('meas_type')  # 测量类型

        if immed is True:
            # 两个不同的报错
            assert source is not None, 'the immediately measurement must be contains key named "source"'
            assert meas_type is not None, 'the immediately measurement must be contains key named "meas_type"'
            self.write('MEASUrement:IMMed:SOUrce1 {}', source)
            self.write('MEASUrement:IMMed:TYPe {}', meas_type)
        elif immed is False:
            # 两个不同的报错
            assert source is not None, 'the measurement dict must be contains key named "source"'
            assert meas_type is not None, 'the measurement dict must be contains key named "meas_type"'
            self.write('MEASUrement:MEAS{}:SOUrce1 {};:MEASUrement:MEAS{}:TYPe {}', count, source, count, meas_type)
        else:
            raise ParamException('Error argument immed, expect a bool but %s', immed)

        # method = measure.get('method', 'AUTO')

        ref_method = measure.get('ref_method')  # , 'AUTO')
        ref_abs_high = measure.get('ref_abs_high')  # , 0.0E+0)
        ref_abs_mid = measure.get('ref_abs_mid')  # , 0.0E+0)
        ref_abs_low = measure.get('ref_abs_low')  # , 0.0E+0)
        ref_per_high = measure.get('ref_per_high')  # , 90.)
        ref_per_mid = measure.get('ref_per_mid')  # , 50.)
        ref_per_low = measure.get('ref_per_low')  # , 10.)

        if ref_method is not None:
            self.write('MEASUrement:REFLevel:METHod {}', ref_method)
        if Mdo3000Cmd.REG_ABSOLUTE.search(meas_type) is not None:
            if ref_abs_high is not None:
                self.write('MEASUrement:REFLevel:ABSolute:HIGH {}', ref_abs_high)
            if ref_abs_low is not None:
                self.write('MEASUrement:REFLevel:ABSolute:LOW {}', ref_abs_low)
            if ref_abs_mid is not None:
                self.write('MEASUrement:REFLevel:ABSolute:MID1 {}', ref_abs_mid)

        if ref_per_mid is not None:
            self.write('MEASUrement:REFLevel:PERCent:MID1 {}', ref_per_mid)
        if ref_per_high is not None:
            self.write('MEASUrement:REFLevel:PERCent:HIGH {}', ref_per_high)
        if ref_per_low is not None:
            self.write('MEASUrement:REFLevel:PERCent:LOW {}', ref_per_low)
        if Mdo3000Cmd.REG_DELAY.search(meas_type) is not None \
                or Mdo3000Cmd.REG_PHASE.search(meas_type) is not None:
            target = measure.get('target')
            assert target is not None, 'the delay or phase measurement must be contains key named "target"'
            self.write('MEASUrement:IMMed:SOUrce2 {}', target)

            #             if meas_type in Mdo3000Cmd.DELAY_LIST:
            if Mdo3000Cmd.REG_DELAY.search(meas_type) is not None:
                direction = measure.get('direction')  # , 'FORWards')
                sour_edge = measure.get('sour_edge')  # , 'RISe')
                targ_edge = measure.get('targ_edge')  # , 'RISe')

                targ_ref_abs_mid = measure.get('targ_ref_abs_mid')  # , 0.0E+0)
                targ_ref_per_mid = measure.get('targ_ref_per_mid')  # , 50.)

                if direction is not None:
                    self.write('MEASUrement:IMMed:DELay:DIRection {}', direction)
                if sour_edge is not None:
                    self.write('MEASUrement:IMMed:DELay:EDGE1 {}', sour_edge)
                if targ_edge is not None:
                    self.write('MEASUrement:IMMed:DELay:EDGE2 {}', targ_edge)
                if targ_ref_abs_mid is not None:
                    self.write('MEASUrement:REFLevel:ABSolute:MID2 {}', targ_ref_abs_mid)
                if targ_ref_per_mid is not None:
                    self.write('MEASUrement:REFLevel:PERCent:MID2 {}', targ_ref_per_mid)

    """======================================================================================== """

    def pause(self, sleep_time=0.0):
        """
        设置示波器停止接受指令的时间
        :param sleep_time: (type float) 止接受指令的时间, 单位s
        :return:
            None
        """
        self.write('PAUSe {}', sleep_time)
        time.sleep(sleep_time)

    """======================================================================================== """

    def horizontal_setting(self, *names, **values):
        """
        示波器水平设置, 包含显示延迟开关, 显示延迟时间设置, 水平位置, 记录长度, 采样率和水平缩放
        :param names: (type tuple) 查询相关值, 可选值如下:
                del_state: 显示延迟开关
                delay: (延迟开启的)显示延迟时间, 单位为s
                pos: (延迟关闭的)水平位置, 单位为相对百分数
                rec_len: 记录长度
                sam_rate: 采样率
                scale: 水平缩放
        :param values: (type dict) 设置字典, 说明如下:
                del_state (type str): 显示延迟开关, 可选值 {ON|1|OFF|0}
                delay (type float): (延迟开启的)显示延迟时间, 单位为s, 当del_state为OFF时无效
                pos (type float): (延迟关闭的)水平位置, 单位为相对百分数, 当del_state为ON时无效
                rec_len (type float): 记录长度, 示波器支持的值
                sam_rate  (type float): 采样率, 示波器支持的值
                scale (type float): 水平缩放, 单位s, 表示s/div
        :return:
            (type str) 依次返回names中查询的值, 以分号(;)分割
        """
        write_cmd = None
        for key, value in values.items():
            write_cmd = utils.contact_spci_cmd(write_cmd, Mdo3000Cmd.HORIZONTAL_SET_DICT.get(key), value)
        self.write(write_cmd)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, Mdo3000Cmd.HORIZONTAL_GET_DICT.get(name))
        return self.query(query_cmd)

    # def histogram_setting(self, *names, **values):
    #     """
    #     直方图设置
    #     :rtype: str
    #     :param names: (type tuple) 查询相关的值, 可选值:
    #         box:        直方图框坐标
    #         box_pcnt:   以源波形的全屏范围的百分比形式直方图框坐标
    #         data:       直方图数据
    #         disp:       直方图显示的比例
    #         end:        直方图的最后一个bin的时间
    #         mode:       直方图的类型{HORizontal|VERTical|OFF}
    #         source:     用于创建直方图的源
    #         start:      直方图的第一个bin的时间
    #     :param values: (type dict) 设置相关参数值
    #         box (type tuple or list of float):
    #             根据源波形的垂直和水平单位设置直方图框坐标
    #         box_pcnt (type tuple or list of float):
    #             设置直方图框距离屏幕左, 上, 右, 下的百分比
    #         count (type str):
    #             清除直方图计数和统计信息, 可选值 {RESET}
    #         disp (type str):
    #             直方图数据显示的缩放比例, 可选值 {OFF|LOG|LINEAr}
    #             OFF: 关闭
    #             LOG: 对数缩放
    #             LINEAr: 直线缩放(默认值)
    #         mode (type str):
    #             直方图显示类型, 可选值 {HORizontal|VERTical|OFF}
    #             HORizontal: 水平
    #             VERTical: 垂直
    #             OFF: 关闭
    #         source (type str):
    #             设置用于创建直方图的源, 可选值 {CH<x>|MATH|REF<x>}
    #     :return: (type str)
    #         相关查询的参数, 以分号(;)分割
    #     """
    #     pass

    """======================================================================================== """

    def show_message(self, msg=None, x=0, y=0):
        """
        在示波器屏幕上显示数据
        :param msg: (type str) 需要显示的信息, 为None时表示清除并关闭显示
        :param x: (type float) 需要显示的信息在屏幕上x轴的位置, 屏幕x坐标范围 0-1023
        :param y: (type float) 需要显示的信息在屏幕上x轴的位置, 屏幕x坐标范围 0-767
        :return:
            (type str): 信息显示状态, 屏幕显示的信息(当msg不为None时), 以分号(;)分割
        """
        if msg is not None:
            self.write('MESSage:SHOW "{}"', msg)
            self.write('MESSage:BOX {},{}', x, y)
            self.write('MESSage:STATE ON')
            self.write('MESSage:STATE?;:MESSage:SHOW?')
        else:
            self.write('MESSage:CLEAR;:MESSage:STATE OFF;:MESSage:STATE?')
        return self.read()

    """======================================================================================== """

    def screen_shot(self, f_path, f_type='PNG', inksaver='ON', sleep=1.):
        """
        屏幕截取
        :param f_path: (type str) 屏幕截取的图片文件保存路径
        :param f_type: (type str) 屏幕截取的图片文件格式, MDO3000系列支持png, bmp and tif三种图片格式
        :param inksaver: (type str) 屏幕截取的图片省墨模式, 可选值{ON|OFF}
        :param sleep: (type float) 屏幕截图时延迟时间
        :return:
            (type str): 保存的图片文件名(当前上位机日期时间, 不包含路径)
        """
        self.write('SAVe:IMAGe:FILEFormat {};:SAVe:IMAGe:INKSaver {};:HARDCopy STARt', f_type, inksaver)
        time.sleep(sleep)
        img_data = self._instrument.read_raw()

        dt = datetime.now()
        file_name = dt.strftime("%Y%m%d%H%M%S%f.{}".format(f_type))
        #         print(len(img_data))
        self._logger.debug('the image size %d', len(img_data))

        with open(f_path + file_name, "wb") as img_file:
            img_file.write(img_data)
        return file_name

    """======================================================================================== """

    def language(self, lang=None):
        """
        设置示波器人机交互语言
        :param:
            lang (type str): 支持的语言:
                {ENGLish|FRENch|GERMan|ITALian|SPANish|PORTUguese|JAPAnese|KOREan|RUSSian|SIMPlifiedchinese|TRADitionalchinese}
        :return:
            (type str): 当前示波器人机交互语言
        """
        if lang is not None:
            self.write('LANGuage {}', lang)
        return self.query('LANGuage?')

    """======================================================================================== """

    def waveform_export(self, source, start=1, points=None):
        """
        导出示波器当前波形采样的点
        :param source: (type str) 需要导出波形的信号源
            可选值 {CH<x>|MATH|REF<x>|BUS<x>|D<x>|RF_AMPlitude|RF_FREQuency|RF_PHASe|RF_NORMal|RF_AVErage| RF_MAXHold|RF_MINHold}
        :param start: (type int) 需要采集的开始点, 范围 1 ~ (记录长度-1), 默认从 1 开始
        :param points: (type int) 需要采集的点的个数, 范围 大于开始点 小于记录长度, 不指定则默认到最后一个点
        :return:
            (type list): 采集点的x轴坐标单位(占一个元素) + x轴点的数据
            (type list): 采集点的y轴坐标单位(占一个元素) + y轴点的数据
        """
        inst_points = int(self.horizontal_setting('rec_len'))
        self._logger.info('The instrument record length is %d', inst_points)
        if points is None \
                or points > inst_points:
            points = inst_points

        _start = (start - 1)

        cmd = 'DATa:SOUrce {};:DATa:START {};:DATa:STOP {};:DATa:ENCdg SRIBINARY;:HEADer OFF'
        self.write(cmd, source, start, (points - _start))

        # info = self.query('DATa?')
        # self._logger.info('DATa: \n%s', info)
        # info = self.query('WFMInpre?')
        # self._logger.info('WFMInpre: \n%s', info)
        # info = self.query('WFMOutpre?')
        # self._logger.info('WFMOutpre: \n%s', info)

        # 时间转换
        x_unit = self.query('WFMOutpre:XUNit?')
        x_zero = float(self.query('WFMOutpre:XZEro?'))
        x_incr = float(self.query('WFMOutpre:XINcr?'))

        y_unit = self.query('WFMOutpre:YUNit?')
        y_zero = float(self.query('WFMOutpre:YZEro?'))
        y_mult = float(self.query('WFMOutpre:YMUlt?'))

        self.write('CURVe?')
        data = self._instrument.read_raw()

        # data start of '#' ascii is 0x23
        data_start = data[0]
        assert 0x23 != data_start, 'error start of data'

        # numbers of data length ascii  - ascii(0)
        data_len_num = data[1] - 0x30
        self._logger.info('number of data length is %d', data_len_num)
        # get data length, assert it equals points
        data_len = 0
        for i in range(data_len_num):
            # calculator the actual length of data
            data_len += (10 ** (data_len_num - i - 1)) * (data[i + 2] - 48)
        if int(data_len) != points:
            self._logger.error('error data length, not equal "points(%d)"', points)
        #         assert int(data_len) != points, 'error data length, not equal "points(0x%s)"'%'%02x'%points

        _data_len = len(data) - 1
        data_end = data[_data_len]
        if 0x0a != data_end:
            self._logger.error('error end of data 0x%s, expect 0x0a', '%02x' % data_end)
        #         assert 0x0a != data_end, 'error end of data 0x%s, expect 0x0a'%'%02x'%data_end

        data_x = [x_unit]
        data_y = [y_unit]

        # the length of head
        x = data_len_num + 2
        for i in range(_data_len - x):
            data_i = data[i + x]
            data_x.append(x_zero + x_incr * i)
            data_y.append(y_zero + y_mult * COMPLEMENT[data_i])
        self._logger.info('data x size: %d', len(data_x))
        self._logger.info('data y size: %d', len(data_y))

        return data_x, data_y

    """======================================================================================== """

    def show_channel(self, **values):
        """
        开启波形显示
        :param values: (type dict) 设置显示波形的字典, 说明如下:
                key可以是 CH<x>, D<x>, DALL, MATH, REF<x>, RF_AM Plitude, RF_AVErage, RF_FREQuency, RF_MAXHold, RF_MINHold, RF_NORMal, RF_PHASe
                value (type str): 可选值{ON|1|OFF|0}
        :return:
            当前values字典中指定的key通道的波形显示状态
        """
        write_cmd = None
        query_cmd = None
        for key, value in values.items():
            write_cmd = utils.contact_spci_cmd(write_cmd, 'SELect:{} {}', key, value)
            query_cmd = utils.contact_spci_cmd(query_cmd, 'SELect:{}?', key)

        self.write(write_cmd)
        time.sleep(0.5)
        return self.query(query_cmd)

    """======================================================================================== """

    def select_control(self, channel):
        """
        选择一个波形用于通道相关操作, 比如光标操作
        :param channel: (type str) 通道名, 可选值
                {CH<x>|MATH|REF<x>|BUS<x>|D<x>|RF_AMPlitude|RF_FREQuency|RF_PHASe|RF_NORMal|RF_AVErage| RF_MAXHold|RF_MINHold}
        :return:
            当前所选的通道名
        """
        self.write('SELect:CONTROl {}', channel)
        return self.query('SELect:CONTROl?')

    """======================================================================================== """

    def trigger_setting(self, source, level, trig_type='edge', roll_mode='AUTO', hold_off=20.0E-9, **values):
        """
        触发操作参数设置查询(当前不支持总线(BUS)触发)
        :param source: (type str) 设置触发信号源, 可选值
                {CH<x>|MATH|REF<x>|BUS<x>|D<x>|RF_AMPlitude|RF_FREQuency|RF_PHASe|RF_NORMal|RF_AVErage| RF_MAXHold|RF_MINHold}
        :param level: (type float) 设置触发的门限电压值
        :param trig_type: (type str) 设置触发类型, 可选值 {edge|logic|pulse|bus|video},
                分别表示 沿触发 逻辑触发 脉宽触发 总线(BUS)触发 视频触发
        :param roll_mode: (type str) 设置滚动模式, 可选值 {AUTO|NORMal}, 分别表示 自动滚动 正常
        :param hold_off: (type float) 设置释抑时间(hold off time), 单位s, 范围 20.0E-9 ~ 8
        :param values: (type dict): 其他参数设置字典, 说明如下:

                当trig_type为edge时, 字典键值说明:
                    b_state (type str): (optional) B触发状态, 可选值 {ON|OFF|1|0}
                    coup (type str): (optional) 耦合方式, 可选值 {DC|AC|HFRej|LFRej|NOISErej}
                    slope (type str): (optional) 触发沿方式,
                        当关闭B触发时(即b_state为OFF或0), 可选值 {RISe|FALL|EITHer}
                        当开启B触发时(即b_state为ON或1), 可选值 {RISe|FALL}
                    trig_by (type str): (must if b_state is ON) B触发方式, 可选值 {EVENTS|TIMe}
                    count (type int): (optional) B触发时事件触发计数器(trig_by为EVENTS), 当设置为B触发且B触发方式为EVENTS时有效
                    delay (type float): (optional) B触发时延迟时间(trig_by为TIMe), 单位s, 最小值0.8E-9, 当设置为B触发且B触发方式为TIMe时有效

                当trig_type为logic时, 字典键值说明:
                    kind (type str): (must) 指定使用触发的逻辑类型, 可选值 {LOGIC|SETHold}
                    func (type str) (must if kind is LOGIC): 逻辑输入通道的计算方式, 可选值 {AND|NANd|NOR|OR}, 当逻辑触发类型设置为LOGIC时有效
                    cond (type str): (optional) 通道的逻辑输入条件, 可选值 {HIGH|LOW|X}, 当逻辑触发类型设置为LOGIC时有效
                    clk_sour (type str): (must if kind is SETHold) 逻辑触发的时钟信号源(不能与信号源同一通道), 可选值 {CH<x>|D<x>|RF|NONE},
                            当设置为NONE时, 表示选择模式触发器
                    clk_edge (type str): (optional) 时钟通道沿的方向, 可选值 {FALL|RISe}, 当clk_sour为NONE时忽略此命令
                    delta (type float): (optional) 模式触发器增量时间值, 时间值用作模式触发条件的一部分，以确定逻辑模式的持续时间是否满足指定的时间约束
                            仅选择逻辑触发时且当clk_sour为NONE时有效
                    when (type str): (optional) 模式触发器的逻辑条件, 可选值 {TRUe|FALSe|LESSthan|MOREthan|EQual|UNEQual}
                    thr (type float or str): (optional) 逻辑触发的通道电压阈值, 可选值 {<NR3>|ECL|TTL}(NR3为float)
                    data_thr (type float or str): (optional) 设置和保持逻辑触发的电压阈值, 可选值 {<NR3>|TTL}(NR3为float)
                            仅在逻辑触发类型(kind)为SETHold时有效
                    clk_thr (type float or str): (optional) 设置和保持逻辑触发时钟电压阈值, 可选值 {<NR3>|TTL}(NR3为float)
                            仅在逻辑触发类型(kind)为SETHold时有效
                    hold_time (type float): (optional) 设置和保持逻辑触发保持时间
                            仅在逻辑触发类型(kind)为SETHold时有效
                    set_time (type float): (optional) 设置和保持逻辑触发的冲突时间
                            仅在逻辑触发类型(kind)为SETHold时有效

                当trig_type为pulse时, 字典键值说明:
                    kind (type str): (must) 指定触发脉宽类型, 可选值为 {RUNt|WIDth|TRANsition|TIMEOut}
                    width (type float): (optional) 指定脉宽时间, 单位s, 仅kind为RUNt或WIDth有效
                    when (type str): (optional) 指定触发时间点, 可选值
                            当kind为RUNt时, {LESSthan|MOREthan|EQual|UNEQual|OCCURS}
                            当kind为WIDth时, {LESSthan|MOREthan|EQual|UNEQual|WIThin|OUTside}
                            当kind为TRANsition时, {SLOWer|FASTer|EQual|UNEQual}
                            当kidn为TIMEOut时, 无效
                    high_lim (type float): (optional) 指定两个值范围之内或之外的脉冲持续时间上限, 单位s, 仅kind为WIDth有效
                    low_lim (type float): (optional) 指定两个值范围之内或之外的脉冲持续时间下限, 单位s, 仅kind为WIDth有效
                    pola (type str): (optional) 指定触发脉冲的极性, 可选值
                            当kind为RUNt时, {EITher|NEGative|POSitive}
                            当kind为WIDth时, {NEGative|POSitive}
                            当kind为TRANsition时, {EITher|NEGative|POSitive}
                            当kidn为TIMEOut时, {STAYSHigh|STAYSLow|EITher}
                    delta (type float): (optional) 指定用于计算转换值的增量时间, 单位s, 仅kind为TRANsition有效
                    upper_thr (type str or float) (optional): 指定通道的门限上限值, 可选值 {<NR3>|ECL|TTL}, 仅kind为RUNt或TRANsition有效
                    lower_thr (type str or float) (optional): 指定通道的门限下限值, 可选值 {<NR3>|ECL|TTL}, 仅kind为RUNt或TRANsition有效
                    timeout (type float) (optional): 指定超时时间, 单位s, 仅kind为RUNt或TIMEOut有效

                当trig_type为bus时, 由于硬件不支持, 会抛出异常

                当trig_type为video时, 字典键值说明:
                    std (type str): (optional) 触发信号使用的视频的标准, 可选值
                        {NTSc|PAL|SECAM|BILevelcustom|TRILevelcustom| HD480P60|HD576P50|HD720P30|HD720P50
                        |HD720P60|HD875I60|HD1080P24|HD1080SF24|HD1080I50|HD1080I60|HD1080P25|HD1080P30|HD1080P50|HD1080P60}
                    field (type float): (optional) 根据视频字段设置视频触发释抑，用于触发视频信号, 范围 0.0 ~ 8.5, 增量 0.5
                    line (type int): (optional) 设置用于触发视频信号的特定视频行号, 但是必须指定sync为NUMERic
                    pola (type str): (optional) 用于触发视频信号的极性, 可选值 {NEGative|POSitive}
                    sync (type str): (optional) 设置触发视频信号的视频字段, 可选值 {ODD|EVEN|ALLFields|ALLLines|NUMERic}
                        ODD: 设置示波器在隔行视频奇数场上触发
                        EVEN: 设置示波器在隔行视频偶数场上触发
                        ALLFields: 将示波器设置为在所有字段上触发
                        ALLLines: 将示波器设置为在所有行上触发
                        NUMERic: 设置示波器在line指定的视频信号线上触发
                    cust_type (type str): 设置视频触发格式, 当std设置为BILevelcustom或TRILevelcustom有效, 可选值 {INTERLAced|PROGressive}
                    line_per (type float): 设置被测标准的行周期, 单位s, 当std设置为BILevelcustom或TRILevelcustom有效
                    sync_int (type float): 设置用于触发视频信号被测标准的同步间隔, 以用于触发视频信号, 单位s, 当std设置为BILevelcustom有效
        :return:
            (type str) 当前的触发设置
        """
        assert source is not None, 'required correct channel'
        assert trig_type in Mdo3000Cmd.TRIG_TYPE_TUPLE, 'required correct trig_type in %s' % Mdo3000Cmd.TRIG_TYPE_TUPLE.__str__()
        assert Mdo3000Cmd.REG_TRIG_MODE.search(roll_mode) is not None, 'required correct trig_mode in {AUTO|NORMal}'
        assert hold_off is not None, 'required correct value of hold off time'
        assert level is not None, 'required correct value of trigger level'
        # assert low_threshold is not None, 'required correct value of low threshold'
        self.write('TRIGger:A:MODe {}', roll_mode)
        self.write('TRIGger:A:HOLDoff:TIMe {}', hold_off)
        self.write('TRIGger:A:LEVel:{} {}', source, level)

        # self.write('TRIGger:A:LOWerthreshold:{} {}', source, low_threshold))

        def edge():
            self.write('TRIGger:A:TYPe {}', 'EDGe')
            b_state = values.get('b_state')

            coup = values.get('coup')
            slope = values.get('slope')

            if b_state in TUPLE_ON:
                self.write('TRIGger:B:STATE {}', 'ON')
                self.write('TRIGger:B:EDGE:SOUrce {}', source)
                if coup is not None:
                    self.write('TRIGger:B:EDGE:COUPling {}', coup)
                if slope is not None:
                    self.write('TRIGger:B:EDGE:SLOpe {}', slope)

                trig_by = values.get('trig_by', 'EVENTS')

                if Mdo3000Cmd.REG_TRIG_BY_EVENTS.search(trig_by):
                    count = values.get('count')
                    if count is not None:
                        self.write('TRIGger:B:EVENTS:COUNt {}', count)

                elif Mdo3000Cmd.REG_TRIG_BY_TIME.search(trig_by):
                    time_value = values.get('delay')
                    if time_value is not None:
                        self.write('TRIGger:B:TIMe {}', time_value)
                else:
                    raise ParamException('The B trigger "trig_by" must be "events" or "tim(e)", ignore case')

                self.write('TRIGger:B:BY {}', trig_by)

            else:
                self.write('TRIGger:B:STATE {}', 'OFF')
                self.write('TRIGger:A:EDGE:SOUrce {}', source)
                if coup is not None:
                    self.write('TRIGger:A:EDGE:COUPling {}', coup)
                if slope is not None:
                    self.write('TRIGger:A:EDGE:SLOpe {}', slope)
            return self.query('TRIGger:A:EDGE?')

        def logic():
            self.write('TRIGger:A:TYPe {}', 'LOGIc')
            kind = values.get('kind')

            if Mdo3000Cmd.REG_LOGICC_LOGIC.search(kind) is not None:
                """"
                TRIGger:A:LOGIc:FUNCtion , 
                TRIGger:A:LOGIc:INPut:CH<x> , 
                TRIGger:A:LOGIc:INPut:CLOCk:EDGE , 
                TRIGger:A:LOGIc:INPut:CLOCk:SOUrce , 
                TRIGger:A:LOGIc:INPut:D<x> ,
                TRIGger:A:LOGIc:INPut:RF , 
                TRIGger:A:LOGIc:PATtern:DELTatime(without clock source)
                """
                # self.write('TRIGger:A:LOGIc:INPut:CH<x>')
                func = values.get('func')
                assert func is not None, 'required correct logic function to logic trigger'
                cond = values.get('cond', 'X')
                self.write('TRIGger:A:LOGIc:INPut:{} {}', source, cond)
                clk_sour = values.get('clk_sour')
                if clk_sour is not None:
                    self.write('TRIGger:A:LOGIc:INPut:CLOCk:SOUrce {}', clk_sour)
                    clk_edge = values.get('clk_edge')
                    if clk_edge is not None:
                        self.write('TRIGger:A:LOGIc:INPut:CLOCk:EDGE {}', clk_edge)
                else:
                    self.write('TRIGger:A:LOGIc:INPut:CLOCk:SOUrce {}', "NONE")
                    delta = values.get('delta')
                    if delta is not None:
                        self.write('TRIGger:A:LOGIc:PATtern:DELTatime {}', delta)

                when = values.get('when')
                if when is not None:
                    self.write('TRIGger:A:LOGIc:PATtern:WHEn {}', when)
                thr = values.get('thr')
                if thr is not None:
                    self.write('TRIGger:A:LOGIc:THReshold:{} {}', source, thr)

            elif Mdo3000Cmd.REG_LOGICC_SETHOLD.search(kind) is not None:
                """"
                TRIGger:A:SETHold:CLOCk:EDGE ,
                TRIGger:A:SETHold:CLOCk:SOUrce , 
                TRIGger:A:SETHold:CLOCk:THReshold , 
                TRIGger:A:SETHold:DATa:SOUrce, 
                TRIGger:A:SETHold:DATa:THReshold , 
                TRIGger:A:SETHold:HOLDTime , 
                TRIGger:A:SETHold:SETTime ,
                TRIGger:A:SETHold:THReshold:CH<x> ,
                TRIGger:A:SETHold:THReshold:D<x>
                """
                # data_sour = values.get('data_sour')
                clk_sour = values.get('clk_sour')
                # assert data_sour is not None, 'required correct data source channel'
                assert clk_sour is None, 'required correct clock source channel'
                assert clk_sour == source, 'cann\'t the same source for both clock and data'

                self.write('TRIGger:A:SETHold:DATa:SOUrce {}', source)
                self.write('TRIGger:A:SETHold:CLOCk:SOUrce {}', clk_sour)

                data_thr = values.get('data_thr')
                clk_edge = values.get('clk_edge')
                clk_thr = values.get('clk_thr')
                hold_time = values.get('hold_time')
                set_time = values.get('set_time')
                thr = values.get('thr')

                if data_thr is not None:
                    self.write('TRIGger:A:SETHold:DATa:THReshold {}', data_thr)
                if clk_edge is not None:
                    self.write('TRIGger:A:SETHold:CLOCk:EDGE {}', clk_edge)
                if clk_thr is not None:
                    self.write('TRIGger:A:SETHold:CLOCk:THReshold {}', clk_thr)
                if hold_time is not None:
                    self.write('TRIGger:A:SETHold:HOLDTime {}', hold_time)
                if set_time is not None:
                    self.write('TRIGger:A:SETHold:SETTime {}', set_time)
                if thr is not None:
                    self.write('TRIGger:A:SETHold:THReshold:{} {}', source, thr)
            else:
                raise ParamException('The logic class must be "logic" or "seth(old)", ignore case')

            self.write('TRIGger:A:LOGIc:CLAss {}', kind)
            return self.query('TRIGger:A:LOGIc?')

        def pulse():
            self.write('TRIGger:A:TYPe {}', 'PULSe')
            kind = values.get('kind')

            if Mdo3000Cmd.REG_PULSEC_RUNT.search(kind) is not None:
                # runt
                self.write('TRIGger:A:RUNT:SOUrce {}', source)
                pola = values.get('pola')
                width = values.get('width')
                when = values.get('when')
                upper_thr = values.get('upper_thr')
                lower_thr = values.get('lower_thr')

                if pola is not None:
                    self.write('TRIGger:A:RUNT:POLarity {}', pola)
                if width is not None:
                    self.write('TRIGger:A:RUNT:WIDth {}', width)
                if when is not None:
                    self.write('TRIGger:A:RUNT:WHEn {}', when)
                if upper_thr is not None:
                    self.write('TRIGger:A:UPPerthreshold:{} {}', source, upper_thr)
                if lower_thr is not None:
                    self.write('TRIGger:A:LOWerthreshold:{} {}', source, lower_thr)
                return self.query('TRIGger:A:RUNT?')

            elif Mdo3000Cmd.REG_PULSEC_WIDTH.search(kind) is not None:
                # pulse width
                self.write('TRIGger:A:PULSEWidth:SOUrce {}', source)
                high_lim = values.get('high_lim')
                low_lim = values.get('low_lim')
                pola = values.get('pola')
                width = values.get('width')
                when = values.get('when')

                if high_lim is not None:
                    self.write('TRIGger:A:PULSEWidth:HIGHLimit {}', high_lim)
                if low_lim is not None:
                    self.write('TRIGger:A:PULSEWidth:LOWLimit {}', low_lim)
                if pola is not None:
                    self.write('TRIGger:A:PULSEWidth:POLarity {}', pola)
                if width is not None:
                    self.write('TRIGger:A:PULSEWidth:WIDth {}', width)
                if when is not None:
                    self.write('TRIGger:A:PULSEWidth:WHEn {}', when)
                return self.query('TRIGger:A:PULSEWidth?')

            elif Mdo3000Cmd.REG_PULSEC_TRANSITION is not None:
                self.write('TRIGger:A:TRANsition:SOUrce {}', source)
                delta = values.get('delta')
                pola = values.get('pola')
                when = values.get('when')
                upper_thr = values.get('upper_thr')
                lower_thr = values.get('lower_thr')

                if delta is not None:
                    self.write('TRIGger:A:TRANsition:DELTatime {}', delta)
                if pola is not None:
                    self.write('TRIGger:A:TRANsition:POLarity {}', pola)
                if when is not None:
                    self.write('TRIGger:A:TRANsition:WHEn {}', when)
                if upper_thr is not None:
                    self.write('TRIGger:A:UPPerthreshold:{} {}', source, upper_thr)
                if lower_thr is not None:
                    self.write('TRIGger:A:LOWerthreshold:{} {}', source, lower_thr)
                return self.query('TRIGger:A:TRANsition?')

            elif Mdo3000Cmd.REG_PULSEC_TIMEOUT(kind) is not None:
                self.write('TRIGger:A:TIMEOut:SOUrce {}', source)
                pola = values.get('pola')
                time_value = values.get('timeout')

                if pola is not None:
                    self.write('TRIGger:A:TIMEOut:POLarity {}', pola)
                if time_value is not None:
                    self.write('TRIGger:A:TIMEOut:TIMe {}', time_value)
                return self.query('TRIGger:A:TIMEOut?')
            else:
                raise ParamException(
                    'The pulse class must be "run(t)" or "wid(th)" or "tran(sition)" or "timeo(ut)", ignore case')

        def bus():
            raise InstrumentException('The bus trigger not supported as required bus module')

        def video():
            warnings.warn(
                'MDO4000 series requires a DPO4VID application module to use any standard besides NTSc, PAL, or SECAM')
            self.write('TRIGger:A:TYPe {}', 'VIDeo')
            self.write('TRIGger:A:VIDeo:SOUrce {}', source)

            std = values.get('std')
            #             assert std is not None, 'The video standard required'
            if std is not None:
                self.write('TRIGger:A:VIDeo:STANdard {}', std)

            field = values.get('field')
            line = values.get('line')
            pola = values.get('pola')
            sync = values.get('sync')
            if field is not None:
                self.write('TRIGger:A:VIDeo:HOLDoff:FIELD {}', field)
            if line is not None:
                self.write('TRIGger:A:VIDeo:LINE {}', line)
            if pola is not None:
                self.write('TRIGger:A:VIDeo:POLarity {}', pola)
            if sync is not None:
                self.write('TRIGger:A:VIDeo:SYNC {}', sync)

            if Mdo3000Cmd.REG_VIDEO_CUSTOM.search(std):
                cust_type = values.get('cust_type')
                line_per = values.get('line_per')
                if cust_type is not None:
                    self.write('TRIGger:A:VIDeo:CUSTom:FORMat {}', cust_type)
                if line_per is not None:
                    self.write('TRIGger:A:VIDeo:CUSTom:LINEPeriod {}', line_per)
                if Mdo3000Cmd.REG_VIDEO_BILEVEL_CUST.search(std):
                    sync_int = values.get('sync_int')
                    if sync_int is not None:
                        self.write('TRIGger:A:VIDeo:CUSTom:SYNCInterval {}', sync_int)
            return self.query('TRIGger:A:VIDeo?')

        switch = {'edge': edge, 'logic': logic, 'pulse': pulse, 'bus': bus, 'video': video}
        return switch.get(trig_type, lambda: utils.raiser(ParamException('Invalid trig_type')))()

    """======================================================================================== """

    def trigger_setlevel(self):
        """
        设置触发信号为当前采集的最大值和最小值差的50%, 相当于前面板操作的setlevel
        :return:
            None
        """
        self.write('TRIGger:A SETLevel')
        self.pause(0.01)
    # time.sleep(0.01)

    """======================================================================================== """

    def trigger_force(self):
        """
        强制触发信号, 当trigger_status为READy时, 示波器才会采集数据, 否则此命令将会被忽略
        :return:
             None
        """
        self.write('TRIGger FORCe')

    """======================================================================================== """

    # def is_triggered(self):
    #     """
    #     return True if is triggered else False
    #     """
    #     s = self.trigger_status()
    #     if 'TRIGGER\n' == s:
    #         return True
    #     elif 'AUTO\n' == s:
    #         return False
    #     elif 'READY\n' == s:
    #         return False
    #     else:
    #         self._logger.error('TRIGger:STATe? return string: %s', s)

    """======================================================================================== """

    def trigger_status(self):
        """
        获取当前触发状态
        get the trigger status string
        :return: (type str)
            ARMED: 表示明波器正在获取预触发信息
                indicates that the oscilloscope is acquiring pre_trigger information.
            AUTO: 表示示波器处于自动模式, 即使在没有触发器的情况下也能获取数据
                indicates that the oscilloscope is in the automatic mode and acquires data even in the absence of a trigger.
            READY: 表示已获取所有预触发信息, 示波器已准备好接受触发
                indicates that all pre_trigger information has been acquired and that the oscilloscope is ready to accept a trigger.
            SAVE: 表示示波器处于保存模式且未采集数据
                indicates that the oscilloscope is in save mode and is not acquiring data.
            TRIGGER: 表示示波器已触发并正在获取触发后信息。
                indicates that the oscilloscope triggered and is acquiring the post trigger information.
        """
        s = self.query('TRIGger:STATe?')
        self._logger.debug('TRIGger:STATe? return string: %s', s)
        return s

    """======================================================================================== """

    def zoom(self, *names, **values):
        """
        缩放搜索
        :param names: (type tuple) 参数查询
                FACtor: 缩放框缩放系数
                POSition: 缩放框的水平位置，以0到100.0%的上窗口为单位
                SCAle: 缩放框的水平比例
                STATE: 缩放框的开启状态
                TRIGPOS: 此查询返回缩放框中心相对于当前选定时域波形的触发位置的时间
        :param values: (type dict) 设置参数, 字典说明如下:
                POSition (type float): 设置缩放框的水平位置，范围0-100(百分比)
                SCAle (type float): 设置缩放框的水平比例
                STATE (type str): 设置缩放框的开启状态, 可选值{ON|OFF}
        :return:
            (type str): 依次返回names中指定的查询值, 以分号(;)分割
        """
        for key, value in values.items():
            self.write('ZOOm:{} {}' if Mdo3000Cmd.REG_STATE.search(key) is not None else 'ZOOm:ZOOM1:{} {}', key,
                       value)

        query_cmd = None
        for name in names:
            query_cmd = utils.contact_spci_cmd(query_cmd, 'ZOOm:{}?' if Mdo3000Cmd.REG_STATE.search(
                'state') is not None else 'ZOOm:ZOOM1:{}?', name)
        return self.query(query_cmd)

    """======================================================================================== """

    def config_query(self, *configs):
        """
        查询示波器内部配置的功能模块或参数
        :param configs: (type tuple) 可选的功能模块或参数名称如下:
                adv_math:       数学计算
                afg:            任意函数发生器(AFG)
                bandwidth:      模拟通道带宽, 单位Hz
                gnd_cplg:       模拟信道的接地耦合
                samp_rate:      模拟通道的最大采样率
                num_ch:         模拟通道数
                rec_len:        模拟通道可支持的记录长度, 以逗号(,)分割
                vert_inv:       模拟信道的垂直反转
                cust_mask:      自定义掩码测试
                limit_mask:     掩码/极限测试
                power:          可选电源应用
                std_mask:       标准掩码测试
                vid_pic:        视频图片处理
                arb:            AFG下的任意波发生器(ARB)
                aux_in:         辅助输入连接器(AUX)
                mag:            数字通道的MagniVu
                dig_samp_rate:  数字通道的最大采样率
                dig_num_ch:     数字通道个数
                dvm:            数字电压表(DVM)
                ext_video:      附加视频处理
                hist:           波形统计
                net_drv:        网卡
                num_meas:       最大周期测量次数
                num_ref:        可引用波形数
                adv_trig:       高级RF触发和分析
                rf_bandw:       RF通道带宽
                rf_num_ch:      RF通道数
                rosc:           外部参考振荡器（ROSC）
        :return:
            (type str): 查询的示波器内部配置的功能模块(已安装该模块为1, 否则为0)或参数(具体的参数值)
        """
        query_cmd = None
        for config in configs:
            query_cmd = utils.contact_spci_cmd(query_cmd, Mdo3000Cmd.CONFIG_DICT.get(config))
        #         if query_cmd is not None:
        return self.query(query_cmd)

    """======================================================================================== """

    def ddt(self, cmd=None):
        """
        自定义一个触发发生后执行的指令
        :param cmd: (type str) SCPI指令, 字符长度不超过80
        :return:
            (type str): 当前定义的指令
        """
        if len(cmd) > 80:
            raise ParamException('the define command string over than 80 characters')

        if cmd is not None:
            self.write('*DDT #{}', cmd)
        return self.query('*DDT?')

    """======================================================================================== """

    def setup_save_recall(self, op, path):
        """
        保存和调用示波器设置, 文件名一般用.SET格式
        :param op: (type str) 保存或调用操作, 可选值 {save|recall|recall_demo}
                分别表示 保存文件或编号 调用已保存文件或编号 调用demo设置
        :param path: (type str or int)
                文件路径或者编号或被调用的demo编号
                文件路径盘符:
                    E: 表示前面板第一个USB口的U盘
                    F: 表示前面板第二个USB口的U盘(MDO3000系列没有)
                    G/H: 表示后面的USB口的U盘
                    I: 表示一个网络路径
                保存设置编号范围 1-10
                调用设置编号范围 1-10以及FACtory(出厂设置值)
                调用demo编号范围 1-22
        :return:
            None
        """
        if 'save' == op:
            self.write('SAVe:SETUp {}', path)
        elif 'recall' == op:
            self.write('RECAll:SETUp {}', path)
        elif 'recall_demo' == op:
            self.write('RECAll:SETUp:DEMO{}', path)
        else:
            self._logger.warn('not supported save and recall operation')








