import enum


@enum.unique
class EventEnum(enum.StrEnum):
    UNFINISHED = "UNFINISHED"
    FIRST_WIN = "FIRST_WIN"
    SECOND_WIN = "SECOND_WIN"
