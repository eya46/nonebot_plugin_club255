from datetime import datetime
from typing import Optional
from base64 import b64decode
import pytz

from nonebot.utils import run_sync
from nonebot_plugin_datastore import get_plugin_data
from nonebot_plugin_datastore.db import post_db_init, get_engine
from sqlalchemy.ext.asyncio import AsyncConnection

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.ddl import CreateTable

from ..client import HeadlessClient, Api
from ..static import Model
from ..utils.time import get_timestamp, timestamp_to_datetime


class User(Model, HeadlessClient):
    __tablename__ = "club255_user"
    uid: Mapped[int] = mapped_column(primary_key=True)
    account: Mapped[Optional[str]]
    password: Mapped[Optional[str]]
    token: Mapped[Optional[str]]
    uuid: Mapped[str]

    async def get_api_client(self) -> Optional[Api]:
        return Api(self) if await self.login() else None


class File(Model):
    __tablename__ = "club255_file"
    url: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    query: Mapped[Optional[str]]
    size: Mapped[int]
    type: Mapped[str]
    file_type: Mapped[str]
    path: Mapped[str]

    timestamp: Mapped[int] = mapped_column(default_factory=get_timestamp)

    temp_data: Optional[bytes] = None

    @property
    def real_name(self) -> str:
        return f"{self.name}_{self.query}.{self.file_type}" if self.query else f"{self.name}.{self.file_type}"

    @property
    def real_query(self) -> str:
        return b64decode(self.query).decode()

    @property
    def create_time(self) -> datetime:
        return timestamp_to_datetime(self.timestamp)


@post_db_init
async def do_something():
    async with get_engine().begin() as conn:
        conn: AsyncConnection
        await conn.run_sync(Model.metadata.create_all)
