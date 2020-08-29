# -*- encoding: utf-8 -*-
from constants import ON, ONE, ZERO, OFF
from instrument.eloads.itech.const import *

FIXED = 'fix'
SHORT = 'short'
TRANSITION = 'tran'
LIST = 'list'
BATTERY = 'batt'


TUPLE_ELOAD_MODE = (CC, CV, CW, CR)
TUPLE_WORK_MODE = (FIXED, SHORT, TRANSITION, LIST, BATTERY)
TUPLE_TRIGGER_MODE = (MANUAL, EXTERNAL, BUS, HOLD)
TUPLE_STOP_COND = (COMPLETE, FAILURE)
TUPLE_TRAN_MODE = (CONTINUOUS, PULSE, TOGGLE)
TUPLE_VON_MODE = (LIVING, LATCH)


class It85xxCmd:

    BAUDRATE_TUPLE = (4800, 9600, 19200, 38400)
    RW_DELAY_TUPLE = (0.03, 0.03, 0.03, 0.03)

    # 85XX系列电子负载命令格式
    # 同步头 负载地址 命令字   4—25字节为相关信息内容  校验码(校验和)
    IT85XX_CMD = [0xAA, 0xFF,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  ]

    VALIDATE = 0x12                 # 校验命令

    LOCAL_REMOTE_SET = 0x20         # 设置负载的操作模式
    INPUT_STATUS_SET = 0x21         # 设置负载的输出状态(on/off)

    MAX_INPUT_VOLT_SET = 0x22       # 设置负载的最大输入电压值
    MAX_INPUT_VOLT_GET = 0x23       # 读取负载的最大输入电压设置值
    MAX_INPUT_CURR_SET = 0x24       # 设置负载的最大输入电流值
    MAX_INPUT_CURR_GET = 0x25       # 读取负载的最大输入电流设置值
    MAX_INPUT_POWER_SET = 0x26      # 设置负载的最大输入功率值
    MAX_INPUT_POWER_GET = 0x27      # 读取负载的最大输入功率设置值

    LOAD_MODE_SET = 0x28            # 设置负载的操作模式(CC, CV, CW, CR)
    LOAD_MODE_GET = 0x29            # 读取负载的操作模式(CC, CV, CW, CR)

    CC_VALUE_SET = 0x2a             # 设置负载的定电流值
    CC_VALUE_GET = 0x2b             # 读取负载的定电流值
    CV_VALUE_SET = 0x2c             # 设置负载的定电压值
    CV_VALUE_GET = 0x2d             # 读取负载的定电压值
    CW_VALUE_SET = 0x2e             # 设置负载的定功率值
    CW_VALUE_GET = 0x2f             # 读取负载的定功率值
    CR_VALUE_SET = 0x30             # 设置负载的定电阻值
    CR_VALUE_GET = 0x31             # 读取负载的定电阻值
    # 动态参数设置, 即TRAN(0x32/0x33为旧指令,支持最小值为0.1ms;0xf0/0xf1为新指令,支持最小值为0.01ms)
    DYN_CURR_SET = 0x32             # 设置负载的动态定电流参数
    DYN_CURR_GET = 0x33             # 读取负载的动态定电流参数
    DYN_VOLT_SET = 0x34             # 设置负载的动态定电压参数
    DYN_VOLT_GET = 0x35             # 读取负载的动态定电压参数
    DYN_POWER_SET = 0x36            # 设置负载的动态定功率参数
    DYN_POWER_GET = 0x37            # 读取负载的动态定功率参数
    DYN_RES_SET = 0x38              # 设置负载的动态定电阻参数
    DYN_RES_GET = 0x39              # 读取负载的动态定电阻参数
    # list模式相关设置
    LIST_MODE_SET = 0x3a            # 设置负载的 LIST 操作模式(CC, CV, CW, CR)
    LIST_MODE_GET = 0x3b            # 读取负载的 LIST 操作模式 (CC, CV, CW, CR)
    LIST_REPEAT_SET = 0x3c          # 设置负载的 LIST 循环模式(ONCE, REPEAT)
    LIST_REPEAT_GET = 0x3d          # 读取负载的 LIST 循环模式(ONCE, REPEAT)
    LIST_STEP_SET = 0x3e            # 设置负载的 LIST 步数
    LIST_STEP_GET = 0x3f            # 读取负载的 LIST 步数
    LIST_CURR_TIME_SET = 0x40       # 设置负载的相应单步的电流值及时间值
    LIST_CURR_TIME_GET = 0x41       # 读取负载的相应单步的电流值及时间值
    LIST_VOLT_TIME_SET = 0x42       # 设置负载的相应单步的电压值及时间值
    LIST_VOLT_TIME_GET = 0x43       # 读取负载的相应单步的电压值及时间值
    LIST_POWER_TIME_SET = 0x44      # 设置负载的相应单步的功率值及时间值
    LIST_POWER_TIME_GET = 0x45      # 读取负载的相应单步的功率值及时间值
    LIST_RES_TIME_SET = 0x46        # 设置负载的相应单步的电阻值及时间值
    LIST_RES_TIME_GET = 0x47        # 读取负载的相应单步的电阻值及时间值
    LIST_FILE_NAME_SET = 0x48       # 设置负载的 LIST 文件名
    LIST_FILE_NAME_GET = 0x49       # 读取负载的 LIST 文件名
    LIST_STORE_MODE_SET = 0x4a      # 设置负载的 LIST 储存区的划分模式
    LIST_STORE_MODE_GET = 0x4b      # 读取负载的 LIST 储存区的划分模式
    LIST_FILE_SAVE = 0x4c           # 保存负载的 LIST 文件到指定的存储区
    LIST_FILE_CALL = 0x4d           # 从指定的负载的 LIST 文件存储区取出 LIST 文件
    # ********************************************************* #
    # battery模式截止电压
    BATT_CUTOFF_VOLT_SET = 0x4e     # 设置负载工作在电池测试模式下的最小电压值
    BATT_CUTOFF_VOLT_GET = 0x4f     # 读取负载工作在电池测试模式下的最小电压值
    FLO_TIMER_SET = 0x50            # 设置负载的 FOR LOAD ON 定时器时间值
    FLO_TIMER_GET = 0x51            # 读取负载的 FOR LOAD ON 定时器时间值
    FLO_STATUS_SET = 0x52           # 设置负载的 FOR LOAD ON 定时器状态
    FLO_STATUS_GET = 0x53           # 读取负载的 FOR LOAD ON 定时器状态
    # ********************************************************* #
    ADDR_SET = 0x54                 # 设置负载的新通讯地址
    # 设置是否允许 LOCAL 键使用，若 LOCAL 键允许使用，则负载在 REMOTE 操作模式时，用户可以按面板上的SHIFT+LOCAL 键使负载返回到 LOCAL 操作模式
    LOCAL_EN_SET = 0x55             #
    RM_STATUS_SET = 0x56            # 设置负载的远程测量模式的状态
    RM_STATUS_GET = 0x57            # 设置负载的远程测量模式的状态
    # 设置负载的触发模式:(0 为MAUNal, 1 为EXTernal, 2 为BUS, 3为HOLD)
    TRIG_MODE_SET = 0x58            # 设置负载的触发模式
    TRIG_MODE_GET = 0x59            # 读取负载的触发模式
    TRIG_BUS = 0x5a                 # 发送给负载一个触发信号(BUS触发信号)
    SETTINGS_SAVE = 0x5b            # 保存负载的相关设置到指定的存储区
    SETTINGS_CALL = 0x5b            # 从指定的负载存储区取出已保存的相关设置
    # 设置负载的工作模式 fix, short, tran, list, batt
    WORK_MODE_SET = 0x5d            # 设置负载的工作模式 (FIXED, SHORT, TRAN, LIST,BATTERY)
    WORK_MODE_GET = 0x5e            # 读取负载的工作模式 (FIXED, SHORT, TRAN, LIST,BATTERY)
    # 读取负载的输入电压,输入电流,输入功率及操作状态寄存器,查询状态寄存器,散热器温度,工作模式,当前LIST的步数,当前LIST的循环次数
    CONTENT_1_GET = 0x5f            # 读取负载的输入电压, 输入电流, 输入功率及相关状态

    CAL_PSTATUS_SET = 0x60          # 设置负载的校准保护状态
    CAL_PSTATUS_GET = 0x61          # 读取负载的校准保护状态
    CAL_VOLT = 0x62                 # 校准负载的电压点
    CAL_VOLT_ACT = 0x63             # 返回给负载当前的实际输入电压
    CAL_CURR = 0x64                 # 校准负载的电流点
    CAL_CURR_ACT = 0x65             # 返回给负载当前的实际输入电流
    CAL_SAVE = 0x66                 # 保存负载校准数据到 EEPROM 中,供用户校准时使用
    CAL_INFO_SET = 0x67             # 设置负载的校准信息
    CAL_INFO_GET = 0x68             # 读取负载的校准信息
    CAL_FACTORY_EXEC = 0x69         # 恢复校准资料为出厂时的值
    MODEL_VERSION_GET = 0x6a        # 读取负载的产品型号,产品序列号及软件版本号
    SN_GET = 0x6b                   # 读取负载的条形码信息

    _WORK_MODE_FIXED = [WORK_MODE_SET, 0]
    _WORK_MODE_SHORT = [WORK_MODE_SET, 1]
    _WORK_MODE_TRANSITION = [WORK_MODE_SET, 2]
    _WORK_MODE_LIST = [WORK_MODE_SET, 3]
    _WORK_MODE_BATTERY = [WORK_MODE_SET, 4]

    DICT_WORK_MODE_SET = {
        FIXED: _WORK_MODE_FIXED, 0: _WORK_MODE_FIXED,
        SHORT: _WORK_MODE_SHORT, 1: _WORK_MODE_SHORT,
        TRANSITION: _WORK_MODE_TRANSITION, 2: _WORK_MODE_TRANSITION,
        LIST: _WORK_MODE_LIST, 3: _WORK_MODE_LIST,
        BATTERY: _WORK_MODE_BATTERY, 4: _WORK_MODE_BATTERY,
    }

    DICT_LOAD_ON_OFF_SET = {
        ON: [INPUT_STATUS_SET, 1], ONE: [INPUT_STATUS_SET, 1], 1: [INPUT_STATUS_SET, 1],
        OFF: [INPUT_STATUS_SET, 0], ZERO: [INPUT_STATUS_SET, 0], 0: [INPUT_STATUS_SET, 0],
    }

    DICT_LIST_STEP = {CC: LIST_CURR_TIME_SET, CV: LIST_VOLT_TIME_SET,
                      CW: LIST_POWER_TIME_SET, CR: LIST_RES_TIME_SET}

    DICT_ELOAD_MODE = {
        CC: [LOAD_MODE_SET, 0], 0: [LOAD_MODE_SET, 0],
        CV: [LOAD_MODE_SET, 1], 1: [LOAD_MODE_SET, 1],
        CW: [LOAD_MODE_SET, 2], 2: [LOAD_MODE_SET, 2],
        CR: [LOAD_MODE_SET, 3], 3: [LOAD_MODE_SET, 3],
    }

    DICT_TRIG_MODE = {
        MANUAL: [TRIG_MODE_SET, 0], 0: [TRIG_MODE_SET, 0],
        EXTERNAL: [TRIG_MODE_SET, 1], 1: [TRIG_MODE_SET, 1],
        BUS: [TRIG_MODE_SET, 2], 2: [TRIG_MODE_SET, 2],
        HOLD: [TRIG_MODE_SET, 3], 3: [TRIG_MODE_SET, 3],
    }


class It8500Cmd:
    LOAD_VOLT_SET = 0x10            # 设置负载的带载电压值
    LOAD_VOLT_GET = 0x11            # 读取负载的带载电压值
    UNLOAD_VOLT_SET = 0x12          # 设置负载的卸载电压值
    UNLOAD_VOLT_GET = 0x13          # 读取负载的卸载电压值


class It8500PlusCmd:
    HARDWARE_RANGE_GET = 0x01       # 取负载讯息(硬件量程参数)
    HP_POWER_SET = 0x02             # 设置硬件过功率保护值
    HP_POWER_GET = 0x03             # 读取硬件过功率保护值
    VON_MODE_SET = 0x0e             # 设置 VON 模式
    VON_MODE_GET = 0x0f             # 读取 VON 模式
    VON_VOLT_SET = 0x10             # 设置 VON 电压值
    VON_VOLT_GET = 0x11             # 读取 VON 电压值
    P_CURR_SET = 0x80               # 设置过电流保护值
    P_CURR_GET = 0x81               # 读取过电流保护值
    PC_DELAY_SET = 0x82             # 设置过电流保护延时时间
    PC_DELAY_GET = 0x83             # 读取过电流保护延时时间
    PC_ENABLE_SET = 0x84            # 设置过电流保护使能/失能状态
    PC_ENABLE_GET = 0x85            # 读取过电流保护使能/失能状态
    SP_POWER_SET = 0x86             # 设置软件过功率保护值
    SP_POWER_GET = 0x87             # 读取软件过功率保护值
    SP_POWER_DELAY_SET = 0x88       # 设置软件过功率保护延时时间
    SP_POWER_DELAY_GET = 0x89       # 读取软件过功率保护延时时间
    # ********************************************************************* #
    MCT1_VOLT_SET = 0x8a            # 设置测控时间的第 1 点比较电压
    MCT1_VOLT_GET = 0x8b            # 读取测控时间的第 1 点比较电压
    MCT2_VOLT_SET = 0x8c            # 设置测控时间的第 2 点比较电压
    MCT2_VOLT_GET = 0x8d            # 读取测控时间的第 2 点比较电压
    # ********************************************************************* #
    CR_LED_CUTOFF_VOLT_SET = 0x8e   # 设置 CR_LED 模式的截止电压值
    CR_LED_CUTOFF_VOLT_GET = 0x8f   # 读取 CR_LED 模式的截止电压值
    PROT_STATUS_CLEAR = 0x90        # 清除保护状态
    VOLT_AUTO_RANGE_SET = 0x91      # 设置电压测量自动量程状态
    VOLT_AUTO_RANGE_GET = 0x92      # 读取电压测量自动量程状态
    CR_LED_FUNC_SET = 0x93          # 设置 CR 模式时 CR_LED 功能
    CR_LED_FUNC_GET = 0x94          # 读取 CR 模式时 CR_LED 功能
    SIM_KEY_EXEC = 0x98             # 模拟键盘按下
    LAST_KEY_CODE_GET = 0x99        # 读取最后一次键盘值
    VFD_MODE_SET = 0x9a             # 设置 VFD 显示模式
    VFD_MODE_GET = 0x9b             # 读取 VFD 显示模式
    VFD_CONTENT_GET = 0x9c          # 设置 VFD 显示内容
    TRIGGER = 0x9d                  # 发送一次触发, 不管触发源为什么, 都产生触发信号
    # ********************************************************************* #
    CONTENT_2_GET = 0xa0            # 读取负载内容 2, 带载容量[3:7], 带载时间或上升/下降时间[7:11], 定时器剩余时间[11:15]
    CONTENT_3_GET = 0xa1            # 读取负载内容 3, 最大输入电压值, 最小输入电压值, 最大输入电流值, 最小输入电流值
    MAX_VOLT_GET = 0xa2             # 读取负载最大电压值
    MIN_VOLT_GET = 0xa3             # 读取负载最小电压值
    MAX_CURR_GET = 0xa4             # 读取负载最大电流值
    MIN_CURR_GET = 0xa5             # 读取负载最小电流值
    # ********************************************************************* #
    LOAD_CAP_GET = 0xa6             # 读取负载的带载容量值
    ALL_RIPPLE_GET = 0xa8           # 获取所有纹波参数
    VOLT_RIPPLE_GET = 0xab          # 获取纹波电压参数
    CURR_RIPPLE_GET = 0xac          # 获取纹波电流参数
    RISE_SLEW_SET = 0xb0            # 设置电流上升斜率
    RISE_SLEW_GET = 0xb1            # 读取电流上升斜率
    FALL_SLEW_SET = 0xb2            # 设置电流下降斜率
    FALL_SLEW_GET = 0xb3            # 读取电流下降斜率
    CC_VOLT_UPPER_SET = 0xb4        # 设置定电流时电压上限
    CC_VOLT_UPPER_GET = 0xb5        # 读取定电流时电压上限
    CC_VOLT_LOWER_SET = 0xb6        # 设置定电流时电压下限
    CC_VOLT_LOWER_GET = 0xb7        # 读取定电流时电压下限
    CV_CURR_UPPER_SET = 0xb8        # 设置定电压时电流上限
    CV_CURR_UPPER_GET = 0xb9        # 读取定电压时电流上限
    CV_CURR_LOWER_SET = 0xba        # 设置定电压时电流下限
    CV_CURR_LOWER_GET = 0xbb        # 读取定电压时电流下限
    CW_VOLT_UPPER_SET = 0xbc        # 设置定功率时电压上限
    CW_VOLT_UPPER_GET = 0xbd        # 读取定功率时电压上限
    CW_VOLT_LOWER_SET = 0xbe        # 设置定功率时电压下限
    CW_VOLT_LOWER_GET = 0xbf        # 读取定功率时电压下限
    MAX_INPUT_RES_SET = 0xc0        # 设置负载的最大输入电阻设置值
    MAX_INPUT_RES_GET = 0xc1        # 读取负载的最大输入电阻设置值
    CR_VOLT_UPPER_SET = 0xc2        # 设置定电阻时电压上限
    CR_VOLT_UPPER_GET = 0xc3        # 读取定电阻时电压上限
    CR_VOLT_LOWER_SET = 0xc4        # 设置定电阻时电压下限
    CR_VOLT_LOWER_GET = 0xc5        # 读取定电阻时电压下限
    LIST_CURR_RANGE_SET = 0xc6      # 设置 LIST 模式电流量程
    LIST_VOLT_RANGE_SET = 0xc7      # 设置 LIST 模式电压量程
    AUTO_TEST_STEP_SET = 0xd0       # 设置自动测试使用的单步
    AUTO_TEST_STEP_GET = 0xd1       # 读取自动测试使用的单步
    AUTO_TEST_SHORT_STEP_SET = 0xd2     # 设置自动测试短路的单步
    AUTO_TEST_SHORT_STEP_GET = 0xd3     # 读取自动测试短路的单步
    AUTO_TEST_PAUSE_STEP_SET = 0xd4     # 设置自动测试暂停的单步
    AUTO_TEST_PAUSE_STEP_GET = 0xd5     # 读取自动测试暂停的单步
    AUTO_TEST_LOAD_TIME_SET = 0xd6      # 设置自动测试单步的带载时间
    AUTO_TEST_LOAD_TIME_GET = 0xd7      # 读取自动测试单步的带载时间
    AUTO_TEST_TEST_TIME_SET = 0xd8      # 设置自动测试单步的测试时间
    AUTO_TEST_TEST_TIME_GET = 0xd9      # 读取自动测试单步的测试时间
    AUTO_TEST_UNLOAD_TIME_SET = 0xda    # 设置自动测试单步的卸载时间
    AUTO_TEST_UNLOAD_TIME_GET = 0xdb    # 读取自动测试单步的卸载时间
    AUTO_TEST_STOP_SET = 0xdc       # 设置自动测试停止条件
    AUTO_TEST_STOP_GET = 0xdd       # 读取自动测试停止条件
    AUTO_TEST_LINK_SET = 0xde       # 设置自动测试链接文件
    AUTO_TEST_LINK_GET = 0xdf       # 读取自动测试链接文件
    AUTO_TEST_SAVE = 0xe0           # 保存自动测试文件
    AUTO_TEST_CALL = 0xe1           # 调用自动测试文件
    # 动态参数设置, 即TRAN(0x32/0x33为旧指令,支持最小值为0.1ms;0xf0/0xf1为新指令,支持最小值为0.01ms)
    DYN_CURR_SET = 0xf0            # 设置负载的动态定电流参数
    DYN_CURR_GET = 0xf1            # 读取负载的动态定电流参数

    # 按键key code
    KEY_CODE_SHIFT = 0x40           # shift键值
    KEY_CODE_LOCAL = 0x18           # local键值
    KEY_CODE_ESC = 0x14             # esc键值
    KEY_CODE_0 = 0x09               # 0键值
    KEY_CODE_1 = 0x0a               # 1键值
    KEY_CODE_2 = 0x0b               # 2键值
    KEY_CODE_3 = 0x0c               # 3键值
    KEY_CODE_4 = 0x0d               # 4键值
    KEY_CODE_5 = 0x0e               # 5键值
    KEY_CODE_6 = 0x0f               # 6键值
    KEY_CODE_7 = 0x10               # 7键值
    KEY_CODE_8 = 0x11               # 8键值
    KEY_CODE_9 = 0x12               # 9键值
    KEY_CODE_DOT = 0x13             # .键值
    KEY_CODE_CC = 0x01              # CC键值
    KEY_CODE_CV = 0x02              # CV键值
    KEY_CODE_CW = 0x04              # CW键值
    KEY_CODE_CR = 0x03              # CR键值
    KEY_CODE_ENTER = 0x16           # enter键值
    KEY_CODE_ON_OFF = 0x17          # on/off键值
    KEY_CODE_UP = 0x07              # up键值
    KEY_CODE_DOWN = 0x08            # down键值
    KEY_CODE_LEFT = 0x05            # left键值
    KEY_CODE_RIGHT = 0x06           # right键值

    DICT_VOLT_AUTO_RANGE_SET = {
        OFF: [VOLT_AUTO_RANGE_SET, 0], ZERO: [VOLT_AUTO_RANGE_SET, 0], 0: [VOLT_AUTO_RANGE_SET, 0],
        ON: [VOLT_AUTO_RANGE_SET, 1], ONE: [VOLT_AUTO_RANGE_SET, 1], 1: [VOLT_AUTO_RANGE_SET, 1],
    }

    DICT_CM_UPPER_SET = {
        CC: [CC_VOLT_UPPER_SET, ], CV: [CV_CURR_UPPER_SET, ],
        CW: [CW_VOLT_UPPER_SET, ], CR: [CR_VOLT_UPPER_SET, ],
    }
    DICT_CM_UPPER_GET = {
        CC: [CC_VOLT_UPPER_GET, ], CV: [CV_CURR_UPPER_GET, ],
        CW: [CW_VOLT_UPPER_GET, ], CR: [CR_VOLT_UPPER_GET, ],
    }

    DICT_CM_LOWER_SET = {
        CC: [CC_VOLT_LOWER_SET, ], CV: [CV_CURR_LOWER_SET, ],
        CW: [CW_VOLT_LOWER_SET, ], CR: [CR_VOLT_LOWER_SET, ],
    }
    DICT_CM_LOWER_GET = {
        CC: [CC_VOLT_LOWER_GET, ], CV: [CV_CURR_LOWER_GET, ],
        CW: [CW_VOLT_LOWER_GET, ], CR: [CR_VOLT_LOWER_GET, ],
    }

    DICT_VON_MODE_SET = {
        LIVING: [VON_MODE_SET, 0], LATCH: [VON_MODE_SET, 1]
    }
