import os
import uuid
from typing import Union, List, Dict, Any

from httpx import AsyncClient, Cookies
from nonebot import logger, get_driver

# 255账号
from nonebot.adapters.onebot.v11 import Message

_config = get_driver().config

account_255: str = getattr(_config, "255_account", "")
# 255密码
password_255: str = getattr(_config, "255_password", "")
# 255的网址，https://???????.com/
# url: str = getattr(_config, "255_url", "")
url: str = "https://2550505.com/"
# 单次最大获取的帖子数, 限制小于25
tid_max_num = min(int(getattr(_config, "255_tid_max_num", 10)), 25)

User_Agent = "255_push bot" + f" account:{account_255}" if account_255 != "" else ""

local = os.path.dirname(__file__)


def merge_msg(
        msg_list: List[Union[str, Message]], uin: Union[int, str], name: str = "俱乐部ID:" + account_255
) -> List[dict]:
    """
    说明:
        生成自定义合并消息 （抄自真寻）
    参数:
        :param msg_list: 消息列表
        :param uin: 发送者 QQ
        :param name: 自定义名称
    """
    uin = int(uin)
    mes_list = []
    for _message in msg_list:
        data = {
            "type": "node",
            "data": {
                "name": name,
                "uin": f"{uin}",
                "content": _message if isinstance(_message, str) else str(_message),
            },
        }
        mes_list.append(data)
    return mes_list


def _cookie_to_str(cookie: Union[Cookies]):
    if isinstance(cookie, Cookies):
        return "; ".join([f'{i}={cookie[i]}' for i in cookie])


# 获取当前目录下的文件地址
def get_file_path(name: str) -> str:
    return os.path.join(local, name)


# 获取最新的帖子id
def get_last_id() -> int:
    with open(get_file_path('new.txt'), 'r') as f:
        return int(_id if (_id := f.read().strip()) != "" else 0)


# 设置最新的帖子id
def set_last_id(_id):
    with open(get_file_path('new.txt'), 'w') as f:
        return f.write(str(_id))


# 获取255 cookie
async def get_cookie(_cookie=None):
    if _cookie is None:
        try:
            with open(get_file_path("cookie.txt"), 'r') as f:
                _cookie = f.read().strip()
        except Exception as e:
            _cookie = ""
    if account_255 == "" or password_255 == "":
        return None
    try:
        async with AsyncClient() as r:
            r: AsyncClient
            _info = await r.get(f"{url}user/info",
                                headers={"Cookie": _cookie, "User-Agent": User_Agent})
            if _info.json()["code"] == 0:
                return _cookie
            _res = await r.post(
                f"{url}auth/login",
                headers={"User-Agent": User_Agent},
                json={"account": account_255, "password": password_255}
            )
            if _res.status_code != 200:
                return None
            if _res.json()["code"] != 0:
                return None
            _token = _cookie_to_str(r.cookies)
            with open(get_file_path("cookie.txt"), 'w') as f:
                f.write(_token)
            return _token
    except Exception as e:
        logger.error(e)
        raise e


async def sign_255(cookie: str = None) -> Dict[str, Any]:
    if cookie is None:
        cookie = await get_cookie()
    async with AsyncClient() as r:
        r: AsyncClient
        web = await r.get(
            f"{url}sign",
            headers={
                "Cookie": cookie,
                "User-Agent": User_Agent,
                "authorization": str(uuid.uuid1())
            }
        )
        return web.json()


async def sign_255_str(cookie: str = None) -> str:
    if cookie is None:
        cookie = await get_cookie()
    try:
        _res = await sign_255(cookie)
    except Exception as e:
        return f"255签到报错:\n{e}"
    try:
        return f'结果:{_res["code"]}\n经验:{_res["exp"]}\n信息:{_res["msg"]}'
    except Exception as e:
        return f"结果解析失败-{e.__class__}:\n{e}\n{_res}"


# 获取帖子
async def get_255_list() -> Union[List, str]:
    if url == "":
        return []
    async with AsyncClient() as r:
        r: AsyncClient
        web = await r.get(
            f'{url}post/list/brief?page=1&pageSize={tid_max_num}',
            headers={"User-Agent": User_Agent}
        )
        if web.status_code != 200:
            logger.error("255帖子获取失败")
            return f"255帖子连接失败,status_code:{web.status_code}"
        _res = web.json()
        if _res["code"] != 0:
            return f"255帖子获取失败,code:{_res['code']}"
        last_id = get_last_id()
        last_id_new = last_id
        list_255 = []
        # 是否是第一次使用
        first_time = (last_id == 0)
        for i in _res["result"]:
            if i.get("id", 0) <= last_id:
                continue
            else:
                if i.get("id", 0) > last_id_new:
                    last_id_new = i.get("id", 0)
                    set_last_id(last_id_new)
                list_255.append(i)
        # 如果是第一次用这个插件，就先不推送
        return list_255[::-1] if not first_time else []


if __name__ == '__main__':
    import asyncio

    # print(asyncio.get_event_loop().run_until_complete(
    #     get_cookie()
    # ))
    print(get_last_id())
