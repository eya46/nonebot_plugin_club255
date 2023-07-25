from ..client.models import SignResult
from ..utils.depends import ClubUserGet, ClubApiGet
from ..config import config
from ..matcher import club255

sign = club255.on_command(config.club255_cmd_sign)


@sign.handle()
async def sign_handle(club_user: ClubUserGet, api: ClubApiGet):
    if club_user is None:
        await sign.finish("签到失败 -> 请先私聊绑定账号", at=True)
    if api is None:
        await sign.finish("签到失败 -> 账号密码错误或token过期", at=True)

    try:
        res = await api.sign_now()
    except Exception as e:
        await sign.finish(f"签到失败 -> {e}", at=True)
        raise e
    mod = SignResult.from_data(res)
    await sign.finish(
        f"{mod.msg} -> 获取经验:{mod.exp}"
        , at=True
    )
