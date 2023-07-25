from itertools import product
from typing import Union, Set

from nonebot_plugin_club255.types import CMD
from ..config import config, raw_config


def link_cmd(cmdl: Union[str, Set[str]], cmdr: Union[str, Set[str]]):
    """
    link_cmd(["week","month","周","月"],["rank","排名"])
    {'month rank',
     'month.rank',
     'month_rank',
     'rank month',
     'rank week',
     'rank.month',
     'rank.week',
     'rank_month',
     'rank_week',
     'week rank',
     'week.rank',
     'week_rank',
     '周排名',
     '月排名'}
    """

    cmdl = {cmdl} if isinstance(cmdl, str) else set(cmdl)
    cmdr = {cmdr} if isinstance(cmdr, str) else set(cmdr)
    sep = set(raw_config.command_sep)
    sep.add("_")
    sep.add(" ")
    cmd = set()

    for cl, s, cr in product(cmdl, sep, cmdr):
        # 简单判断是否为英文
        if cl.isascii() and cr.isascii():
            cmd.add(cl + s + cr)
            cmd.add(cr + s + cl)
        else:
            if not cl.isascii() and not cr.isascii():
                cmd.add(cl + cr)
    return cmd


def add_prefix(cmd: CMD) -> CMD:
    if not config.club255_prefix:
        return cmd
    prefix = (config.club255_prefix,)
    if isinstance(cmd, str):
        return prefix + (cmd,)
    elif isinstance(cmd, tuple):
        return prefix + cmd
    # elif isinstance(cmd, set):
    else:
        return {prefix + (i,) if isinstance(i, str) else prefix + i for i in cmd}


__all__ = ["link_cmd", "add_prefix"]
