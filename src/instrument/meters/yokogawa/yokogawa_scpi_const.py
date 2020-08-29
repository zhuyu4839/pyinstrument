# -*- encoding: utf-8 -*-
from instrument import utils
from instrument.const import SPACE, BRACE, INTERROGATION, COMMAS, IGNORE_CASE


class Wt300eCmd:

    COMMUNICATE = 'COMM'
    HEADER = ':HEAD'
    LOCKOUT = ':LOCK'
    REMOTE = ':REM'
    STATUS = ':STAT'
    VERBOSE = ':VERB'
    WAIT = ':WAIT'

    DISPLAY = 'DISP'
    NORMAL = ':NORM'
    ITEM = ':ITEM'
    _HARMONICS = ':HARM'

    HARMONICS = 'HARM'
    PLL_SOURCE = ':PLLS'
    ORDER = ':ORD'
    THD = ':THD'                # total harmonic distortion
    _DISPLAY = ':DISP'
    STATE = ':STAT'

    INTEGRATE = 'INTEG'
    MODE = ':MODE'
    TIMER = ':TIMER'
    START = ':STAR'
    STOP = ':STOP'
    RESET = ':RES'

    INPUT = 'INP'
    CURRENT = ':CURR'
    RANGE = ':RANG'
    AUTO = ':AUTO'
    CONFIG = ':CONF'
    PO_JUMP = ':POJ'            # peak over jump
    S_RATIO = ':SRAT'           # sensor conversion ratios
    EXT_SENSOR = ':EXTS'
    ALL = ':ALL'
    ELEMENT = ':ELEM'

    SCALING = ':SCAL'
    VT = ':VT'
    CT = ':CT'
    S_FACTOR = ':SFAC'

    FILTER = ':FILT'
    LINE = ':LINE'
    FREQUENCY = ':FREQ'

    CREST_FACTOR = ':CFAC'
    WIRING = ':WIR'
    RANGE_CONFIG = ':RCON'
    SYNCHRONIZE = ':SYNC'
    PEAK_OVER = ':POV'
    CHECK_RANGE = 'CRAN'

    NUMERIC = 'NUM'
    FORMAT = ':FORM'
    VALUE = ':VAL'
    NUMBER = ':NUM'
    CLEAR = ':CLE'
    DELETE = ':DEL'
    HOLD = ':HOLD'
    PRESET = ':PRES'
    LIST = ':LIST'
    SELECT = ':SEL'

    DICT_COMMUNICATE_SET = {
        'header': '{}{}{}{}'.format(COMMUNICATE, HEADER, SPACE, BRACE),
        'lockout': '{}{}{}{}'.format(COMMUNICATE, LOCKOUT, SPACE, BRACE),
        'remote': '{}{}{}{}'.format(COMMUNICATE, REMOTE, SPACE, BRACE),
        # 'status': '{}{}{}{}'.format(COMMUNICATE, STATUS, SPACE, BRACE),
        'verbose': '{}{}{}{}'.format(COMMUNICATE, VERBOSE, SPACE, BRACE),
        'wait': '{}{}{}{}'.format(COMMUNICATE, WAIT, SPACE, BRACE),
    }
    DICT_COMMUNICATE_GET = {
        'header': '{}{}{}'.format(COMMUNICATE, HEADER, INTERROGATION),
        'lockout': '{}{}{}'.format(COMMUNICATE, LOCKOUT, INTERROGATION),
        'remote': '{}{}{}'.format(COMMUNICATE, REMOTE, INTERROGATION),
        'status': '{}{}{}'.format(COMMUNICATE, STATUS, INTERROGATION),
        'verbose': '{}{}{}'.format(COMMUNICATE, VERBOSE, INTERROGATION),
        'wait': '{}{}{}'.format(COMMUNICATE, WAIT, INTERROGATION),
    }

    DICT_DISPLAY_SET = {
        utils.dict_add({
            'normal{}'.format(i + 1):
                '{}{}{}{}{}{}{}{}'.format(DISPLAY, NORMAL, ITEM, i + 1, SPACE, BRACE, BRACE, BRACE)
                for i in range(4)
        }, {
            'harmonic{}'.format(i + 1):
                '{}{}{}{}{}{}{}{}'.format(DISPLAY, _HARMONICS, ITEM, i + 1, SPACE, BRACE, BRACE, BRACE)
                for i in range(4)
        },
        )
    }
    DICT_DISPLAY_GET = {
        'normals': '{}{}{}'.format(DISPLAY, NORMAL, INTERROGATION),
        'harmonics': '{}{}{}'.format(DISPLAY, _HARMONICS, INTERROGATION),
    }

    DICT_HARMONIC_SET = {
        'harm_plls': '{}{}{}{}'.format(HARMONICS, PLL_SOURCE, SPACE, BRACE),
        'harm_order': '{}{}{}{}'.format(HARMONICS, ORDER, SPACE, BRACE),
        'harm_thd': '{}{}{}{}'.format(HARMONICS, THD, SPACE, BRACE),
        'disp_state': '{}{}{}{}{}'.format(HARMONICS, _DISPLAY, STATE, SPACE, BRACE),
        'disp_order': '{}{}{}{}{}'.format(HARMONICS, _DISPLAY, ORDER, SPACE, BRACE),
    }
    DICT_HARMONIC_GET = {
        'measures': '{}{}'.format(HARMONICS, INTERROGATION),
        'display': '{}{}{}'.format(HARMONICS, _DISPLAY, INTERROGATION)
    }

    DICT_INTEGRATE_SET = {
        'mode': '{}{}{}{}'.format(INTEGRATE, MODE, SPACE, BRACE),
        'timer': '{}{}{}{}{}{}{}{}'.format(INTEGRATE, TIMER, SPACE, BRACE, COMMAS, BRACE, COMMAS, BRACE),
    }
    DICT_INTEGRATE = {
        'mode': '{}{}{}'.format(INTEGRATE, MODE, INTERROGATION),
        'timer': '{}{}{}'.format(INTEGRATE, TIMER, INTERROGATION),
        'start': '{}{}'.format(INTEGRATE, START),
        'stop': '{}{}'.format(INTEGRATE, STOP),
        'reset': '{}{}'.format(INTEGRATE, RESET),
        'state': '{}{}{}'.format(INTEGRATE, STATE, INTERROGATION),
    }

    DICT_INPUT_CURRENT_SET = utils.dict_add({
            'range': '{}{}{}{}{}'.format(INPUT, CURRENT, RANGE, SPACE, BRACE),
            'auto': '{}{}{}{}{}'.format(INPUT, CURRENT, AUTO, SPACE, BRACE),
            'conf': '{}{}{}{}{}'.format(INPUT, CURRENT, CONFIG, SPACE, BRACE),
            'poj': '{}{}{}{}{}'.format(INPUT, CURRENT, PO_JUMP, SPACE, BRACE),
            'ext_conf': '{}{}{}{}{}{}'.format(INPUT, CURRENT, EXT_SENSOR, CONFIG, SPACE, BRACE),
            'ext_poj': '{}{}{}{}{}{}'.format(INPUT, CURRENT, EXT_SENSOR, PO_JUMP, SPACE, BRACE),
            'ratio': '{}{}{}{}{}{}'.format(INPUT, CURRENT, S_RATIO, ALL, SPACE, BRACE),
        },
        {
            'ratio_el{}'.format(i + 1):
                '{}{}{}{}{}{}{}'.format(INPUT, CURRENT, S_RATIO, ELEMENT, i + 1, SPACE, BRACE) for i in range(3)
        }
    )
    DICT_INPUT_CURRENT_GET = utils.dict_add({
            'range': '{}{}{}{}'.format(INPUT, CURRENT, RANGE, INTERROGATION),
            'auto': '{}{}{}{}'.format(INPUT, CURRENT, AUTO, INTERROGATION),
            'conf': '{}{}{}{}'.format(INPUT, CURRENT, CONFIG, INTERROGATION),
            'poj': '{}{}{}{}'.format(INPUT, CURRENT, PO_JUMP, INTERROGATION),
            'ext_conf': '{}{}{}{}{}'.format(INPUT, CURRENT, EXT_SENSOR, CONFIG, INTERROGATION),
            'ext_poj': '{}{}{}{}{}'.format(INPUT, CURRENT, EXT_SENSOR, PO_JUMP, INTERROGATION),
            'ratio': '{}{}{}{}'.format(INPUT, CURRENT, S_RATIO, INTERROGATION),
        },
        {
            'ratio_el{}'.format(i + 1):
                '{}{}{}{}{}{}'.format(INPUT, CURRENT, S_RATIO, ELEMENT, i + 1, INTERROGATION) for i in range(3)
        }
    )

    DICT_INPUT_SCALING_SET = utils.dict_add({
            'state': '{}{}{}{}{}'.format(INPUT, SCALING, STATE, SPACE, BRACE),
            'vt': '{}{}{}{}{}{}'.format(INPUT, SCALING, VT, ALL, SPACE, BRACE),
            'ct': '{}{}{}{}{}{}'.format(INPUT, SCALING, CT, ALL, SPACE, BRACE),
            'factor': '{}{}{}{}{}{}'.format(INPUT, SCALING, S_FACTOR, ALL, SPACE, BRACE),
        },
        {
            'vt_el{}'.format(i + 1):
                '{}{}{}{}{}{}{}'.format(INPUT, SCALING, VT, ELEMENT, i + 1, SPACE, BRACE) for i in range(3)
        },
        {
            'ct_el{}'.format(i + 1):
                '{}{}{}{}{}{}{}'.format(INPUT, SCALING, CT, ELEMENT, i + 1, SPACE, BRACE) for i in range(3)
        },
        {
            'factor_el{}'.format(i + 1):
                '{}{}{}{}{}{}{}'.format(INPUT, SCALING, S_FACTOR, ELEMENT, i + 1, SPACE, BRACE) for i in range(3)
        },
    )
    DICT_INPUT_SCALING_GET = utils.dict_add({
            'state': '{}{}{}{}'.format(INPUT, SCALING, STATE, INTERROGATION),
            'vt': '{}{}{}{}{}'.format(INPUT, SCALING, VT, ALL, INTERROGATION),
            'ct': '{}{}{}{}{}'.format(INPUT, SCALING, CT, ALL, INTERROGATION),
            'factor': '{}{}{}{}'.format(INPUT, SCALING, S_FACTOR, INTERROGATION),
        },
        {
            'vt_el{}'.format(i + 1):
                '{}{}{}{}{}{}'.format(INPUT, SCALING, VT, ELEMENT, i + 1, INTERROGATION) for i in range(3)
        },
        {
            'ct_el{}'.format(i + 1):
                '{}{}{}{}{}{}'.format(INPUT, SCALING, CT, ELEMENT, i + 1, INTERROGATION) for i in range(3)
        },
        {
            'factor_el{}'.format(i + 1):
                '{}{}{}{}{}{}'.format(INPUT, SCALING, S_FACTOR, ELEMENT, i + 1, INTERROGATION) for i in range(3)
        },
    )

    DICT_INPUT_FILTER_SET = {
        'line': '{}{}{}{}{}'.format(INPUT, FILTER, LINE, SPACE, BRACE),
        'freq': '{}{}{}{}{}'.format(INPUT, FILTER, FREQUENCY, SPACE, BRACE),
    }

    DICT_INPUT_OTHERS_SET = {
        'crest_fac': '{}{}{}{}'.format(INPUT, CREST_FACTOR, SPACE, BRACE),
        'wiring': '{}{}{}{}'.format(INPUT, WIRING, SPACE, BRACE),
        'mode': '{}{}{}{}'.format(INPUT, MODE, SPACE, BRACE),
        'rconf': '{}{}{}{}'.format(INPUT, RANGE_CONFIG, SPACE, BRACE),
        'sync': '{}{}{}{}'.format(INPUT, SYNCHRONIZE, SPACE, BRACE),
        # 'peak_over': '{}{}{}{}'.format(INPUT, PEAK_OVER, SPACE, BRACE),
        # 'check_range': '{}{}{}{}'.format(INPUT, CHECK_RANGE, SPACE, BRACE),
    }
    DICT_INPUT_OTHERS_GET = {
        'crest_fac': '{}{}{}'.format(INPUT, CREST_FACTOR, INTERROGATION),
        'wiring': '{}{}{}'.format(INPUT, WIRING, INTERROGATION),
        'mode': '{}{}{}'.format(INPUT, MODE, INTERROGATION),
        'rconf': '{}{}{}'.format(INPUT, RANGE_CONFIG, INTERROGATION),
        'sync': '{}{}{}'.format(INPUT, SYNCHRONIZE, INTERROGATION),
        'peak_over': '{}{}{}'.format(INPUT, PEAK_OVER, INTERROGATION),
        'check_range': '{}{}{}'.format(INPUT, CHECK_RANGE, INTERROGATION),
    }

    REGEX_NUMERIC_FORMAT = utils.get_regex('^ASC(ii)?$|^FLO(at)?$', IGNORE_CASE)

    DICT_NUMERIC_SET = {
        'fmt': '{}{}{}{}'.format(NUMERIC, FORMAT, SPACE, BRACE),
        'hold': '{}{}{}{}'.format(NUMERIC, HOLD, SPACE, BRACE),
    }
    DICT_NUMERIC_GET = {
        'fmt': '{}{}{}'.format(NUMERIC, FORMAT, INTERROGATION),
        'hold': '{}{}{}'.format(NUMERIC, HOLD, INTERROGATION),
    }

    DICT_NUMERIC_NORMAL_SET = utils.dict_add({
            'number': '{}{}{}{}{}'.format(NUMERIC, NORMAL, NUMBER, SPACE, BRACE),
            'clear': '{}{}{}{}{}'.format(NUMERIC, NORMAL, CLEAR, SPACE, BRACE),
            'delete': '{}{}{}{}{}'.format(NUMERIC, NORMAL, DELETE, SPACE, BRACE),
            'preset': '{}{}{}{}{}'.format(NUMERIC, NORMAL, PRESET, SPACE, BRACE),
        },
        {
            'item{}'.format(i + 1):
                '{}{}{}{}{}{}'.format(NUMERIC, NORMAL, ITEM, i + 1, SPACE, BRACE) for i in range(255)
        }
    )
    DICT_NUMERIC_NORMAL_GET = utils.dict_add({
            'number': '{}{}{}{}'.format(NUMERIC, NORMAL, NUMBER, INTERROGATION),
            # 'clear': '{}{}{}{}'.format(NUMERIC, NORMAL, CLEAR, INTERROGATION),
            # 'delete': '{}{}{}{}'.format(NUMERIC, NORMAL, DELETE, INTERROGATION),
            # 'preset': '{}{}{}{}'.format(NUMERIC, NORMAL, PRESET, INTERROGATION),
            'header': '{}{}{}{}{}{}'.format(NUMERIC, NORMAL, HEADER, INTERROGATION, SPACE, BRACE),
            'value': '{}{}{}{}{}{}'.format(NUMERIC, NORMAL, VALUE, INTERROGATION, SPACE, BRACE),
        },
        {
            'item{}'.format(i + 1):
                '{}{}{}{}{}'.format(NUMERIC, NORMAL, ITEM, i + 1, INTERROGATION) for i in range(255)
        }
    )

    DICT_NUMERIC_LIST_SET = utils.dict_add({
            'number': '{}{}{}{}{}'.format(NUMERIC, LIST, NUMBER, SPACE, BRACE),
            'order': '{}{}{}{}{}'.format(NUMERIC, LIST, ORDER, SPACE, BRACE),
            'select': '{}{}{}{}{}'.format(NUMERIC, LIST, SELECT, SPACE, BRACE),
            'preset': '{}{}{}{}{}'.format(NUMERIC, LIST, PRESET, SPACE, BRACE),
            'clear': '{}{}{}{}{}'.format(NUMERIC, LIST, CLEAR, SPACE, BRACE),
            'delete': '{}{}{}{}{}'.format(NUMERIC, LIST, DELETE, SPACE, BRACE),
        },
        {
            'item{}'.format(i + 1):
                '{}{}{}{}{}{}'.format(NUMERIC, LIST, ITEM, i + 1, SPACE, BRACE) for i in range(32)
        }
    )
    DICT_NUMERIC_LIST_GET = utils.dict_add({
            'number': '{}{}{}{}'.format(NUMERIC, LIST, NUMBER, INTERROGATION),
            'order': '{}{}{}{}'.format(NUMERIC, LIST, ORDER, INTERROGATION),
            'select': '{}{}{}{}'.format(NUMERIC, LIST, SELECT, INTERROGATION),
            # 'preset': '{}{}{}{}'.format(NUMERIC, LIST, PRESET, INTERROGATION),
            # 'clear': '{}{}{}{}'.format(NUMERIC, LIST, CLEAR, INTERROGATION),
            # 'delete': '{}{}{}{}'.format(NUMERIC, LIST, DELETE, INTERROGATION),
            'value': '{}{}{}{}'.format(NUMERIC, LIST, VALUE, INTERROGATION),
        },
        {
            'item{}'.format(i + 1):
                '{}{}{}{}{}'.format(NUMERIC, LIST, ITEM, i + 1, INTERROGATION) for i in range(32)
        }
    )

