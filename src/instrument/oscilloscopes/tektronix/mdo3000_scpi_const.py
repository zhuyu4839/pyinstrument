# -*- encoding: utf-8 -*-
from constants import OFF, ZERO, ON, ONE, RUN, STOP
from instrument import utils
from instrument.const import INTERROGATION, EMPTY, BRACE, SPACE, COMMAS

from re import IGNORECASE as IGNORE_CASE

YELLOW = 'yellow'
BLUE = 'blue'
PURPLE = 'purple'
GREEN = 'green'

SAMPLE = 'sam'
# 采样
PEAK = 'peak'
# 峰值
HIRES = 'hir'
# 高分辨率
AVERAGE = 'ave'
# 平均
ENVELOPE = 'env'
# 包络

RUN_STOP = 'runs'

SEQUENCE = 'seq'

EXECUTE = 'exec'
INITIALIZE = 'init'
UNDO = 'undo'
BYPASS = 'byp'
PASS = 'pass'

PROBE_AUTO_ZERO = 'auto_zero'           # 清零
PROBE_CALIBRATE = 'cal'                 # 校准EXECute INITialize
PROBE_CALIBRATE_STATE = 'cal_state'     # 获取校准状态
PROBE_DEGAUSS = 'deg'                   # 消磁
PROBE_DEGAUSS_STATE = 'deg_state'       # 获取消磁状态
PROBE_FORCE_RANGE = 'range'             # 设置或查询量程
PROBE_GAIN = 'gain'                     # 设置或查询衰减比
PROBE_ID = 'id'                         # 获取ID
# PROBE_SN = 'sn'                         # 获取SerialNumber
PROBE_TYPE = 'type'                     # 获取探头类型
PROBE_MODEL = 'model'                   # 获取探头型号
PROBE_PROP_DELAY = 'prop_delay'         # 设置或查询传播延时(propagation delay)
PROBE_DESKEW = 'deskew'                 # 设置或查询偏差校正值
PROBE_RESISTANCE = 'res'                # 获取探头电阻值
PROBE_SIGNAL = 'signal'                 # 设置探头型号类型(BYPass and PASS)
PROBE_UNITS = 'units'                   # 获取探头单位

BANDWIDTH = 'bandwidth'
ANALOG_SAMPLE_RATE = 'samp_rate'
ANALOG_CHANNEL_NUMBER = 'num_ch'
RECORD_LENGTH = 'rec_len'

TUPLE_Y_UNITS = (
    '%', '/Hz', 'A', 'A/A', 'A/V', 'A/W', 'A/dB', 'A/s', 'AA', 'AW', 'AdB', 'As', 'B', 'Hz', 'IRE', 'S/s', 'V',
    'V/A', 'V/V', 'V/W', 'V/dB', 'V/s', 'VV', 'VW', 'VdB', 'volts', 'Vs', 'W', 'W/A', 'W/V', 'W/W', 'W/dB',
    'W/s', 'WA', 'WV', 'WW', 'WdB', 'Ws', 'dB', 'dB/A', 'dB/V', 'dB/W', 'dB/dB', 'dBA', 'dBV', 'dBW',
    'dBdB', 'day', 'degrees', 'div', 'hr', 'min', 'ohms', 'percent', 's')

COMPLEMENT = [i if i < 0x80 else -(0xff - i + 1) for i in range(0xff + 1)]
# 用于把补码转换为原码数字

CHANNEL_COLOR_DICT = {YELLOW: 1, BLUE: 2, PURPLE: 3, GREEN: 4}


class Mdo3000Cmd:

    ACQUIRE = 'ACQ'
    FAST_ACQUIRE = ':FASTA'
    PALETTE = ':PALE'
    STATE = ':STATE'
    NUM_ACQUIRE = ':NUMAC'
    MODE = ':MOD'
    NUM_AVERAGE = ':NUMAV'
    NUM_ENVELOPE = ':NUME'
    STOP_AFTER = ':STOPA'

    ALIAS = 'ALI'
    CATALOG = ':CAT'
    DEFINE = ':DEF'
    DELETE = ':DELE'
    ALL = ':ALL'
    NAME = ':NAM'

    AUTO_SET = 'AUTOS'
    ENABLE = ':ENA'
    FACTOR = ':FAC'

    CHANNEL = 'CH{}'
    AMPS_VIA_VOLTS = ':AMPSVIAVOLT'
    BAND_WIDTH = ':BAN'
    COUPLING = ':COUP'
    DESKEW = ':DESK'
    CONFIG = 'CONFIG'

    MAX_SAMPLE_RATE = ':MAXS'
    _RES = ':RES'
    _MOD = ':MOD'
    _FASTA = ':FASTA'
    _PALE = ':PALE'
    _STATE = ':STATE'
    _NUMAC = ':NUMAC'
    _NUMAV = ':NUMAV'
    _NUME = ':NUME'
    _STOPA = ':STOPA'
    _CAT = ':CAT'
    _DEF = ':DEF'
    _ALL = ':ALL'
    _DELE = ':DELE'
    _NAM = ':NAM'
    _ENA = ':ENA'
    _AMPSVIAVOLT = ':AMPSVIAVOLT'
    _FAC = ':FAC'
    _BAN = ':BAN'
    _COUP = ':COUP'
    _DESK = ':DESK'
    _INV = ':INV'
    _LAB = ':LAB'
    _OFFS = ':OFFS'
    _POS = ':POS'
    _SCA = ':SCA'
    _TER = ':TER'
    _YUN = ':YUN'
    _PRO = ':PRO'
    _AUTOZ = ':AUTOZ'
    _CAL = ':CAL'
    _CALIBRATABL = ':CALIBRATABL'
    _COMMAND = ':COMMAND'
    _DEGAU = ':DEGAU'
    _FORCEDR = ':FORCEDR'
    _GAIN = ':GAIN'
    _ID = ':ID'
    _SER = ':SER'
    _TYP = ':TYP'
    _PROPDEL = ':PROPDEL'
    _RECDES = ':RECDES'
    _SIG = ':SIG'
    _UNI = ':UNI'
    _ADVMATH = ':ADVMATH'
    _AFG = ':AFG'
    _ANALO = ':ANALO'
    _BANDW = ':BANDW'
    _GNDCPLG = ':GNDCPLG'
    _MAXSAMPLER = ':MAXSAMPLER'
    _NUMCHAN = ':NUMCHAN'
    _RECLENS = ':RECLENS'
    _VERTINV = ':VERTINV'
    _APPL = ':APPL'
    _CUSTOMM = ':CUSTOMM'
    _LIMITM = ':LIMITM'
    _STANDARDM = ':STANDARDM'
    _VIDPIC = ':VIDPIC'
    _ARB = ':ARB'
    _AUXIN = ':AUXIN'
    _DIGITA = ':DIGITA'
    _MAG = ':MAG'
    _DVM = ':DVM'
    _EXTVIDEO = ':EXTVIDEO'
    _HISTOGRAM = ':HISTOGRAM'
    _NETWORKDRIVES = ':NETWORKDRIVES'
    _NUMMEAS = ':NUMMEAS'
    _REFS = ':REFS'
    _NUMREFS = ':NUMREFS'
    _RF = ':RF'
    _ADVTRIG = ':ADVTRIG'
    _ROSC = ':ROSC'
    _DDT = ':DDT'
    _HBA = ':HBA'
    _DELT = ':DELT'
    _POSITION = ':POSITION'
    _USE = ':USE'
    _SOU = ':SOU'
    _VBA = ':VBA'
    _ALTERNATE = ':ALTERNATE'
    _HPOS = ':HPOS'
    _VDELT = ':VDELT'
    _XY = ':XY'
    _POL = ':POL'
    _RADIUS = ':RADIUS'
    _THETA = ':THETA'
    _PRODUCT = ':PRODUCT'
    _RATIO = ':RATIO'
    _READOUT = ':READOUT'
    _RECT = ':RECT'
    _X = ':X'
    _Y = ':Y'
    _DEL = ':DEL'
    _TIM = ':TIM'
    _RECO = ':RECO'
    _SAMPLER = ':SAMPLER'
    _MAXS = ':MAXS'
    _POW = ':POW'
    CURS = 'CURS'
    _FUNC = ':FUNC'
    DATE = 'DATE'
    TIME = 'TIME'
    HOR = 'HOR'

    __EXEC = 'EXEC'

    ACQ_MAX_SAMPLE = '{}{}{}'.format(ACQUIRE, MAX_SAMPLE_RATE, INTERROGATION)

    _ACQUIRE = '{}{}{}{}{}'.format(ACQUIRE, BRACE, BRACE, BRACE, BRACE)
    ACQ_FAST_PALETTE_SET = _ACQUIRE.format(FAST_ACQUIRE, PALETTE, SPACE, BRACE)
    # 设置快速采集时波形调色板模式 {NORMal|TEMPErature|SPECTral|INVERTed}
    ACQ_FAST_PALETTE_GET = _ACQUIRE.format(FAST_ACQUIRE, PALETTE, INTERROGATION, EMPTY)

    ACQ_FAST_STATE_SET = _ACQUIRE.format(FAST_ACQUIRE, STATE, SPACE, BRACE)
    # 设置快速采集时状态 {0|1|OFF|ON}
    ACQ_FAST_STATE_GET = _ACQUIRE.format(FAST_ACQUIRE, STATE, INTERROGATION, EMPTY)

    ACQ_NUM_GET = _ACQUIRE.format(NUM_ACQUIRE, INTERROGATION, EMPTY, EMPTY)
    # 获取数据采集点的个数

    ACQ_MODE_SET = _ACQUIRE.format(MODE, SPACE, BRACE, EMPTY)
    # 采集模式 {SAMple|PEAKdetect|HIRes|AVErage|ENVelope}
    ACQ_MODE_GET = _ACQUIRE.format(MODE, INTERROGATION, EMPTY, EMPTY)

    ACQ_AVG_NUM_SET = _ACQUIRE.format(NUM_AVERAGE, SPACE, BRACE, EMPTY)
    # 采集模式为平均时的采集波形的个数 2-512间的2的指数值
    ACQ_AVG_NUM_GET = _ACQUIRE.format(NUM_AVERAGE, INTERROGATION, EMPTY, EMPTY)

    ACQ_ENV_NUM_SET = _ACQUIRE.format(NUM_ENVELOPE, SPACE, BRACE, EMPTY)
    # 采集模式为包络时的采集包络的个数 1-2000, 增量为1, 大于2000为无穷大(INFInite)
    ACQ_ENV_NUM_GET = _ACQUIRE.format(NUM_ENVELOPE, INTERROGATION, EMPTY, EMPTY)

    ACQ_STATE_SET = _ACQUIRE.format(STATE, SPACE, BRACE, EMPTY)
    # 设置采集状态{OFF|ON|RUN|STOP|<NR1>}
    # 当设置为ON or RUN, 一次新的采集将开始
    ACQ_STATE_GET = _ACQUIRE.format(STATE, INTERROGATION, EMPTY, EMPTY)

    ACQ_STOP_AFTER_SET = _ACQUIRE.format(STOP_AFTER, SPACE, BRACE, EMPTY)
    # 设置采集停止后动作 {RUNSTop|SEQuence}
    ACQ_STOP_AFTER_GET = _ACQUIRE.format(STOP_AFTER, INTERROGATION, EMPTY, EMPTY)

    TUPLE_ACQ_STATE = (ON, RUN, ONE, 1, OFF, STOP, '0', 0)

    TUPLE_ACQ_MODE = ('SAMple', 'SAM', 'sam', 'sample', 'PEAKdetect', 'PEAK', 'peak', 'peakdetect',
                      'HIRes', 'HIR', 'hir', 'hires', 'AVErage', 'AVE', 'ave', 'average', 'ENVelope', 'ENV', 'env',
                      'envelope')
    TUPLE_ACQ_STOP_AFTER = ('RUNSTop', 'RUNST', 'runst', 'runstop', 'SEQuence', 'SEQ', 'seq', 'sequence')
    TUPLE_ACQ_FAST_PALETTE = ('NORMal', 'NORM', 'norm', 'normal',
                              'TEMPErature', 'TEMPE', 'tempe', 'temperature',
                              'SPECTral', 'SPECT', 'spect', 'spectral',
                              'INVERTed', 'INVERT', 'invert', 'inverted')

    TUPLE_AUTO_SET = ('EXECute', 'EXEC', 'exec', 'execute', 'UNDo', 'UND', 'und', 'undo')
    TUPLE_COUPING = ('DC', 'dc', 'AC', 'ac', 'DCREJect', 'DCREJ', 'dcrej')

    _ALIAS = '{}{}{}{}{}'.format(ALIAS, BRACE, BRACE, BRACE, BRACE)
    ALIAS_CATALOG_GET = _ALIAS.format(CATALOG, INTERROGATION, EMPTY, EMPTY)

    ALIAS_DEFINE_SET = _ALIAS.format(DEFINE, SPACE, BRACE + COMMAS, BRACE)
    ALIAS_DEFINE_GET = _ALIAS.format(DEFINE, INTERROGATION, SPACE, BRACE)

    ALIAS_DELETE = _ALIAS.format(DELETE, NAME, SPACE, BRACE)
    ALIAS_DELETE_ALL = _ALIAS.format(DELETE, ALL, EMPTY, EMPTY)

    ALIAS_STATE_SET = _ALIAS.format(STATE, SPACE, BRACE, EMPTY)
    ALIAS_STATE_GET = _ALIAS.format(STATE, INTERROGATION, EMPTY, EMPTY)

    # ALIAS_OP_DICT = {'def':ALIAS_DEFINE_SET, 'del':ALIAS_DELETE, 'del_all':ALIAS_DELETE_ALL}

    _AUTO_SET = '{}{}{}{}'.format(AUTO_SET, BRACE, BRACE, BRACE)
    AUTO_SET_SET = _AUTO_SET.format(SPACE, BRACE, EMPTY)
    AUTO_SET_GET = _AUTO_SET.format(INTERROGATION, EMPTY, EMPTY)

    AUTO_SET_ENABLE_SET = _AUTO_SET.format(ENABLE, SPACE, BRACE)
    AUTO_SET_ENABLE_GET = _AUTO_SET.format(ENABLE, INTERROGATION, EMPTY)

    CH_INFO_GET = '{}{}'.format(CHANNEL, INTERROGATION)
    CH_AMP_VOLT_EN_SET = '{}{}{}{}{}'.format(CHANNEL, AMPS_VIA_VOLTS, ENABLE, SPACE, BRACE)
    CH_AMP_VOLT_FACT_SET = '{}{}{}{}{}'.format(CHANNEL, AMPS_VIA_VOLTS, FACTOR, SPACE, BRACE)
    _CH_PARAMS_SET = '{}{}{}{}'.format(CHANNEL, BRACE, SPACE, BRACE)
    CH_BANDWIDTH_SET = _CH_PARAMS_SET.format(BRACE, BAND_WIDTH, BRACE)
    CH_COUPLING_SET = _CH_PARAMS_SET.format(BRACE, COUPLING, BRACE)
    CH_DESKEW_SET = _CH_PARAMS_SET.format(BRACE, DESKEW, BRACE)
    CH_INVERT_SET = _CH_PARAMS_SET.format(BRACE, _INV, BRACE)
    CH_LABEL_SET = _CH_PARAMS_SET.format(BRACE, _LAB, BRACE)
    CH_OFFSET_SET = _CH_PARAMS_SET.format(BRACE, _OFFS, BRACE)
    CH_POSITION_SET = _CH_PARAMS_SET.format(BRACE, _POS, BRACE)
    CH_SCALE_SET = _CH_PARAMS_SET.format(BRACE, _SCA, BRACE)
    CH_TERMINATION_SET = _CH_PARAMS_SET.format(BRACE, _TER, BRACE)
    CH_YUNITS_SET = _CH_PARAMS_SET.format(BRACE, _YUN, BRACE)

    #     PROB_INFO_GET = '{}{}{}'.format(CHANNEL, )
    _PROBE = '{}{}{}{}{}'.format(CHANNEL, _PRO, BRACE, BRACE, BRACE)
    PROBE_AUTO_ZERO_EXEC = _PROBE.format(BRACE, _AUTOZ, SPACE, __EXEC)
    PROBE_CALIBRATE_SET = _PROBE.format(BRACE, _CAL, SPACE, BRACE)
    PROBE_CALIBRATABLE_GET = _PROBE.format(BRACE, _CAL, _CALIBRATABL, INTERROGATION)
    PROBE_CALIBRATE_STATE_GET = _PROBE.format(BRACE, _CAL, _STATE, INTERROGATION)

    PROBE_DEGAUSS_EXEC = _PROBE.format(BRACE, _DEGAU, SPACE, __EXEC)
    PROBE_DEGAUSS_STATE_GET = _PROBE.format(BRACE, _DEGAU, _STATE, INTERROGATION)

    PROBE_FORCE_RANGE_SET = _PROBE.format(BRACE, _FORCEDR, SPACE, BRACE)
    PROBE_FORCE_RANGE_GET = _PROBE.format(BRACE, _FORCEDR, INTERROGATION, EMPTY)

    PROBE_GAIN_SET = _PROBE.format(BRACE, _GAIN, SPACE, BRACE)
    PROBE_GAIN_GET = _PROBE.format(BRACE, _GAIN, INTERROGATION, EMPTY)

    PROBE_ID_GET = _PROBE.format(BRACE, _ID, INTERROGATION, EMPTY)
    PROBE_SN_GET = _PROBE.format(BRACE, _SER, INTERROGATION, EMPTY)
    PROBE_TYPE_GET = _PROBE.format(BRACE, _ID, _TYP, INTERROGATION)
    PROBE_MODEL_SET = _PROBE.format(BRACE, _MOD, SPACE, BRACE)
    PROBE_MODEL_GET = _PROBE.format(BRACE, _MOD, INTERROGATION, EMPTY)

    PROBE_PROP_DELAY_SET = _PROBE.format(BRACE, _PROPDEL, SPACE, BRACE)
    PROBE_PROP_DELAY_GET = _PROBE.format(BRACE, _PROPDEL, INTERROGATION, EMPTY)

    PROBE_DESKEW_GET = _PROBE.format(BRACE, _RECDES, INTERROGATION, EMPTY)
    PROBE_RESISTANCE_GET = _PROBE.format(BRACE, _RES, INTERROGATION, EMPTY)

    PROBE_SIGNAL_SET = _PROBE.format(BRACE, _SIG, SPACE, BRACE)
    PROBE_SIGNAL_GET = _PROBE.format(BRACE, _SIG, INTERROGATION, EMPTY)

    PROBE_UNITS_GET = _PROBE.format(BRACE, _UNI, INTERROGATION, EMPTY)

    PROBE_OPERATION_DICT = {PROBE_AUTO_ZERO: PROBE_AUTO_ZERO_EXEC,
                            PROBE_CALIBRATE_STATE: PROBE_CALIBRATE_STATE_GET,
                            PROBE_DEGAUSS: PROBE_DEGAUSS_EXEC,
                            PROBE_DEGAUSS_STATE: PROBE_DEGAUSS_STATE_GET,
                            PROBE_FORCE_RANGE: PROBE_FORCE_RANGE_GET,
                            PROBE_GAIN: PROBE_GAIN_GET,
                            PROBE_ID: PROBE_ID_GET,
                            # PROBE_SN:PROBE_SN_GET,
                            PROBE_TYPE: PROBE_TYPE_GET,
                            PROBE_MODEL: PROBE_MODEL_GET,
                            PROBE_PROP_DELAY: PROBE_PROP_DELAY_GET,
                            PROBE_DESKEW: PROBE_DESKEW_GET,
                            PROBE_RESISTANCE: PROBE_RESISTANCE_GET,
                            PROBE_SIGNAL: PROBE_SIGNAL_GET,
                            PROBE_UNITS: PROBE_UNITS_GET}
    #  Calibrate Execute initialize, Range, Gain, Prop delay, Signal
    PROBE_SET_DICT = {PROBE_CALIBRATE: PROBE_CALIBRATE_SET, PROBE_FORCE_RANGE: PROBE_FORCE_RANGE_SET,
                      PROBE_GAIN: PROBE_GAIN_SET,
                      PROBE_PROP_DELAY: PROBE_PROP_DELAY_SET, PROBE_SIGNAL: PROBE_SIGNAL_SET}

    _CONFIG = '{}{}{}{}'.format(CONFIG, BRACE, BRACE, INTERROGATION)
    ADV_MATH = _CONFIG.format(_ADVMATH, EMPTY)
    AFG = _CONFIG.format(_AFG, EMPTY)
    ANALOG_BANDWIDTH = _CONFIG.format(_ANALO, _BANDW)
    ANALOG_GND_CPLG = _CONFIG.format(_ANALO, _GNDCPLG)
    ANALOG_MAX_SAMPLE_RATE = _CONFIG.format(_ANALO, _MAXSAMPLER)
    ANALOG_NUM_CH = _CONFIG.format(_ANALO, _NUMCHAN)
    ANALOG_REC_LEN = _CONFIG.format(_ANALO, _RECLENS)
    ANALOG_VERT_INVERT = _CONFIG.format(_ANALO, _VERTINV)
    APP_CUST_MASK = _CONFIG.format(_APPL, _CUSTOMM)
    APP_LIMIT_MASK = _CONFIG.format(_APPL, _LIMITM)
    APP_POWER = _CONFIG.format(_APPL, _POW)
    APP_STD_MASK = _CONFIG.format(_APPL, _STANDARDM)
    APP_VID_PIC = _CONFIG.format(_APPL, _VIDPIC)
    ARB = _CONFIG.format(_ARB, EMPTY)
    AUXIN = _CONFIG.format(_AUXIN, EMPTY)
    DIGITAL_MAGNIVU = _CONFIG.format(_DIGITA, _MAG)
    DIGITAL_MAX_SAMPLE_RATE = _CONFIG.format(_DIGITA, _MAXSAMPLER)
    DIGITAL_NUM_CH = _CONFIG.format(_DIGITA, _NUMCHAN)
    DVM = _CONFIG.format(_DVM, EMPTY)
    EXT_VIDEO = _CONFIG.format(_EXTVIDEO, EMPTY)
    HISTOGRAM = _CONFIG.format(_HISTOGRAM, EMPTY)
    NET_DRV = _CONFIG.format(_NETWORKDRIVES, EMPTY)
    NUM_MEAS = _CONFIG.format(_NUMMEAS, EMPTY)
    REFS_NUM_REFS = _CONFIG.format(_REFS, _NUMREFS)
    RF_ADV_TRIG = _CONFIG.format(_RF, _ADVTRIG)
    RF_BANDWIDTH = _CONFIG.format(_RF, _BANDW)
    RF_NUM_CH = _CONFIG.format(_RF, _NUMCHAN)
    ROSC = _CONFIG.format(_ROSC, EMPTY)
    CONFIG_DICT = {
        'adv_math': ADV_MATH,
        'afg': AFG,
        'bandwidth': ANALOG_BANDWIDTH,
        'gnd_cplg': ANALOG_GND_CPLG,
        'samp_rate': ANALOG_MAX_SAMPLE_RATE,
        'num_ch': ANALOG_NUM_CH,
        'rec_len': ANALOG_REC_LEN,
        'vert_inv': ANALOG_VERT_INVERT,
        'cust_mask': APP_CUST_MASK,
        'limit_mask': APP_LIMIT_MASK,
        'power': APP_POWER,
        'std_mask': APP_STD_MASK,
        'vid_pic': APP_VID_PIC,
        'arb': ARB,
        'aux_in': AUXIN,
        'mag': DIGITAL_MAGNIVU,
        'dig_samp_rate': DIGITAL_MAX_SAMPLE_RATE,
        'dig_num_ch': DIGITAL_NUM_CH,
        'dvm': DVM,
        'ext_video': EXT_VIDEO,
        'hist': HISTOGRAM,
        'net_drv': NET_DRV,
        'num_meas': NUM_MEAS,
        'num_ref': REFS_NUM_REFS,
        'adv_trig': RF_ADV_TRIG,
        'rf_bandw': RF_BANDWIDTH,
        'rf_num_ch': RF_NUM_CH,
        'rosc': ROSC,
    }

    _CURSOR = '{}{}{}{}'.format(CURS, BRACE, BRACE, BRACE)
    CURSOR_FUNC_SET = _CURSOR.format(_FUNC, SPACE, BRACE)
    CURSOR_FUNC_GET = _CURSOR.format(_FUNC, INTERROGATION, EMPTY)
    CURSOR_HBARS_GET = _CURSOR.format(_HBA, INTERROGATION, EMPTY)
    _CURSOR_HBARS = '{}{}{}{}{}{}'.format(CURS, _HBA, BRACE, BRACE, BRACE, BRACE)
    CURSOR_HBARS_DELTA_GET = _CURSOR_HBARS.format(_DELT, INTERROGATION, EMPTY, EMPTY)
    CURSOR_HBARS_POSITION_SET = _CURSOR_HBARS.format(_POSITION, BRACE, SPACE, BRACE)
    CURSOR_HBARS_POSITION_GET = _CURSOR_HBARS.format(_POSITION, BRACE, INTERROGATION, EMPTY)
    CURSOR_HBARS_UNITS_SET = _CURSOR_HBARS.format(_UNI, SPACE, BRACE, EMPTY)
    CURSOR_HBARS_UNITS_GET = _CURSOR_HBARS.format(_UNI, INTERROGATION, EMPTY, EMPTY)
    CURSOR_HBARS_USE_SET = _CURSOR_HBARS.format(_USE, SPACE, BRACE, EMPTY)
    CURSOR_MODE_SET = _CURSOR.format(_MOD, SPACE, BRACE)
    CURSOR_MODE_GET = _CURSOR.format(_MOD, INTERROGATION, EMPTY)
    CURSOR_SOURCE_SET = _CURSOR.format(_SOU, SPACE, BRACE)
    CURSOR_SOURCE_GET = _CURSOR.format(_SOU, INTERROGATION, EMPTY)
    _CURSOR_VBARS = '{}{}{}{}{}{}'.format(CURS, _VBA, BRACE, BRACE, BRACE, BRACE)
    CURSOR_VBARS_GET = _CURSOR.format(_VBA, INTERROGATION, EMPTY)
    CURSOR_VBARS_ALTERNATE_GET = _CURSOR_VBARS.format(_ALTERNATE, BRACE, INTERROGATION, EMPTY)
    CURSOR_VBARS_DELTA_GET = _CURSOR_VBARS.format(_DELT, INTERROGATION, EMPTY, EMPTY)
    CURSOR_VBARS_HPOS_GET = _CURSOR_VBARS.format(_HPOS, BRACE, INTERROGATION, EMPTY)
    CURSOR_VBARS_POSITION_SET = _CURSOR_VBARS.format(_POSITION, BRACE, SPACE, BRACE)
    CURSOR_VBARS_POSITION_GET = _CURSOR_VBARS.format(_POSITION, BRACE, INTERROGATION, EMPTY)
    CURSOR_VBARS_UNITS_SET = _CURSOR_VBARS.format(_UNI, SPACE, BRACE, EMPTY)
    CURSOR_VBARS_UNITS_GET = _CURSOR_VBARS.format(_UNI, INTERROGATION, EMPTY, EMPTY)
    CURSOR_VBARS_USE_SET = _CURSOR_VBARS.format(_USE, SPACE, BRACE, EMPTY)
    CURSOR_VBARS_VDELTA_GET = _CURSOR_VBARS.format(_VDELT, INTERROGATION, EMPTY, EMPTY)
    _CURSOR_XY = '{}{}{}{}{}{}{}'.format(CURS, _XY, BRACE, BRACE, BRACE, BRACE, BRACE)
    CURSOR_POLAR_RADIUS_DELTA_GET = _CURSOR_XY.format(_POL, _RADIUS, _DELT, INTERROGATION, EMPTY)
    CURSOR_POLAR_RADIUS_POSITION_GET = _CURSOR_XY.format(_POL, _RADIUS, _POSITION, BRACE, INTERROGATION)
    CURSOR_POLAR_RADIUS_UNITS_GET = _CURSOR_XY.format(_POL, _RADIUS, _UNI, INTERROGATION, EMPTY)
    CURSOR_POLAR_THETA_DELTA_GET = _CURSOR_XY.format(_POL, _THETA, _DELT, INTERROGATION, EMPTY)
    CURSOR_POLAR_THETA_POSITION_GET = _CURSOR_XY.format(_POL, _THETA, _POSITION, BRACE, INTERROGATION)
    CURSOR_POLAR_THETA_UNITS_GET = _CURSOR_XY.format(_POL, _THETA, _UNI, INTERROGATION, EMPTY)
    CURSOR_PRODUCT_DELTA_GET = _CURSOR_XY.format(_PRODUCT, _DELT, INTERROGATION, EMPTY, EMPTY)
    CURSOR_PRODUCT_POSITION_GET = _CURSOR_XY.format(_PRODUCT, _POSITION, BRACE, INTERROGATION, EMPTY)
    CURSOR_PRODUCT_UNITS_GET = _CURSOR_XY.format(_PRODUCT, _UNI, INTERROGATION, EMPTY, EMPTY)
    CURSOR_RATIO_DELTA_GET = _CURSOR_XY.format(_RATIO, _DELT, INTERROGATION, EMPTY, EMPTY)
    CURSOR_RATIO_POSITION_GET = _CURSOR_XY.format(_RATIO, _POSITION, BRACE, INTERROGATION, EMPTY)
    CURSOR_RATIO_UNITS_GET = _CURSOR_XY.format(_RATIO, _UNI, INTERROGATION, EMPTY, EMPTY)
    CURSOR_READOUT_SET = _CURSOR_XY.format(_READOUT, SPACE, BRACE, EMPTY, EMPTY)
    CURSOR_READOUT_GET = _CURSOR_XY.format(_READOUT, INTERROGATION, EMPTY, EMPTY, EMPTY)
    CURSOR_X_DELTA_GET = _CURSOR_XY.format(_RECT, _X, _DELT, INTERROGATION, EMPTY)
    CURSOR_X_POSITION_SET = _CURSOR_XY.format(_RECT, _X, _POSITION, BRACE, SPACE + BRACE)
    CURSOR_X_POSITION_GET = _CURSOR_XY.format(_RECT, _X, _POSITION, BRACE, INTERROGATION)
    CURSOR_X_UNITS_GET = _CURSOR_XY.format(_RECT, _X, _UNI, INTERROGATION, EMPTY)
    CURSOR_Y_DELTA_GET = _CURSOR_XY.format(_RECT, _Y, _DELT, INTERROGATION, EMPTY)
    CURSOR_Y_POSITION_SET = _CURSOR_XY.format(_RECT, _Y, _POSITION, BRACE, SPACE + BRACE)
    CURSOR_Y_POSITION_GET = _CURSOR_XY.format(_RECT, _Y, _POSITION, BRACE, INTERROGATION)
    CURSOR_Y_UNITS_GET = _CURSOR_XY.format(_RECT, _Y, _UNI, INTERROGATION, EMPTY)

    CURSOR_GET_DICT = {
        'func': CURSOR_FUNC_GET,
        # 'h_bar':CURSOR_HBARS_GET,
        'h_delta': CURSOR_HBARS_DELTA_GET,
        'h_pos1': CURSOR_HBARS_POSITION_GET.format(1),
        'h_pos2': CURSOR_HBARS_POSITION_GET.format(2),
        'h_unit': CURSOR_HBARS_UNITS_GET,
        'mode': CURSOR_MODE_GET,
        'source': CURSOR_SOURCE_GET,
        # 'v_bar':CURSOR_VBARS_GET,
        'v_alt1': CURSOR_VBARS_ALTERNATE_GET.format(1),
        'v_alt2': CURSOR_VBARS_ALTERNATE_GET.format(2),
        'v_delta': CURSOR_VBARS_DELTA_GET,
        'v_hpos1': CURSOR_VBARS_HPOS_GET.format(1),
        'v_hpos2': CURSOR_VBARS_HPOS_GET.format(2),
        'v_pos1': CURSOR_VBARS_POSITION_GET.format(1),
        'v_pos2': CURSOR_VBARS_POSITION_GET.format(2),
        'v_unit': CURSOR_VBARS_UNITS_GET,
        'v_vdelta': CURSOR_VBARS_VDELTA_GET,
        'pr_delta': CURSOR_POLAR_RADIUS_DELTA_GET,
        'pr_pos1': CURSOR_POLAR_RADIUS_POSITION_GET.format(1),
        'pr_pos2': CURSOR_POLAR_RADIUS_POSITION_GET.format(2),
        'pr_unit': CURSOR_POLAR_RADIUS_UNITS_GET,
        'pt_delta': CURSOR_POLAR_THETA_DELTA_GET,
        'pt_pos1': CURSOR_POLAR_THETA_POSITION_GET.format(1),
        'pt_pos2': CURSOR_POLAR_THETA_POSITION_GET.format(2),
        'pt_unit': CURSOR_POLAR_THETA_UNITS_GET,
        'p_delta': CURSOR_PRODUCT_DELTA_GET,
        'p_pos1': CURSOR_PRODUCT_POSITION_GET.format(1),
        'p_pos2': CURSOR_PRODUCT_POSITION_GET.format(2),
        'p_unit': CURSOR_PRODUCT_UNITS_GET,
        'r_delta': CURSOR_RATIO_DELTA_GET,
        'r_pos1': CURSOR_RATIO_POSITION_GET.format(1),
        'r_pos2': CURSOR_RATIO_POSITION_GET.format(2),
        'r_unit': CURSOR_RATIO_UNITS_GET,
        'readout': CURSOR_READOUT_GET,
        'rx_delta': CURSOR_X_DELTA_GET,
        'rx_pos1': CURSOR_X_POSITION_GET.format(1),
        'rx_pos2': CURSOR_X_POSITION_GET.format(2),
        'rx_unit': CURSOR_X_UNITS_GET,
        'ry_delta': CURSOR_Y_DELTA_GET,
        'ry_pos1': CURSOR_Y_POSITION_GET.format(1),
        'ry_pos2': CURSOR_Y_POSITION_GET.format(2),
        'ry_unit': CURSOR_Y_UNITS_GET,
    }

    CURSOR_SET_DICT = {
        'func': CURSOR_FUNC_SET,
        'h_pos1': CURSOR_HBARS_POSITION_SET.format(1, BRACE),
        'h_pos2': CURSOR_HBARS_POSITION_SET.format(2, BRACE),
        'h_unit': CURSOR_HBARS_UNITS_SET,
        'h_use': CURSOR_HBARS_USE_SET,
        'mode': CURSOR_MODE_SET,
        'source': CURSOR_SOURCE_SET,
        'v_pos1': CURSOR_VBARS_POSITION_SET.format(1, BRACE),
        'v_pos2': CURSOR_VBARS_POSITION_SET.format(2, BRACE),
        'v_unit': CURSOR_VBARS_UNITS_SET,
        'v_use': CURSOR_VBARS_USE_SET,
        'readout': CURSOR_READOUT_SET,
        'rx_pos1': CURSOR_X_POSITION_SET.format(1, BRACE),
        'rx_pos2': CURSOR_X_POSITION_SET.format(2, BRACE),
        'ry_pos1': CURSOR_Y_POSITION_SET.format(1, BRACE),
        'ry_pos2': CURSOR_Y_POSITION_SET.format(2, BRACE),
    }

    DATE_SET = '{}{}{}'.format(DATE, SPACE, BRACE)
    DATE_GET = '{}{}{}'.format(DATE, INTERROGATION, SPACE)
    TIME_SET = '{}{}{}'.format(TIME, SPACE, BRACE)
    TIME_GET = '{}{}{}'.format(TIME, INTERROGATION, SPACE)

    DATE_TIME_SET_DICT = {'d': DATE_SET, 't': TIME_SET}
    DATE_TIME_GET_DICT = {'d': DATE_GET, 't': TIME_GET}

    _HORIZONTAL_DELAY = '{}{}{}{}{}'.format(HOR, _DEL, BRACE, BRACE, BRACE)
    HORIZONTAL_DELAY_STATE_SET = _HORIZONTAL_DELAY.format(_MOD, SPACE, BRACE)
    HORIZONTAL_DELAY_STATE_GET = _HORIZONTAL_DELAY.format(_MOD, INTERROGATION, EMPTY)
    HORIZONTAL_DELAY_TIME_SET = _HORIZONTAL_DELAY.format(_TIM, SPACE, BRACE)
    HORIZONTAL_DELAY_TIME_GET = _HORIZONTAL_DELAY.format(_TIM, INTERROGATION, EMPTY)
    _HORIZONTAL = '{}{}{}{}'.format(HOR, BRACE, BRACE, BRACE)
    HORIZONTAL_POSITION_SET = _HORIZONTAL.format(_POS, SPACE, BRACE)
    HORIZONTAL_POSITION_GET = _HORIZONTAL.format(_POS, INTERROGATION, EMPTY)
    HORIZONTAL_RECORD_LENGTH_SET = _HORIZONTAL.format(_RECO, SPACE, BRACE)
    HORIZONTAL_RECORD_LENGTH_GET = _HORIZONTAL.format(_RECO, INTERROGATION, EMPTY)
    # HORIZONTAL_SAMPLE_RATE_SET = _HORIZONTAL.format(_SAMPLER, SPACE, BRACE)
    HORIZONTAL_SAMPLE_RATE_GET = _HORIZONTAL.format(_SAMPLER, INTERROGATION, EMPTY)
    HORIZONTAL_SCALE_SET = _HORIZONTAL.format(_SCA, SPACE, BRACE)
    HORIZONTAL_SCALE_GET = _HORIZONTAL.format(_SCA, INTERROGATION, EMPTY)

    HORIZONTAL_SET_DICT = {
        'del_state': HORIZONTAL_DELAY_STATE_SET,
        'delay': HORIZONTAL_DELAY_TIME_SET,
        'pos': HORIZONTAL_POSITION_SET,
        'rec_len': HORIZONTAL_RECORD_LENGTH_SET,
        # 'sam_len':HORIZONTAL_SAMPLE_RATE_SET,
        'scale': HORIZONTAL_SCALE_SET,
    }
    HORIZONTAL_GET_DICT = {
        'del_state': HORIZONTAL_DELAY_STATE_GET,
        'delay': HORIZONTAL_DELAY_TIME_GET,
        'pos': HORIZONTAL_POSITION_GET,
        'rec_len': HORIZONTAL_RECORD_LENGTH_GET,
        'sam_rate': HORIZONTAL_SAMPLE_RATE_GET,
        'scale': HORIZONTAL_SCALE_GET,
    }

    _REMOTE_ON = 'LOCk ALL'
    _REMOTE_OFF = 'LOCk NONe'

    DICT_REMOTE = {
        OFF: _REMOTE_OFF,
        ZERO: _REMOTE_OFF,
        ON: _REMOTE_ON,
        ONE: _REMOTE_ON,
    }

    TRIG_TYPE_TUPLE = ('edge', 'logic', 'pulse', 'bus', 'video')

    REG_TRIG_MODE = utils.get_regex('^(auto)$|^(norm)(al)?$', IGNORE_CASE)
    REG_TRIG_BY_EVENTS = utils.get_regex('^(EVENTS)$', IGNORE_CASE)
    REG_TRIG_BY_TIME = utils.get_regex('^(tim)(e)?$', IGNORE_CASE)
    REG_LOGICC_LOGIC = utils.get_regex('^(logic)$', IGNORE_CASE)
    REG_LOGICC_SETHOLD = utils.get_regex('^(seth)(old)?$', IGNORE_CASE)

    REG_PULSEC_RUNT = utils.get_regex('^(run)(t)?$', IGNORE_CASE)
    REG_PULSEC_WIDTH = utils.get_regex('^(wid)(th)?$', IGNORE_CASE)
    REG_PULSEC_TRANSITION = utils.get_regex('^(tran)(sition)?$', IGNORE_CASE)
    REG_PULSEC_TIMEOUT = utils.get_regex('^(timeo)(ut)?$', IGNORE_CASE)
    REG_VIDEO_CUSTOM = utils.get_regex('^(bil)(evelcustom)?$|^(tril)(evelcustom)?$', IGNORE_CASE)
    REG_VIDEO_BILEVEL_CUST = utils.get_regex('^(bil)(evelcustom)?$', IGNORE_CASE)

    REG_STATE = utils.get_regex('^(STATE)$', IGNORE_CASE)
    REG_DELAY = utils.get_regex('^(DEL)(ay)?$', IGNORE_CASE)
    REG_PHASE = utils.get_regex('^(PHA)(se)?$', IGNORE_CASE)
    REG_ABSOLUTE = utils.get_regex('^(ABS)(olute)?$', IGNORE_CASE)











