from pathlib import Path

from nonebot import load_plugins, require

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_htmlrender")
require("nonebot_plugin_saa")
require("nonebot_plugin_userinfo")
require("nonebot_plugin_datastore")

load_plugins(str(Path(__file__).parent.joinpath("plugins").resolve()))

# @scheduler.scheduled_job("interval", minutes=push_minutes, timezone='Asia/Shanghai')
# async def auto_255_post():
#     # 当没有要推送的
#     if (len(friends_push_list) + len(groups_push_list)) == 0:
#         return
#
#     # 获取帖子
#     list_255 = await get_255_list()
#
#     # 获取bot
#     if push_bot != 0:
#         bot: Bot = get_bot(str(push_bot))
#     else:
#         bot: Bot = get_bot()
#
#     if bot is None:
#         logger.error("255新帖，推送失败:没有已连接的机器人！")
#         return
#
#     msgs: List[Union[Message, dict]] = []
#
#     if isinstance(list_255, str):
#         msgs.append(Message(list_255))
#     else:
#         logger.debug(f"255新帖，此次获取: {len(list_255)} 个帖子")
#         for i in list_255:
#             i: Dict
#             user: Dict = i.get("author", {})
#             msg = Message()
#             msg.append(MessageSegment.text("毛怪俱乐部新帖:\n"))
#             if user.get("avatar") is not None and if_show_avatar:
#                 msg.append(MessageSegment.image(file=user.get("avatar")))
#             msg.append(MessageSegment.text(
#                 f"昵称:{user.get('nickname')}\n"
#                 f"UID:{user.get('uid')}\n"
#                 f"经验:{user.get('exp')}\n\n"
#                 f"标题:{i.get('title')}\n\n" +
#                 f"{i.get('content')[:100]}...\n\n".replace("&nbsp;", " ") +  # 最多显示100字文本
#                 f"URL:\n{url}postDetails/{i.get('id')}"
#             ))
#             # 显示帖子图片。不想显示图片请注释下面两行
#             for j in i.get("pictures", [])[:picture_max]:
#                 msg.append(MessageSegment.image(file=j))
#             msgs.append(msg)
#
#     merge_msgs = merge_msg(msgs, bot.self_id)
#
#     for g in groups_push_list:
#         if if_merge_msg and len(msgs) > merge_msg_num:
#             await bot.call_api("send_group_forward_msg", group_id=int(g), messages=merge_msgs)
#         else:
#             for m in msgs:
#                 logger.debug(f"255新帖，开始推送群聊:{g}")
#                 try:
#                     await bot.call_api("send_group_forward_msg", group_id=int(g), message=m)
#                 except Exception as e:
#                     if isinstance(e, ValueError):
#                         logger.error(f"255新帖，推送失败:群号错误 -> {g}")
#                     else:
#                         logger.error(f"255新帖，推送失败:群号 -> {g},未知错误 -> {e}")
#
#     for m in msgs:
#         for f in friends_push_list:
#             logger.debug(f"255新帖，开始推送QQ:{f}")
#             try:
#                 await bot.send_private_msg(user_id=int(f), message=m)
#             except Exception as e:
#                 if isinstance(e, ValueError):
#                     logger.error(f"255新帖，推送失败:QQ号错误 -> {f}")
#                 else:
#                     logger.error(f"255新帖，推送失败:QQ -> {f},未知错误 -> {e}")
#     return len(msgs)
#
#
# if __name__ == '__main__':
#     pass
