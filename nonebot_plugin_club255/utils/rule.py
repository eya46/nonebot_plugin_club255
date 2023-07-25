# link https://github.com/iyume/nonebot-plugin-params/blob/main/nonebot_plugin_params/rule.py

from nonebot import Bot, logger
from nonebot.internal.adapter import Event
from nonebot.internal.rule import Rule


async def _is_private_message(
        event: Event, bot: Bot
) -> bool:
    try:
        # 没有message当然不是私聊消息
        event.get_message()
    except:
        return False
    adapter_name = bot.adapter.get_name()

    if adapter_name == "OneBot V11":
        return True if getattr(event, "message_type", None) == "private" else False
    elif adapter_name == "Kaiheila":
        return True if getattr(event, "message_type", None) == "private" else False
    elif adapter_name in ["OneBot V12", "Walle-Q"]:
        return True if getattr(event, "detail_type", None) == "private" else False
    elif adapter_name == "Feishu":
        return True if getattr(event, "chat_type", None) == "p2p" else False
    elif adapter_name == "Telegram":
        return True if getattr(event, "get_event_name", lambda: None)() == "message.private" else False
    elif adapter_name == "QQ Guild":
        return True if getattr(event, "__type__", None) == "DIRECT_MESSAGE_CREATE" else False
    elif adapter_name == "mirai2":
        session = getattr(event, "get_session_id", lambda: "")()
        # 好友、其它客户端、陌生人
        return any(i in session for i in ["friend", "other_", "stranger_"])
    elif adapter_name == "Console":
        return True
    elif adapter_name == "GitHub":
        # github哪有私聊😡
        # private库里面的issue和pull算吗???
        return False
    elif adapter_name == "ntchat":
        return not bool(getattr(event, "room_wxid", None))
    elif adapter_name == "Minecraft":
        # 翻了下，好像都是公屏聊天，一律False
        return False
    elif adapter_name == "BilibiliLive":
        return False
    elif adapter_name == "大别野":
        return False
    elif adapter_name == "Club255":
        logger.warning("Club255 adapter is not supported yet.")
        return False
    return False


MustPrivate: Rule = Rule(_is_private_message)
