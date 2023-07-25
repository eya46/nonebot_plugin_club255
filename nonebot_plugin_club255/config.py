from typing import Set, Optional

from nonebot import get_driver
from pydantic import BaseModel, Extra, Field, root_validator

from nonebot_plugin_club255.types import WeekOrMonth, Theme


class Config(BaseModel, extra=Extra.ignore):
    club255_theme: Theme = Field(default="2023")

    club255_at: bool = Field(default=False)
    club255_reply: bool = Field(default=False)

    club255_ua: str = Field(default=(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    ))

    club255_cmd_sign: Set[str] = Field(default={"sign", "签到"})
    club255_cmd_rank: Set[str] = Field(default={"rank", "排行榜", "排名", "贡献榜"})
    club255_cmd_bind: Set[str] = Field(default={"bind", "绑定"})

    club255_rank_define: WeekOrMonth = Field(default="week")

    club255_rank_size: int = Field(default=10)
    club255_post_size: int = Field(default=10)

    club255_prefix: str = Field(default="255")
    club255_priority: int = Field(default=5)
    club255_block: bool = Field(default=False)

    club255_test: Optional[float] = 11.45

    @root_validator
    def _check_prefix(cls, value):
        for i in dir(value):
            if i.startswith("club255_cmd_") and len(getattr(value, i)) < 1:
                raise ValueError(f"{i} 长度不能小于1")
        return value


raw_config = get_driver().config
config: Config = Config.parse_obj(raw_config)

__all__ = ["config", "Config", "raw_config"]
