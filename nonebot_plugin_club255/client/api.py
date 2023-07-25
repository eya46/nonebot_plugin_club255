from typing import Optional, List, Union, Tuple, Callable, Any, Type
from httpx import AsyncClient, Response
from urllib.parse import urljoin
import json

from nonebot import logger
from pydantic import parse_obj_as

from ..types import PID, UID, T
from ..config import config
from .client import HeadlessClient


class HeadlessApi:
    def __init__(self, client: HeadlessClient):
        self.client = client
        self.get = self.client.get
        self.post = self.client.post

    async def get(self, api: str, **kwargs) -> Response:
        return await self.client.get(api, params=kwargs)

    async def post(self, api: str, **kwargs) -> Response:
        return await self.client.post(api, json=kwargs)

    async def get_version(self) -> dict:
        """
        获取版本信息
        :return: {android,ios,description,version}
        """
        return (await self.get("get_version")).json()

    async def get_week_rank(self, page: int = 1, pageSize: int = 10) -> dict:
        return (await self.get(
            f"contribution/rank?page={page}&pageSize={pageSize}&sort=week",
        )).json()

    async def get_month_rank(self, page: int = 1, pageSize: int = 10) -> dict:
        return (await self.get(
            f"contribution/rank?page={page}&pageSize={pageSize}&sort=month"
        )).json()


class Api(HeadlessApi):
    async def get_self_uid(self) -> int:
        """
        获取自己的uid
        :return: uid
        """
        return (await self.get_self_info())["query"]["uid"]

    async def get_user_info(self, uid: UID) -> dict:
        """
        获取用户信息
        :param uid: 用户uid
        :return: {code,query:{
            uid,nickname,avatar,role,status,exp,contribution,sign,auth,authentication,location,isp,sex,birthday
        }}
        """
        return (await self.get("user/user-query", uid=uid)).json()

    async def get_self_info(self) -> dict:
        """
        获取自己的信息
        :return: {code,query:{
            uid,nickname,avatar,role,status,exp,contribution,sign,auth,authentication,location,isp,sex,birthday
        }}
        """
        return (await self.get("user/query")).json()

    async def get_token_by_auth(self, *, auth: str, code: str, key: str, platformUid: int, site: str, uid: str) -> dict:
        """
        获取token
        :param auth: validate_auth_code返回的auth
        :param code: publicKey公钥
        :param key: privateKey私钥
        :param platformUid: club255 uid
        :param site: 平台名称
        :param uid: 平台uid
        :return: {code,token,uid}
        """
        return (await self.post(
            "auth/validate-login", auth=auth, code=code, key=key, platformUid=platformUid, site=site, uid=uid
        )).json()

    async def validate_auth_code(self, *, publicKey: str, privateKey: str) -> dict:
        """
        验证验证码
        :param publicKey: 公钥
        :param privateKey: 私钥
        :return: {code,auth,bind,msg,platformUid,site,uid}
        auth用于获取key
        bind: bool 平台的账号是否绑定club255
        msg: str 返回提示信息
        site: 平台名称
        platformUid: club25 uid
        """
        return (await self.post("auth/validate", code=publicKey, key=privateKey)).json()

    async def get_auth_code(self) -> dict:
        """
        直播间验证码，斗鱼和B站通用
        :return: {code,privateKey,publicKey}
        privateKey: 私钥
        publicKey: 公钥，发弹幕
        """
        return (await self.get("auth/code")).json()

    async def sign_now(self) -> dict:
        """
        签到
        :return: {code,exp,msg}
        code: 0 签到成功、104 已签到
        """
        return (await self.get("sign")).json()

    async def check_if_sign(self) -> bool:
        """
        检查是否已签到
        :return: bool
        """
        data = await self.get("sign/signed")
        return data.json()["signed"]

    async def like_post(self, pid: PID, uid: UID) -> dict:
        """
        点赞/取消点赞 帖子
        :param pid: 帖子id
        :param uid: 作者id
        :return: {exp,liked,msg}
        """
        return (
            await self.post(f"post/like/{pid}", author=int(uid))
        ).json()


def model_api(data: Any, model_type: Type[T], data_from: Optional[Union[str, Callable]] = None) -> Optional[T]:
    return parse_obj_as(
        model_type, (
            data[data_from] if isinstance(data_from, str) else data_from(data)
        ) if data_from else data
    )
