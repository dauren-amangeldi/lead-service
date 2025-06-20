from enum import IntEnum


class LeadStatusEnum(IntEnum):
    SEND = 1
    LAZY = 2
    ERROR = 3

    @classmethod
    def get_values(cls) -> list[int]:
        return [status.value for status in cls]

    @classmethod
    def get_names(cls) -> list[str]:
        return [status.name for status in cls] 