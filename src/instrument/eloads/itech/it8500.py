# -*- encoding: utf-8 -*-
"""
@File    : it8500.py
@Time    : 2020/8/17 11:58
@Author  : blockish
@Email   : blockish@yeah.net
"""
import warnings
from abc import abstractmethod


class It85xx:

    def __init__(self):
        self._max_volt = None
        self._min_volt = None
        self._max_curr = None
        self._max_power = None
        self._max_res = None
        self._min_res = None

    @property
    def max_voltage(self):
        return self._max_volt

    @property
    def min_voltage(self):
        return self._min_volt

    @property
    def max_current(self):
        return self._max_curr

    @property
    def max_power(self):
        return self._max_power

    @property
    def max_resistance(self):
        return self._max_res

    @property
    def min_resistance(self):
        return self._min_res

    @abstractmethod
    def sn(self):
        warnings.warn('%s not supported sno() method' % self.__class__)

    @abstractmethod
    def load(self, on_off=None):
        warnings.warn('%s not supported load() method' % self.__class__)

    @abstractmethod
    def load_mode(self, mode, value):
        """
        设置负载模式
        """
        warnings.warn('%s not supported load_mode() method' % self.__class__)

    @abstractmethod
    def short(self, on_off=None):
        warnings.warn('%s not supported short() method' % self.__class__)

    def auto_range(self, on_off=None):
        """
        设置电压表自动量程
        """
        warnings.warn('%s can\'t support auto_range() method' % self.__class__)

    @abstractmethod
    def list_mode(self, eload_mode=None, curr_range=None, repeat=1, *steps):
        """
        list 模式
        """
        warnings.warn('%s can\'t support list_mode() method' % self.__class__)

    @abstractmethod
    def tran_mode(self, eload_mode, level_a, time_a, level_b, time_b, tran=None):
        """
        Tran模式
        """
        warnings.warn('%s can\'t support tran_mode() method' % self.__class__)

    def ocp_mode(self,
                 v_level: float,        # 设置 Von 电压值
                 v_delay: float,        # 设置 Von 电压延时时间
                 c_range: float,        # 设置工作电流量程
                 c_start: float,        # 设置初始电流值
                 c_step: float,         # 设置步进电流值
                 step_delay: float,     # 设置步进延时时间
                 c_end: float,          # 设置截止电流值
                 ocp_volt: float,       # 设置 OCP 电压值
                 max_trip: float,       # 过电流范围(最大值)设置
                 min_trip: float,       # 过电流范围(最小值)设置
                 nrf: int               # 保存 OCP 测试文件(1-10)
                 ):
        """
        OCP(Over Current Protection)测试
        """
        warnings.warn('%s can\'t support ocp_mode() method' % self.__class__)

    def opp_mode(self,
                 v_level: float,        # 设置 Von 电压值
                 v_delay: float,        # 设置 Von 电压延时时间
                 c_range: float,        # 设置工作电流量程
                 p_start: float,        # 设置初始功率值
                 p_step: float,         # 设置步进功率值
                 step_delay: float,     # 设置步进延时时间
                 p_end: float,          # 设置截止电流值
                 opp_volt: float,       # 设置 OPP 电压值
                 max_trip: float,       # 过功率范围(最大值)设置
                 min_trip: float,       # 过功率范围(最小值)设置
                 nrf: int               # 保存 OCP 测试文件(1-10)
                 ):
        """
        OPP(Over Power Protection)测试
        """
        warnings.warn('%s can\'t support opp_mode() method' % self.__class__)

    # 电池测试参数编辑需将 RUNMODE 选为 NORMAL 后编辑
    def batt_mode(self, c_range, batt_curr, cut_volt, cut_cap, batt_time, file):
        """
        电池模式
        """
        warnings.warn('%s can\'t support batt_mode() method' % self.__class__)

    def cr_led_mode(self):
        """
        CR_LED模式
        """
        warnings.warn('%s can\'t support cr_led_mode() method' % self.__class__)

    @abstractmethod
    def content(self):
        """
        获取电子负载所有内容值
        """
        warnings.warn('%s can\'t support cr_led_mode() method' % self.__class__)

    @abstractmethod
    def von_mode(self):
        """
        von模式
        """
        warnings.warn('%s can\'t support von_mode() method' % self.__class__)

    def curr_protection(self):
        """
        过流保护设置
        """
        warnings.warn('%s can\'t support curr_protection() method' % self.__class__)

    def power_protection(self):
        """
        软件过功率保护设置
        """
        warnings.warn('%s can\'t support power_protection() method' % self.__class__)

    def hardware_protection(self):
        """
        硬件过载保护设置
        """
        warnings.warn('%s can\'t support hardware_protection() method' % self.__class__)

    def auto_test_mode(self):
        """
        自动测试功能
        """
        warnings.warn('%s can\'t support auto_test() method' % self.__class__)

    def input_limit(self):
        """
        输入限制
        """
        warnings.warn('%s not supported input_limit() method' % self.__class__)

    def hardware_ranges(self):
        """
        获取硬件量程
        """
        warnings.warn('%s can\'t support hardware_ranges() method' % self.__class__)

    @abstractmethod
    def trigger_source(self, source):
        """
        设置触发源
        """
        warnings.warn('%s can\'t support trigger_source() method' % self.__class__)

    def curr_slew(self, **values):
        """
        设置电流上升或下降斜率
        """
        warnings.warn('%s can\'t support current_slew() method' % self.__class__)

    def get_ripple(self):
        """
        获取谐波电压和谐波电流
        """
        warnings.warn('%s can\'t support get_ripple() method' % self.__class__)

    # @abstractmethod
    # def prog_mode(self):
    #     """
    #     Prog模式, 相当于面板上的Shift+Prog键, IT8500+为兼容IT8500而作
    #     """
    #     warnings.warn('%s can\'t support prog_mode() method' % self.__class__)

    def calibrate_lock(self, on_off):
        """
        校准保护锁
        """
        warnings.warn('%s can\'t support calibrate_lock() method' % self.__class__)

    def calibrate_reset(self):
        """
        恢复校准状态到出厂值
        """
        warnings.warn('%s can\'t support calibrate_reset() method' % self.__class__)

    def calibrate_save(self):
        """
        校准信息保存
        """
        warnings.warn('%s can\'t support calibrate_save() method' % self.__class__)

    def calibrate(self):
        """
        设置和读取校准信息
        """
        warnings.warn('%s can\'t support calibrate() method' % self.__class__)

    def calibrate_volt(self, point, act_volt):
        """
        校准电压, 1-4点
        """
        warnings.warn('%s can\'t support calibrate_volt() method' % self.__class__)

    def calibrate_curr(self, point, act_curr):
        """
        校准电流, 1-4点
        """
        warnings.warn('%s can\'t support calibrate_curr() method' % self.__class__)
