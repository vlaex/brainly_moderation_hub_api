from typing_extensions import TypedDict
from pydantic import BaseModel
from core.enums import Gender


class BrainlyGQLUserRank(TypedDict):
    id: str
    name: str


class BrainlyGQLUserAvatar(TypedDict):
    url: str


class BrainlyGQLUserThanks(TypedDict):
    count: int


class BrainlyGQLUser(BaseModel):
    id: str
    nick: str
    created: str
    rank: BrainlyGQLUserRank
    specialRanks: list[BrainlyGQLUserRank]
    points: int
    gender: Gender
    avatar: BrainlyGQLUserAvatar
    helpedUsersCount: int
    thanks: BrainlyGQLUserThanks
