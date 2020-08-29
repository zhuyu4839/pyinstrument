# -*- encoding: utf-8 -*-


class An8721pCmd:

    BAUDRATE_TUPLE = (1200, 9600, 19200, 38400)
    RW_DELAY_TUPLE = (0.3, 0.3, 0.2, 0.2)
    SUCCESS = 0x00
    FAIL = 0x01

    __CONTROL = 0x0F
    __QUERY = 0xF0
    __SETTING = 0x5A

    START = (__CONTROL, 0x00)  # 启动电能量
    STOP = (__CONTROL, 0x01)  # 停止电能量
    CLEAR = (__CONTROL, 0x02)  # 清零电能量

    VOLTAGE = (__QUERY, 0x00)  # 查询电压值
    CURRENT = (__QUERY, 0x01)  # 查询电流值
    ACTIVE_POWER = (__QUERY, 0x02)  # 查询有功功率值
    APPARENT_POWER = (__QUERY, 0x03)  # 查询视在功率值
    REACTIVE_POWER = (__QUERY, 0x04)  # 查询无功功率值
    POWER_FACTOR = (__QUERY, 0x05)  # 查询功率因数值
    ANGLE = (__QUERY, 0x06)  # 查询角度值
    FREQUENCY = (__QUERY, 0x07)  # 查询频率值
    ENERGY_TIME = (__QUERY, 0x08)  # 查询电能量时间
    ENERGY = (__QUERY, 0x09)  # 查询电能量
    ENERGY_TIME_THRESHOLD = (__QUERY, 0x0A)  # 查询电能量时间(达到门限后)

    # 电压4 字节，电流4 字节，功率8 字节，功率因数3 字节，频率3 字节，时间4 字节，电能量8 字节
    NORMALS = (__QUERY, 0xAF)  # 查询所有常规测量值

    QUERY_DICT = {
        'volt': VOLTAGE,
        'curr': CURRENT,
        'act_p': ACTIVE_POWER,
        'app_p': APPARENT_POWER,
        'react_p': REACTIVE_POWER,
        'p_fact': POWER_FACTOR,
        'ang': ANGLE,
        'freq': FREQUENCY,
        'ene_t': ENERGY_TIME,
        'ene': ENERGY,
        'et_thr': ENERGY_TIME_THRESHOLD
    }

    MAGNIFY_DICT = {
        'volt': 100,
        'curr': 10000,
        'act_p': 1000,
        'app_p': 1000,
        'react_p': 1000,
        'p_fact': 1000,
        'ang': 10,
        'freq': 100,
        'ene_t': 1,
        'ene': 100,
        'et_thr': 1
    }

    VOLTAGE_RANGE = (__SETTING, 0x00)  # 设置电压量程 (1 字节)
    CURRENT_RANGE = (__SETTING, 0x01)  # 设置电流量程 (1 字节)
    CALCULATION_MODE = (__SETTING, 0x02)  # 设置计算模式 (1 字节)
    CALCULATION_PERIOD = (__SETTING, 0x03)  # 设置计算周期 (1 字节)
    VOLTAGE_RATIO = (__SETTING, 0x04)  # 设置电压变比 (2 字节)
    CURRENT_RATIO = (__SETTING, 0x05)  # 设置电流变比 (2 字节)
    CURRENT_THRESHOLD = (__SETTING, 0x06)  # 设置电能量电流门限 (2 字节)
    TIME = (__SETTING, 0x07)  # 设置电能量计时时间 (4 字节)

    WARNING_BUZZER = (__SETTING, 0x08)  # 设置报警蜂鸣器开关 (1 字节)
    WARNING_GROUP = (__SETTING, 0x09)  # 设置报警参数组号 (1 字节)
    WARNING_VOLTAGE_UPPER = (__SETTING, 0x0A)  # 设置电压报警上限 (2 字节)
    WARNING_VOLTAGE_LOWER = (__SETTING, 0x0B)  # 设置电压报警下限 (2 字节)
    WARNING_VOLTAGE_THRESHOLD = (__SETTING, 0x0C)  # 设置报警门限电压 (2 字节)
    WARNING_CURRENT_UPPER = (__SETTING, 0x0D)  # 设置电流报警上限 (2 字节)
    WARNING_CURRENT_LOWER = (__SETTING, 0x0E)  # 设置电流报警下限 (2 字节)
    WARNING_CURRENT_THRESHOLD = (__SETTING, 0x0F)  # 设置报警门限电流 (2 字节)
    WARNING_POWER_UPPER = (__SETTING, 0x10)  # 设置功率报警上限 (2 字节)
    WARNING_POWER_LOWER = (__SETTING, 0x11)  # 设置功率报警下限 (2 字节)
    WARNING_POWER_THRESHOLD = (__SETTING, 0x12)  # 设置报警门限功率 (1 字节)
    WARNING_DELAY = (__SETTING, 0x13)  # 设置报警延时 (1 字节)

    ZERO_THRESHOLD = (__SETTING, 0x20)  # 设置零值门限开关 (1 字节)
    VOLTAGE_SHIELD = (__SETTING, 0x21)  # 设置电压屏蔽值 (3 字节)
    CURRENT_SHIELD = (__SETTING, 0x21)  # 设置电流屏蔽值 (2 字节)
    KEY_LOCK = (__SETTING, 0x23)  # 设置键盘锁功能 (1 字节)

    # 设置报警参数（报警参数组号，电压报警上下限及门限，电流报警上下限及门限，功率报警上下限及门限，报警延时）
    WARNING_PARAMETERS = (__SETTING, 0XA0)  # 20 字节
    # 设置所有常规参数（电压量程，电流量程，计算模式， 计算周期，电压变比，电流变比，电能量电流门限，电能量计时时间，报警蜂鸣器开关）
    PARAMETERS = (__SETTING, 0XAF)  # 15 字节




























