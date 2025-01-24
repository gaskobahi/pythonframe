from enum import Enum

class AbilitySubjectEnum(str, Enum):
    all = "all"
    User = "User"
    Role = "Role"
    AuthUser = "AuthUser"
    

class AbilityActionEnum(str, Enum):
    admin = "admin"
    manage = "manage"
    read = "read"
    create = "create"
    edit = "edit"
    delete = "delete"
    stream = "stream"