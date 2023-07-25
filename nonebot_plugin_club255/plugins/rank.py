from nonebot_plugin_saa import Image

from ..client.models import Rank
from ..config import config
from ..utils.depends import ClubApiHeadlessGet, CommandGet, CommandArgGet
from ..draw.rank import draw
from ..types import week, month
from ..utils.cmd import link_cmd
from ..matcher import club255

_rank_week_cmd = link_cmd(week, config.club255_cmd_rank)
_rank_month_cmd = link_cmd(month, config.club255_cmd_rank)

rank = club255.on_command(config.club255_cmd_rank)
rank_week = club255.on_command(_rank_week_cmd)
rank_month = club255.on_command(_rank_month_cmd)


@rank.handle()
@rank_week.handle()
@rank_month.handle()
async def rank_handle(api: ClubApiHeadlessGet, cmd: CommandGet, arg: CommandArgGet):
    arg = arg.extract_plain_text()
    # 获取页数
    if arg.isdigit():
        arg = int(arg)
    else:
        arg = 1

    if any([i in cmd for i in week]):
        ranks = Rank.from_data(await api.get_week_rank(arg), page=arg)
    elif any([i in cmd for i in month]):
        ranks = Rank.from_data(await api.get_month_rank(arg), page=arg)
    else:
        if config.club255_rank_define in month:
            ranks = Rank.from_data(await api.get_month_rank(arg), page=arg)
        else:
            ranks = Rank.from_data(await api.get_week_rank(arg), page=arg)
    await rank.finish(Image(await draw(
        ranks, rank_type=cmd, page=arg
    )))
