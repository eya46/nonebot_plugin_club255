from functools import wraps

from nonebot.exception import FinishedException
from nonebot.internal.matcher import current_matcher, current_bot
from nonebot_plugin_saa import MessageFactory
from typing_extensions import NoReturn

from ..config import config
from ..types import T


async def send(msg: MessageFactory, at: bool = False, reply: bool = False):
    _raw_msg = msg
    if not isinstance(msg, MessageFactory):
        msg = MessageFactory(msg)
    try:
        await msg.send(at_sender=at or config.club255_at, reply=reply or config.club255_reply)
    except Exception as e:
        try:
            if (matcher := current_matcher.get()) and (_send := getattr(matcher, "_raw_send", None)) is not None:
                await _send(_raw_msg if isinstance(_raw_msg,str) else str(msg))
        except Exception as e2:
            raise Exception(e, e2)


async def finish(msg: MessageFactory, at: bool = False, reply: bool = False) -> NoReturn:
    _raw_msg = msg
    if not isinstance(msg, MessageFactory):
        msg = MessageFactory(msg)
    try:
        await msg.send(at_sender=at or config.club255_at, reply=reply or config.club255_reply)
    except Exception as e:
        try:
            if (matcher := current_matcher.get()) and (_send := getattr(matcher, "_raw_send", None)) is not None:
                await _send(_raw_msg if isinstance(_raw_msg,str) else str(msg))
        except Exception as e2:
            raise Exception(e, e2)
    raise FinishedException


def fake(cls: T) -> T:
    def wrap(func_name: str):
        setattr(cls, "_raw_" + func_name, getattr(cls, func_name))

        @wraps(getattr(cls, func_name))
        def _(*args, **kwargs):
            matcher = getattr(cls, "_raw_" + func_name)(*args, **kwargs)
            setattr(matcher, "_raw_send", matcher.send)
            setattr(matcher, "_raw_finish", matcher.finish)
            matcher.send = send
            matcher.finish = finish
            return matcher

        setattr(cls, func_name, _)

    for i in dir(cls):
        if i.startswith("on") and callable(getattr(cls, i)):
            wrap(i)
    return cls


__all__ = [
    "fake"
]
