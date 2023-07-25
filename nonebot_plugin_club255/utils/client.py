from httpx import AsyncClient
from ..config import config

client = AsyncClient(headers={"User-Agent": config.club255_ua})
