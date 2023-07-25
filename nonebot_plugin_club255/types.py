from typing import TypeVar, Union, Tuple, Set

from pydantic import AnyHttpUrl
from typing_extensions import Literal, get_args

AccessEventName = Literal['on_live', 'notice', 'nice_post', 'post']

T = TypeVar("T")

CMD = Union[str, Tuple[str, ...], Set[Union[str, Tuple[str, ...]]]]

Week = Literal["week", "周"]
Month = Literal["month", "月"]
WeekOrMonth = Literal["week", "month", "周", "月"]

Theme = Literal["white", "dark", "2022", "2023"]

UID = TypeVar('UID', int, str)  # 用户id
PID = TypeVar('PID', int, str)  # 帖子id
FID = TypeVar('FID', int, str)  # 楼层id
MID = TypeVar('MID', int, str)  # 消息id

URL = TypeVar('URL', str, AnyHttpUrl)

week = get_args(Week)
month = get_args(Month)
week_or_month = get_args(WeekOrMonth)
themes = get_args(Theme)

__all__ = [
    "T", "UID", "PID", "FID", "MID", "URL", "CMD", "AccessEventName", "AnyHttpUrl", "Week",
    "Month", "WeekOrMonth", "week", "month", "week_or_month", "themes", "Theme"
]
