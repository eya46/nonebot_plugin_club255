from typing import Tuple, Union, Set

from nonebot import MatcherGroup
from nonebot.internal.matcher import Matcher
from typing_extensions import Type

from .config import config
from .utils.matcher import fake


class Club255(MatcherGroup):
    basecmd: Tuple[str, ...]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_command = self.command
        self.on_shell_command = self.shell_command
        self.basecmd = (config.club255_prefix,)

    def command(
            self,
            cmd: Union[str, Tuple[str, ...]], **kwargs
    ) -> Type[Matcher]:
        if isinstance(cmd, set):
            _ = set(cmd)
            cmd = _.pop()
            kwargs["aliases"] = _
        if isinstance(cmd, str):
            cmd = (cmd,)
        cmd = self.basecmd + cmd
        if aliases := kwargs.get("aliases"):
            kwargs["aliases"] = {
                self.basecmd + ((alias,) if isinstance(alias, str) else alias)
                for alias in aliases
            }
        return super().on_command(cmd, **kwargs)

    def shell_command(
            self,
            cmd: Union[str, Tuple[str, ...], Set[str]], **kwargs
    ) -> Type[Matcher]:
        if isinstance(cmd, set):
            _ = set(cmd)
            cmd = _.pop()
            kwargs["aliases"] = _
        if isinstance(cmd, str):
            cmd = (cmd,)
        cmd = self.basecmd + cmd
        if aliases := kwargs.get("aliases"):
            kwargs["aliases"] = {
                self.basecmd + ((alias,) if isinstance(alias, str) else alias)
                for alias in aliases
            }
        return super().on_command(cmd, **kwargs)


club255 = fake(Club255(priority=config.club255_priority, block=config.club255_block))

__all__ = ["club255"]
