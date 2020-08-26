# -*- encoding: utf-8 -*-
from instrument.const import INTERROGATION, SPACE, BRACE

CMD_SET_RIGOL = 'RIGOL'
CMD_SET_AGILENT = 'AGILENT'
CMD_SET_FLUKE = 'FLUKE'

CMD_SET = 'CMDSET {}'


class Md3058RigolCmd:

    FUNCTION = 'FUNC'
    FUNCTION2 = 'FUNC2'
    VOLTAGE = ':VOLT'
    CURRENT = ':CURR'
    AC = ':AC'
    DC = ':DC'
    RESISTANCE = ':RES'
    FRESISTANCE = ':FRES'
    FREQUENCY = ':FREQ'
    PERIOD = ':PER'
    CONTINUITY = ':CONT'
    DIODE = ':DIOD'
    CAPACITY = ':CAP'

    MEASURE = 'MEAS'
    RANGE = ':RANG'
    IMPEDANCE = ':IMPE'
    FILTER = ':FILT'
    STATE = ':STAT'
    VALUE = ':VALUE'

    RATE = 'RATE'
    SENSOR = ':SENS'

    TRIGGER = 'TRIG'
    SOURCE = ':SOUR'
    AUTO = ':AUTO'
    INTERVAL = ':INTE'
    HOLD = ':HOLD'
    SENSITIVITY = ':SENS'
    SINGLE = ':SING'
    TRIGGERED = ':TRIG'
    EXT = ':EXT'
    VM_COMPLETE = ':VMC'
    POLAR = ':POLA'
    PULSE_WIDTH = ':PULS'

    CALCULATE = 'CALC'
    _FUNCTION = ':FUNC'
    STATISTIC = ':STAT'
    MIN = ':MIN'
    MAX = ':MAX'
    AVERAGE = ':AVER'
    COUNT = ':COUN'
    REL = ':REL'
    OFFSET = ':OFFS'
    DB = ':DB'
    REFERENCE = ':REFE'
    DBM = ':DBM'
    PF = ':PF'
    LOWER = ':LOWE'
    UPPER = ':UPPE'

    FUNC_GET = '{}{}'.format(FUNCTION, INTERROGATION)
    FUNC2_GET = '{}{}'.format(FUNCTION2, INTERROGATION)

    DICT_FUNC_SET = {
        'ac_volt': '{}{}{}{}'.format(FUNCTION, VOLTAGE, AC, BRACE),
        'dc_volt': '{}{}{}{}'.format(FUNCTION, VOLTAGE, DC, BRACE),
        'ac_curr': '{}{}{}{}'.format(FUNCTION, CURRENT, AC, BRACE),
        'dc_curr': '{}{}{}{}'.format(FUNCTION, CURRENT, DC, BRACE),
        'res': '{}{}{}'.format(FUNCTION, RESISTANCE, BRACE),
        'fres': '{}{}{}'.format(FUNCTION, FRESISTANCE, BRACE),
        'freq': '{}{}{}'.format(FUNCTION, FREQUENCY, BRACE),
        'per': '{}{}{}'.format(FUNCTION, PERIOD, BRACE),
        'cont': '{}{}{}'.format(FUNCTION, CONTINUITY, BRACE),
        'dio': '{}{}{}'.format(FUNCTION, DIODE, BRACE),
        'cap': '{}{}{}'.format(FUNCTION, CAPACITY, BRACE),
    }

    DICT_FUNC2_SET = {
        'ac_volt': '{}{}{}{}'.format(FUNCTION2, VOLTAGE, AC, BRACE),
        'dc_volt': '{}{}{}{}'.format(FUNCTION2, VOLTAGE, DC, BRACE),
        'ac_curr': '{}{}{}{}'.format(FUNCTION2, CURRENT, AC, BRACE),
        'dc_curr': '{}{}{}{}'.format(FUNCTION2, CURRENT, DC, BRACE),
        'res': '{}{}{}'.format(FUNCTION2, RESISTANCE, BRACE),
        'fres': '{}{}{}'.format(FUNCTION2, FRESISTANCE, BRACE),
        'freq': '{}{}{}'.format(FUNCTION2, FREQUENCY, BRACE),
        'per': '{}{}{}'.format(FUNCTION2, PERIOD, BRACE),
        'cont': '{}{}{}'.format(FUNCTION2, CONTINUITY, BRACE),
        'dio': '{}{}{}'.format(FUNCTION2, DIODE, BRACE),
        'cap': '{}{}{}'.format(FUNCTION2, CAPACITY, BRACE),
    }

    DICT_MEASURE_SET = {
        'mode': '{}{}{}'.format(MEASURE, SPACE, BRACE),
        'dc_volt_range': '{}{}{}{}{}'.format(MEASURE, VOLTAGE, DC, SPACE, BRACE),
        'dc_volt_imp': '{}{}{}{}{}{}'.format(MEASURE, VOLTAGE, DC, IMPEDANCE, SPACE, BRACE),
        'dc_volt_flt': '{}{}{}{}{}{}{}'.format(MEASURE, VOLTAGE, DC, FILTER, STATE, SPACE, BRACE),
        'ac_volt_range': '{}{}{}{}{}'.format(MEASURE, VOLTAGE, AC, SPACE, BRACE),
        'dc_curr_range': '{}{}{}{}{}'.format(MEASURE, CURRENT, DC, SPACE, BRACE),
        'dc_curr_flt': '{}{}{}{}{}{}{}'.format(MEASURE, CURRENT, DC, FILTER, STATE, SPACE, BRACE),
        'ac_curr_range': '{}{}{}{}{}'.format(MEASURE, CURRENT, AC, SPACE, BRACE),
        'res_range': '{}{}{}{}'.format(MEASURE, RESISTANCE, SPACE, BRACE),
        'fres_range': '{}{}{}{}'.format(MEASURE, FRESISTANCE, SPACE, BRACE),
        'fv_range': '{}{}{}'.format(MEASURE, FREQUENCY, SPACE, BRACE),
        'pv_range': '{}{}{}'.format(MEASURE, PERIOD, SPACE, BRACE),
        'cont_range': '{}{}{}'.format(MEASURE, CONTINUITY, SPACE, BRACE),
        'cap_range': '{}{}{}'.format(MEASURE, CAPACITY, SPACE, BRACE),
    }

    DICT_MEASURE_GET = {
        'dc_volt_value': '{}{}{}{}{}'.format(MEASURE, VOLTAGE, DC, VALUE, INTERROGATION),
        'dc_volt_range': '{}{}{}{}{}'.format(MEASURE, VOLTAGE, DC, RANGE, INTERROGATION),
        'dc_volt_imp': '{}{}{}{}{}'.format(MEASURE, VOLTAGE, DC, IMPEDANCE, INTERROGATION),
        'dc_volt_flt': '{}{}{}{}{}'.format(MEASURE, VOLTAGE, DC, FILTER, INTERROGATION),
        'ac_volt_value': '{}{}{}{}{}'.format(MEASURE, VOLTAGE, AC, VALUE, INTERROGATION),
        'ac_volt_range': '{}{}{}{}{}'.format(MEASURE, VOLTAGE, AC, RANGE, INTERROGATION),
        'dc_curr_value': '{}{}{}{}{}'.format(MEASURE, CURRENT, DC, VALUE, INTERROGATION),
        'dc_curr_range': '{}{}{}{}{}'.format(MEASURE, CURRENT, DC, RANGE, INTERROGATION),
        'dc_curr_flt': '{}{}{}{}{}'.format(MEASURE, CURRENT, DC, FILTER, INTERROGATION),
        'ac_curr_value': '{}{}{}{}{}'.format(MEASURE, CURRENT, AC, VALUE, INTERROGATION),
        'ac_curr_range': '{}{}{}{}{}'.format(MEASURE, CURRENT, AC, RANGE, INTERROGATION),
        'res_value': '{}{}{}'.format(MEASURE, RESISTANCE, INTERROGATION),
        'res_range': '{}{}{}{}'.format(MEASURE, RESISTANCE, RANGE, INTERROGATION),
        'fres_value': '{}{}{}'.format(MEASURE, FRESISTANCE, INTERROGATION),
        'fres_range': '{}{}{}{}'.format(MEASURE, FRESISTANCE, RANGE, INTERROGATION),
        'freq_value': '{}{}{}'.format(MEASURE, FREQUENCY, INTERROGATION),
        'fv_range': '{}{}{}{}'.format(MEASURE, FREQUENCY, RANGE, BRACE),
        'per_value': '{}{}{}'.format(MEASURE, PERIOD, INTERROGATION),
        'pv_range': '{}{}{}{}'.format(MEASURE, PERIOD, RANGE, BRACE),
        'cont_value': '{}{}{}'.format(MEASURE, CONTINUITY, INTERROGATION),
        'dio_volt': '{}{}{}'.format(MEASURE, DIODE, INTERROGATION),
        'cap_value': '{}{}{}'.format(MEASURE, CAPACITY, INTERROGATION),
        'cap_range': '{}{}{}{}'.format(MEASURE, CAPACITY, RANGE, INTERROGATION),
    }

    DICT_MEASURE_RATE_SET = {
        'dc_volt': '{}{}{}{}{}'.format(RATE, VOLTAGE, DC, SPACE, BRACE),
        'ac_volt': '{}{}{}{}{}'.format(RATE, VOLTAGE, AC, SPACE, BRACE),
        'dc_curr': '{}{}{}{}{}'.format(RATE, CURRENT, DC, SPACE, BRACE),
        'ac_curr': '{}{}{}{}{}'.format(RATE, CURRENT, AC, SPACE, BRACE),
        'res': '{}{}{}{}'.format(RATE, RESISTANCE, SPACE, BRACE),
        'fres': '{}{}{}{}'.format(RATE, FRESISTANCE, SPACE, BRACE),
        'sensor': '{}{}{}{}'.format(RATE, SENSOR, SPACE, BRACE)
    }

    DICT_MEASURE_RATE_GET = {
        'dc_volt': '{}{}{}{}'.format(RATE, VOLTAGE, DC, INTERROGATION),
        'ac_volt': '{}{}{}{}'.format(RATE, VOLTAGE, AC, INTERROGATION),
        'dc_curr': '{}{}{}{}'.format(RATE, CURRENT, DC, INTERROGATION),
        'ac_curr': '{}{}{}{}'.format(RATE, CURRENT, AC, INTERROGATION),
        'res': '{}{}{}'.format(RATE, RESISTANCE, INTERROGATION),
        'fres': '{}{}{}'.format(RATE, FRESISTANCE, INTERROGATION),
        'sensor': '{}{}{}'.format(RATE, SENSOR, INTERROGATION)
    }

    DICT_TRIGGER_SET = {
        'source': '{}{}{}{}'.format(TRIGGER, SOURCE, SPACE, BRACE),
        'inter': '{}{}{}{}{}'.format(TRIGGER, AUTO, INTERVAL, SPACE, BRACE),
        'hold': '{}{}{}{}{}'.format(TRIGGER, AUTO, HOLD, SPACE, BRACE),
        'sens': '{}{}{}{}{}{}'.format(TRIGGER, AUTO, HOLD, SENSITIVITY, SPACE, BRACE),
        'count': '{}{}{}{}'.format(TRIGGER, SINGLE, SPACE, BRACE),
        'ext': '{}{}{}{}'.format(TRIGGER, EXT, SPACE, BRACE),
        'polar': '{}{}{}{}{}'.format(TRIGGER, VM_COMPLETE, POLAR, SPACE, BRACE),
        'w_pulse': '{}{}{}{}{}'.format(TRIGGER, VM_COMPLETE, POLAR, SPACE, BRACE),
    }

    DICT_TRIGGER_GET = {
        'source': '{}{}{}'.format(TRIGGER, SOURCE, INTERROGATION),
        'inter': '{}{}{}{}'.format(TRIGGER, AUTO, INTERVAL, INTERROGATION),
        'hold': '{}{}{}{}'.format(TRIGGER, AUTO, HOLD, INTERROGATION),
        'sens': '{}{}{}{}{}'.format(TRIGGER, AUTO, HOLD, SENSITIVITY, INTERROGATION),
        'count': '{}{}{}'.format(TRIGGER, SINGLE, INTERROGATION),
        'ext': '{}{}{}'.format(TRIGGER, EXT, INTERROGATION),
        'polar': '{}{}{}{}'.format(TRIGGER, VM_COMPLETE, POLAR, INTERROGATION),
        'w_pulse': '{}{}{}{}'.format(TRIGGER, VM_COMPLETE, POLAR, INTERROGATION),
    }

    DICT_CALC_SET = {
        'func': '{}{}{}{}'.format(CALCULATE, _FUNCTION, SPACE, BRACE),
        'st_stat': '{}{}{}{}{}'.format(CALCULATE, STATISTIC, STATE, SPACE, BRACE),
        'rel_offset': '{}{}{}{}{}'.format(CALCULATE, REL, OFFSET, SPACE, BRACE),
        'rel_stat': '{}{}{}{}{}'.format(CALCULATE, REL, STATE, SPACE, BRACE),
        'db_ref': '{}{}{}{}{}'.format(CALCULATE, DB, REFERENCE, SPACE, BRACE),
        'db_stat': '{}{}{}{}{}'.format(CALCULATE, DB, STATE, SPACE, BRACE),
        'dbm_ref': '{}{}{}{}{}'.format(CALCULATE, DBM, REFERENCE, SPACE, BRACE),
        'dbm_stat': '{}{}{}{}{}'.format(CALCULATE, DBM, STATE, SPACE, BRACE),
        'pf_low': '{}{}{}{}{}'.format(CALCULATE, PF, LOWER, SPACE, BRACE),
        'pf_up': '{}{}{}{}{}'.format(CALCULATE, PF, UPPER, SPACE, BRACE),
        'pf_stat': '{}{}{}{}{}'.format(CALCULATE, PF, STATE, SPACE, BRACE),
    }

    DICT_CALC_GET = {
        'func': '{}{}{}'.format(CALCULATE, _FUNCTION, INTERROGATION),
        'st_min': '{}{}{}{}'.format(CALCULATE, STATISTIC, MIN, INTERROGATION),
        'st_max': '{}{}{}{}'.format(CALCULATE, STATISTIC, MAX, INTERROGATION),
        'st_avg': '{}{}{}{}'.format(CALCULATE, STATISTIC, AVERAGE, INTERROGATION),
        'st_count': '{}{}{}{}'.format(CALCULATE, STATISTIC, COUNT, INTERROGATION),
        'st_stat': '{}{}{}{}'.format(CALCULATE, STATISTIC, STATE, INTERROGATION),
        # 'rel_value': '{}{}{}{}'.format(CALCULATE, _STAT, _COUN, INTERROGATION),
        'rel_offset': '{}{}{}{}'.format(CALCULATE, REL, OFFSET, INTERROGATION),
        'rel_stat': '{}{}{}{}'.format(CALCULATE, REL, STATE, INTERROGATION),
        'db_value': '{}{}{}'.format(CALCULATE, DB, INTERROGATION),
        'db_ref': '{}{}{}{}'.format(CALCULATE, DB, REFERENCE, INTERROGATION),
        'db_stat': '{}{}{}{}'.format(CALCULATE, DB, STATE, INTERROGATION),
        'dbm_value': '{}{}{}'.format(CALCULATE, DBM, INTERROGATION),
        'dbm_ref': '{}{}{}{}'.format(CALCULATE, DBM, REFERENCE, INTERROGATION),
        'dbm_stat': '{}{}{}{}'.format(CALCULATE, DBM, STATE, INTERROGATION),
        'pf_value': '{}{}{}'.format(CALCULATE, PF, INTERROGATION),
        'pf_low': '{}{}{}{}'.format(CALCULATE, PF, LOWER, INTERROGATION),
        'pf_up': '{}{}{}{}'.format(CALCULATE, PF, UPPER, INTERROGATION),
        'pf_stat': '{}{}{}{}'.format(CALCULATE, PF, STATE, INTERROGATION),
    }


