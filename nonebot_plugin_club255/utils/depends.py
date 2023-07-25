from typing import Optional, Tuple, List, Set

from nonebot.internal.adapter import Message
from nonebot.internal.params import Depends
from nonebot.params import Command, CommandStart, CommandArg
from nonebot_plugin_datastore import get_session
from nonebot_plugin_userinfo import EventUserInfo, UserInfo
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from ..client import Api, HeadlessClient
from ..db.models import User
from .rule import _is_private_message

IsPrivateMessageGet = Annotated[bool, Depends(_is_private_message)]

CommandGet = Annotated[Tuple[str, ...], Command()]
CommandStartGet = Annotated[str, CommandStart()]
CommandArgGet = Annotated[Message, CommandArg()]

ClientUserGet = Annotated[UserInfo, EventUserInfo()]
SessionGet = Annotated[AsyncSession, Depends(get_session)]


async def _club_user(
        user: ClientUserGet,
        session: SessionGet
) -> Optional[User]:
    return await session.get(User, user.user_id)


ClubUserGet: Optional[User] = Annotated[Optional[User], Depends(_club_user)]


async def _club_api_headless(
        club_user: ClubUserGet
) -> Api:
    return Api(club_user or HeadlessClient())


async def _club_api(
        club_user: ClubUserGet,
        session: SessionGet,
) -> Optional[Api]:
    if club_user is None:
        return None
    if club_user.token:
        if await club_user.check_token():
            return Api(club_user)
    if club_user.login():
        # 更新token
        club_user.token = club_user.get_token_from_cookies()
        await session.commit()
        return Api(club_user)
    return None


ClubApiGet: Optional[Api] = Annotated[Optional[Api], Depends(_club_api)]
ClubApiHeadlessGet: Api = Annotated[Optional[Api], Depends(_club_api_headless)]
