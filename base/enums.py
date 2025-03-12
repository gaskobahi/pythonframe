from enum import Enum

class AbilitySubjectEnum(str, Enum):
    Role="Role"
    all = "all"


class AbilityActionEnum(str, Enum):
    manage = "manage"
    read = "read"
    create = "create"
    edit = "edit"
    delete = "delete"
    stream = "stream"

class ArticleEnum(str, Enum):
    RCN = "RCN"
    CRCN = "CRCN"
    BCK_PW = "BCK-PW"
    CKG = "CKG"
    BCK = "BCK"
    CKFG = "CKFG"


class CKFGVariantEnum(str, Enum):
    BB1="BB1",
    BB2="BB2",
    CH="CH",
    CH2="CH2",
    CW="CW",
    CW240="CW240",
    CW320="CW320",
    CW450="CW450",
    DW="DW",
    FB_WB="FB/WB",
    FS="FS",
    LWP="LWP",
    MEAL="MEAL",
    PKW="PKW",
    PKW1="PKW1",
    PKW2="PKW2",
    POWDER="POWDER",
    POWDER2="POWDER2",
    SB="SB",
    SP="SP",
    SS="SS",
    SSW="SSW",
    SSW320="SSW320",
    SSW360="SSW360",
    SW210="SW210",
    SW240="SW240",
    SW320="SW320",
    SW360="SW360",
    SW450="SW450",
    TBP="TBP",
    WB="WB",
    WS="WS",
    WSP="WSP",
    WSP2="WSP2",
    WW180="WW180",
    WW210="WW210",
    WW240="WW240",
    WW320="WW320",
    WW450="WW450"

class BCKVariantEnum(str, Enum):
    BCKW_M="BCKW-M",
    BCKW_A="BCKW-A",
    BCKW_B="BCKW-B",
    BCKW_C="BCKW-C",
    BCKW_D="BCKW-D",

class CRCNVariantEnum(str, Enum):
    E="18 E",
    D="18-20 D",
    C="20-22 C",
    B="22-24 B",
    A="24 A",


