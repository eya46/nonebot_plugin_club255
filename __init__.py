from typing import List, Union, Optional, Dict

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot import require, get_driver, logger, get_bot, get_bots
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment

from .tool import get_255_list

scheduler: AsyncIOScheduler = require("nonebot_plugin_apscheduler").scheduler

friends_push_list: List = getattr(get_driver().config, "255_push_friends", [])
groups_push_list: List = getattr(get_driver().config, "255_push_groups", [])
push_minutes: int = int(getattr(get_driver().config, "255_push_minutes", 10))
push_bot: Union[str, int] = getattr(get_driver().config, "255_push_bot", 0)
# picture_max: int = 0 if (_p_m := int(getattr(get_driver().config, "255_pictures_max", 4))) < 0 else _p_m
picture_max: int = int(getattr(get_driver().config, "255_pictures_max", 4))

url: str = getattr(get_driver().config, "255_url", "")


@scheduler.scheduled_job("interval", minutes=push_minutes, timezone='Asia/Shanghai')
async def auto_255_post():
    # 当没有要推送的
    if (len(friends_push_list) + len(groups_push_list)) == 0:
        return

    # 获取帖子
    list_255 = await get_255_list()

    # 获取bot
    bot: Optional[Bot] = None
    if push_bot != 0:
        bot = get_bot(str(push_bot))
    else:
        bots = get_bots()
        for i in bots.items():
            if isinstance(i[1], Bot):
                bot = i[1]
                break

    if bot is None:
        logger.error("255新帖，推送失败:没有已连接的机器人！")
        return

    msgs: List[Message] = []

    if isinstance(list_255, str):
        msgs.append(Message(list_255))
    else:
        logger.debug(f"255新帖，此次获取: {len(list_255)} 个帖子")
        for i in list_255:
            i: Dict
            user: Dict = i["author"]
            msg = Message()
            msg.append(MessageSegment.text("毛怪俱乐部新帖:\n"))
            # 不显示头像请注释下面两行
            if user.get("avatar") is not None:
                msg.append(MessageSegment.image(file=user.get("avatar")))
            msg.append(MessageSegment.text(
                f"昵称:{user.get('nickname')}\n"
                f"UID:{user.get('uid')}\n"
                f"经验:{user.get('exp')}\n\n"
                f"标题:{i.get('title')}\n\n"
                f"{i.get('content')[:100]}...\n\n"  # 最多显示100字文本
                f"URL:\n{url}postDetails/{i.get('id')}"
            ))
            # 显示帖子图片。不想显示图片请注释下面两行
            for j in i.get("pictures", [])[:picture_max]:
                msg.append(MessageSegment.image(file=j))

    for m in msgs:
        for g in groups_push_list:
            try:
                await bot.send_group_msg(group_id=int(g), message=m)
            except Exception as e:
                if isinstance(e, ValueError):
                    logger.error(f"255新帖，推送失败:群号错误 -> {g}")
                else:
                    logger.error(f"255新帖，推送失败:群号 -> {g},未知错误 -> {e}")

        for f in friends_push_list:
            try:
                await bot.send_private_msg(user_id=int(f), message=m)
            except Exception as e:
                if isinstance(e, ValueError):
                    logger.error(f"255新帖，推送失败:QQ号错误 -> {f}")
                else:
                    logger.error(f"255新帖，推送失败:QQ -> {f},未知错误 -> {e}")


if __name__ == '__main__':
    pass
