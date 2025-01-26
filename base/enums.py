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