# -*- encoding utf-8 -*-
"""
@File     const.py
@Time     2020/7/31 1207
@Author   blockish
@Email    blockish@yeah.net
"""

EMPTY = ''
SPACE = ' '
INTERROGATION = '?'

SEMICOLON = ';'
COLON = ':'


class Ieee488Const:

    # 校准命令
    CAL = '*CAL'

    # 清除状态寄存器
    CLS = '*CLS'

    """
        该命令编辑标准事件状态使能寄存器（Standard  Event  Status  Enable  register）
        位。该程序决定标准事件状态寄存器(见*ESR?)的哪个事件被允许去设定状态字
        节（Status Byte register）寄存器的ESB (Event Summary Bit)。哪位是1就触
        发哪位相应事件。标准事件状态寄存器的所有使能的事件逻辑OR，从而设定状
        态字节寄存器的ESB（Event Summary Bit )。见“编辑状态寄存器”中对标准事件
        状态寄存器的描述。 
        查询读取标准事件状态使能(Standard Event Status Enable)寄存器。 
        命令语法 
            *ESE <NRf> 
        参数 
            0 to 255 
    """
    ESE = '*ESE{}{}'

    # 查询读取标准状态寄存器并清除它
    ESR = '*ESR?'

    # 获取仪器型号序列号等信息
    IDN = '*IDN?'

    """
        当负载完成所有未完成操作时，该命令使接口设定标准事件状态寄存器的OPC
        位 (第0位)。（参考*ESE 去配置标准事件状态寄存器的位）。下列情况存在时，
        未完成操作完成： 
          在*OPC执行前，所有命令（包括重叠命令）都发出。大多数命令是串行的，
        在下一命令执行前完成。重叠命令和其他命令并行执行。影响触发的命令与
        后面命令重叠发往电子负载。*OPC提供所有重叠命令完成的通知。 
          所有触发动作完成，触发系统返回闲置状态。 
        *OPC不阻止后面命令的处理，但是在所有未完成操作完成前，位0不被设置。
        当所有未完成操作完成时，该查询使接口输出ASCII“1”。 

        命令语法 
            *OPC 
        参数 
            None 
        查询语法 
            *OPC? 
        返回参数 
            <NR1> 该命令用来查询命令执行完毕与否。
    """
    OPC = '*OPC{}'

    OPT = '*OPT'

    """
        该命令用来控制当负载重上电时是否会产生一个服务请求。 
        1 or ON：当负载上电时，状态位元组使能寄存器，操作事件使能寄存器，查 
        询事件使能寄存器及标准事件使能寄存器的值被清零。 
        0 or OFF：状态位元组使能寄存器，操作事件使能寄存器，查询事件使能寄存 
        器及标准事件使能寄存器的值被储存在非易失性存储器中，供重上电时取出使用。 
    """
    PSC = '*PSC{}{}'

    """
        该命令调用用*SAV命令储存的状态。
        CAL:STATe设为OFF， 
        一个隐含的ABORt命令将触发系统设为闲置状态（这将取消任何未完成的触发动作）。 
        注意：储存在地址0的设备状态在机器上电时自动调用。 
        命令语法 
            *RCL <NRf> 
        参数 
            0 - 9 
    """
    RCL = '*RCL {}'

    """
        这条命令复位负载到工厂设定状态。
    """
    RST = '*RST'

    """
        该命令将负载当前状态存储到一个特定位置。最多可存储100种状态。 
        如果上电时要求一个特定状态，该状态需存储在位置0。如果上电状态设为RCL0，
        则在上电时负载就调用它。用*RCL检索仪器状态。
        命令语法 
            *SAV <NRf>
        参数 
            0 - 99 
    """
    SAV = '*SAV {}'

    """
        该命令设定服务请求使能寄存器。该寄存器决定允许状态字节寄存器的哪一位去
        设定Master Status Summary (MSS)位和Request for Service (RQS)总览位。服
        务请求使能寄存器的任何位是1就会使相应的状态字节寄存器位和所有这些使能
        的位逻辑OR，从而设定Status Byte Register的第6位。 
        当控制器执行一个响应SRQ的串行轮询，RQS位会被清除，但是MSS位不会。
        当*SRE被清除（将它设为0），负载不会向电脑发送一个SRQ。查询返回*SRE
        的电流状态。
        命令语法 
                *SRE <NRf> 
        参数 
            0 - 255 
        查询语法 
            *SRE? 
        返回参数 
            <NR1> (register binary value) 
    """
    SRE = '*SRE{}{}'

    """
        该查询读取状态字节寄存器（Status Byte register），该寄存器包含状态总览位和
        Output Queue MAV 位。 读Status Byte寄存器的同时不会清除它。当读取事件
        寄存器时，清除输入总览位（见“编辑状态寄存器”那章获取更多信息）。 一个串
        行轮询返回状态字节寄存器的值，第 6位返回Request  for  Service  (RQS)，而
        不是Master Status Summary (MSS)。 一个串行轮询清除RQS，而不是MSS。
        当MSS设定，它表示负载对请求服务有一个或多个响应。
        返回参数 
            <NR1> (register value) 
    """
    STB = '*STB?'

    TRG = '*TRG'

    """
        该查询使负载做一个自检并报告错误。返回值的参考信息如下： 
        0：表示无错误 
        1：表示模组初始化失败 
        3：表示模组标定数据丢失 
        4或5：表示EEPROM出错 
    """
    TST = '*TST?'

    WAI = '*WAI'


# class Scpi:
#
#     SOUR = 'SOUR'
#     SYST = 'SYST'
#     CONF = 'CONF'
#     OUTP = 'OUTP'
#     DISP = 'DISP'
#     ACQ = 'ACQ'
#     ALI = 'ALI'
#     AUTOS = 'AUTOS'
#     CH = 'CH{}'
#     CONFIG = 'CONFIG'
#     CURS = 'CURS'
#     DATE = 'DATE'
#     TIME = 'TIME'
#     HOR = 'HOR'
#     LIST = 'LIST'
#     TRIG = 'TRIG'
#     SWE = 'SWE'
#     VOLT = 'VOLT'
#     CURR = 'CURR'
#     POW = 'POW'
#     FREQ = 'FREQ'
#     PROT = 'PROT'
#     RANG = 'RANG'
#     LEV = 'LEV'
#     RES = 'RES'
#     IMM = 'IMM'
#     AMPL = 'AMPL'
#     INP = 'INP'
#     SHOR = 'SHOR'
#     AUTO = 'AUTO'
#     STAT = 'STAT'
#     BOTH = 'BOTH'
#     SLEW = 'SLEW'
#     RISE = 'RISE'
#     FALL = 'FALL'
#     FUNC = 'FUNC'
#     DYN = 'DYN'
#     HIGH = 'HIGH'
#     LOW = 'LOW'
#     MODE = 'MODE'
#     ON = 'ON'
#     OFF = 'OFF'
#     LOC = 'LOC'
#     REM = 'REM'
#     RWL = 'RWL'
#     DWEL = 'DWEL'
#     MIN = 'MIN'
#     MAX = 'MAX'
#     RMS = 'RMS'
#     PEAK = 'PEAK'
#     MOD = 'MOD'
#     PHAS = 'PHAS'
#     STAR = 'STAR'
#     END = 'END'
#     DIMM = 'DIMM'
#     WIND = 'WIND'
#     TEXT = 'TEXT'
#     CLE = 'CLE'
#     RUN = 'RUN'
#     STEP = 'STEP'
#     REP = 'REP'
#     COUN = 'COUN'
#     SAV = 'SAV'
#     BANK = 'BANK'
#     REC = 'REC'
#     SLOP = 'SLOP'
#     UNIT = 'UNIT'
#     SD = 'SD'
#     CONT = 'CONT'
#     SIT = 'SIT'
#
#     FASTA = 'FASTA'
#     PALE = 'PALE'
#     STATE = 'STATE'
#     NUMAC = 'NUMAC'
#     NUMAV = 'NUMAV'
#     NUME = 'NUME'
#     STOPA = 'STOPA'
#     CAT = 'CAT'
#     DEF = 'DEF'
#     ALL = 'ALL'
#     DELE = 'DELE'
#     NAM = 'NAM'
#     ENA = 'ENA'
#     AMPSVIAVOLT = 'AMPSVIAVOLT'
#     FAC = 'FAC'
#     BAN = 'BAN'
#     COUP = 'COUP'
#     DESK = 'DESK'
#     INV = 'INV'
#     LAB = 'LAB'
#     OFFS = 'OFFS'
#     POS = 'POS'
#     SCA = 'SCA'
#     TER = 'TER'
#     YUN = 'YUN'
#     PRO = 'PRO'
#     AUTOZ = 'AUTOZ'
#     CAL = 'CAL'
#     CALIBRATABL = 'CALIBRATABL'
#     COMMAND = 'COMMAND'
#     DEGAU = 'DEGAU'
#     FORCEDR = 'FORCEDR'
#     GAIN = 'GAIN'
#     ID = 'ID'
#     SER = 'SER'
#     TYP = 'TYP'
#     PROPDEL = 'PROPDEL'
#     RECDES = 'RECDES'
#     SIG = 'SIG'
#     UNI = 'UNI'
#     ADVMATH = 'ADVMATH'
#     AFG = 'AFG'
#     ANALO = 'ANALO'
#     BANDW = 'BANDW'
#     GNDCPLG = 'GNDCPLG'
#     MAXSAMPLER = 'MAXSAMPLER'
#     NUMCHAN = 'NUMCHAN'
#     RECLENS = 'RECLENS'
#     VERTINV = 'VERTINV'
#     APPL = 'APPL'
#     CUSTOMM = 'CUSTOMM'
#     LIMITM = 'LIMITM'
#     STANDARDM = 'STANDARDM'
#     VIDPIC = 'VIDPIC'
#     ARB = 'ARB'
#     AUXIN = 'AUXIN'
#     DIGITA = 'DIGITA'
#     MAG = 'MAG'
#     DVM = 'DVM'
#     EXTVIDEO = 'EXTVIDEO'
#     HISTOGRAM = 'HISTOGRAM'
#     NETWORKDRIVES = 'NETWORKDRIVES'
#     NUMMEAS = 'NUMMEAS'
#     REFS = 'REFS'
#     NUMREFS = 'NUMREFS'
#     RF = 'RF'
#     ADVTRIG = 'ADVTRIG'
#     ROSC = 'ROSC'
#     DDT = 'DDT'
#     HBA = 'HBA'
#     DELT = 'DELT'
#     POSITION = 'POSITION'
#     USE = 'USE'
#     SOU = 'SOU'
#     VBA = 'VBA'
#     ALTERNATE = 'ALTERNATE'
#     HPOS = 'HPOS'
#     VDELT = 'VDELT'
#     XY = 'XY'
#     POL = 'POL'
#     RADIUS = 'RADIUS'
#     THETA = 'THETA'
#     PRODUCT = 'PRODUCT'
#     RATIO = 'RATIO'
#     READOUT = 'READOUT'
#     RECT = 'RECT'
#     X = 'X'
#     Y = 'Y'
#     DEL = 'DEL'
#     TIM = 'TIM'
#     RECO = 'RECO'
#     SAMPLER = 'SAMPLER'
#     MAXS = 'MAXS'
#
#     FUNC2 = 'FUNC2'
#     DC = 'DC'
#     AC = 'AC'
#     FRES = 'FRES'
#     PER = 'PER'
#     DIOD = 'DIOD'
#     CAP = 'CAP'
#     MEAS = 'MEAS'
#     IMPE = 'IMPE'
#     FILT = 'FILT'
#     RATE = 'RATE'
#     SENS = 'SENS'
#     INTE = 'INTE'
#     HOLD = 'HOLD'
#     SING = 'SING'
#     EXT = 'EXT'
#     VMC = 'VMC'
#     POLA = 'POLA'
#     PULS = 'PULS'
#     CALC = 'CALC'
#     REFE = 'REFE'
#     DB = 'DB'
#     DBM = 'DBM'
#     REL = 'REL'
#     PF = 'PF'
#     LOWE = 'LOWE'
#     UPPE = 'UPPE'
#     AVER = 'AVER'
#
#     COMM = 'COMM'
#     HEAD = 'HEAD'
#     LOCK = 'LOCK'
#     VERB = 'VERB'
#     WAIT = 'WAIT'
#     HARM = 'HARM'
#     NORM = 'NORM'
#     ITEM = 'ITEM'
#     PLLS = 'PLLS'
#     ORD = 'ORD'
#     THD = 'THD'
#     INTEG = 'INTEG'
#     STOP = 'STOP'
#     TYPE = 'TYPE'
#     MHOL = 'MHOL'
#     SYNC = 'SYNC'
#     NUM = 'NUM'
#     VAL = 'VAL'
#     PAN = 'PAN'
#     EESE = 'EESE'
#     QEN = 'QEN'
#     QMES = 'QMES'
#     COND = 'COND'
#     ERR = 'ERR'
#     EESR = 'EESR'
#     SPOL = 'SPOL'
#     STOR = 'STOR'
#     INT = 'INT'
#     KLOC = 'KLOC'
#     SUFF = 'SUFF'
#     VER = 'VER'
#     FIRM = 'FIRM'
#     POJ = 'POJ'
#     EXTS = 'EXTS'
#     SRAT = 'SRAT'
#     ELEM = 'ELEM'
#     SCAL = 'SCAL'
#     VT = 'VT'
#     CT = 'CT'
#     SFAC = 'SFAC'
#     LINE = 'LINE'
#     CFAC = 'CFAC'
#     WIR = 'WIR'
#     RCON = 'RCON'
#     POV = 'POV'
#     CRAN = 'CRAN'
#     PRES = 'PRES'
#     FORM = 'FORM'
#     SELSEL = 'SEL'


