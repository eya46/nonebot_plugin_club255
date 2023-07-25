from base64 import b64encode
from os.path import basename
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

from aiofiles import open
from httpx import AsyncClient
from nonebot import logger
from sqlalchemy.ext.asyncio import AsyncSession

from ..client import client as base_client
from ...db.models import File
from ...static import CachePath
from ...types import URL


def build_file_name(name: str, type_: str, query: str) -> str:
    """
    构建文件名,对应File.real_name生成规则
    :param name: 文件名
    :param type_: 文件类型
    :param query: 查询参数(要base64编码后的)
    """
    return f"{name}_{query}.{type_}" if query else f"{name}.{type_}"


def get_url_name_type_query(url: URL) -> Tuple[str, str, str]:
    """
    从URL中获取文件名、文件类型和查询参数
    :return: 文件名、文件类型、查询参数(b64)
    """
    url = urlparse(url) if isinstance(url, str) else url
    split = basename(url.path).split('.')
    name = ".".join(split[:-1])
    type_ = split[-1]
    return name, type_, b64encode(url.query.encode()).decode()


async def down_load_file(url: URL, client: Optional[AsyncClient] = None) -> bytes:
    url = urlparse(url) if isinstance(url, str) else url
    client = client or base_client
    return (await client.get(url)).content


async def load_file(*, session: AsyncSession, url: str) -> Optional[File]:
    # 没有本地缓存
    if file := await session.get(File, str(url)):
        return None
    # 有本地缓存
    try:
        async with open(CachePath / file.path, 'rb') as f:
            file.temp_data = await f.read()
    except Exception as e:
        logger.error(f"读取文件失败({file.path}): {e}")
    return file


async def save_file(
        *, url: URL, _type: str, type_: str, query: str, name: str, client: Optional[AsyncClient] = None
) -> Tuple[bytes, Path]:
    """
    下载和保存文件
    name_query.type_ / name.type_
    :param url: url
    :param _type: avatar, picture, face...
    :param type_: png, jpg, gif...
    :param query: query
    :param name: name
    :param client: client
    :return 文件数据, 子路径
    """
    client = client or base_client
    data = await down_load_file(url, client=client)
    _child_path = Path(_type) / build_file_name(name, type_, query)
    async with open(CachePath / _child_path, 'wb') as f:
        await f.write(data)
    return data, _child_path


async def add_file(
        *, session: AsyncSession, url: str, name: str, _type: str, type_: str, query: str, size: int, path: str
) -> File:
    """
    添加进数据库
    """
    file = File(url=url, name=name, type=_type, file_type=type_, info=query, size=size, path=path)
    session.add(file)
    await session.commit()
    return file


async def resolve_url(*, session: AsyncSession, client: AsyncClient, url: URL, _type: str) -> File:
    file = await load_file(session=session, url=url)
    if file:
        if file.temp_data:
            return file
        else:
            # 加载失败,删除记录,管它啥原因
            await session.delete(file)
    name, type_, query = get_url_name_type_query(url)
    data, child_path = await save_file(url=url, _type=_type, name=name, client=client, type_=type_, query=query)
    file = await add_file(
        session=session, url=str(url), name=name, _type=_type, type_=type_,
        query=query, size=len(data), path=str(child_path)
    )
    file.temp_data = data
    return file


async def resolve_avatar(session: AsyncSession, url: URL, client: Optional[AsyncClient] = None) -> File:
    """
    处理头像
    """
    return await resolve_url(
        session=session, client=client or base_client, url=url, _type='avatar'
    )


async def resolve_picture(session: AsyncSession, url: URL, client: Optional[AsyncClient] = None) -> File:
    """
    处理图片（帖子中的图片）
    """
    return await resolve_url(
        session=session, client=client or base_client, url=url, _type='picture'
    )


async def resolve_face(session: AsyncSession, url: URL, client: Optional[AsyncClient] = None) -> File:
    """
    处理表情
    """
    return await resolve_url(
        session=session, client=client or base_client, url=url, _type='face'
    )
