from enum import Enum


class EnvTypeEnum(str, Enum):
    LOCAL = "local"
    TEST = "test"
    RC = "rc"
    PROD = "prod"
