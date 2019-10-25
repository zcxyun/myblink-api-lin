from enum import Enum


class GenderEnum(Enum):
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2


class MemberActive(Enum):
    INACTIVE = 0
    ACTIVE = 1


class ClassicType(Enum):
    MOVIE = 100
    MUSIC = 200
    EPISODE = 300


class IsClassic(Enum):
    YES = 1
    NO = 0
