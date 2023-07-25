from nonebot import on_command

from ..config import config
from ..matcher import club255
from ..utils.depends import ClubUserGet, IsPrivateMessageGet

# on_command("",permission=)
bind = club255.on_command(config.club255_cmd_bind)



@bind.handle(parameterless=[])
async def bind_handle(club_user: ClubUserGet, is_private: IsPrivateMessageGet):
    if club_user:
        bind.finish("您已绑定账号，如需更换请先解绑")
    await bind.send(
        "请选择绑定方式：\n"
        "1.账号密码(仅限私聊)\n"
        "2.token(仅限私聊)\n"
        "3.弹幕验证\n"
        "other.取消"
    )
    bind.receive()


