from datetime import datetime
from typing import List

from typing_extensions import Self

from pydantic import BaseModel, AnyHttpUrl

from ..config import config
from ..client import model_api


class RawUser(BaseModel):
    uid: int
    nickname: str
    avatar: AnyHttpUrl


class SignResult(BaseModel):
    code: int
    msg: str
    exp: int

    def __str__(self):
        return f"签到结果:{self.msg}\n经验值:{self.exp}"

    @classmethod
    def from_data(cls, data: dict) -> Self:
        return model_api(data, cls)


class Rank(RawUser):
    uid: int
    nickname: str
    avatar: AnyHttpUrl

    rank: int
    # 贡献点
    contribution: int

    @classmethod
    def from_data(cls, data: dict, *, page: int = 1, pageSize: int = 10) -> List[Self]:
        return model_api(
            [{"rank": index + 1 + (page-1)*pageSize, **i}
             for index, i in enumerate(data["list"])], List[cls]
        )


class Tag(BaseModel):
    tagId: int
    tagName: str


class Label(BaseModel):
    labelId: int
    labelName: str
    # "rgb(250,143,34)"
    color: str


class Author(BaseModel):
    uid: int
    nickname: str
    avatar: AnyHttpUrl
    role: int
    status: int
    exp: int
    auth: int
    authentication: str


class Post(BaseModel):
    id: int
    # 标题
    title: str
    # 内容
    content: str
    hanserLike: bool
    hanserReplay: bool
    last_reply_time: datetime
    last_reply_user: int
    post_time: datetime
    likes: int
    replies: int
    readings: int
    type: int
    role: int
    exp: int
    auth: int
    authentication: str
    # 是否点赞
    liked: bool
    # 预览图
    pictures: List[AnyHttpUrl]
    # 原图
    primaryPictures: List[AnyHttpUrl]

    tags: List[Tag]
    labels: List[Label]
    videos: List[AnyHttpUrl]
    author: Author
