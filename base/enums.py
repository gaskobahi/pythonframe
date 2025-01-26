from enum import Enum

class AbilitySubjectEnum(str, Enum):
    all = "all"


class AbilityActionEnum(str, Enum):
    manage = "manage"
    read = "read"
    create = "create"
    edit = "edit"
    delete = "delete"
    stream = "stream"