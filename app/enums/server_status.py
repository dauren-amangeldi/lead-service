from enum import IntEnum


class ServerStatusEnum(IntEnum):
    ACTIVE = 1
    NOTACTIVE = 2
    LAZY_SEND_DELAY_SECONDS_DEFAULT = 300

    @classmethod
    def get_values(cls) -> list[int]:
        return [status.value for status in cls]

    @classmethod
    def get_names(cls) -> list[str]:
        return [status.name for status in cls]