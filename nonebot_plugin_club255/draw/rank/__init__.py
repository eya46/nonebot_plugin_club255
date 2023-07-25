from typing import List, Optional

from nonebot_plugin_htmlrender import html_to_pic

from ..api import render_template
from ...client.models import Rank
from ...types import WeekOrMonth, week


async def draw(ranks: List[Rank], *, rank_type: WeekOrMonth, page: int) -> Optional[bytes]:
    return await html_to_pic(
        await render_template("rank", ranks=ranks, page=page, if_week=rank_type in week)
        , wait=0, device_scale_factor=1.5, viewport={
            "width": 400,
            "height": 700
        }
    )
