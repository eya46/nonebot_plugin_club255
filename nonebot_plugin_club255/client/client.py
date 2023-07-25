from typing import Optional
from urllib.parse import urljoin
from uuid import uuid1

from httpx import AsyncClient, Response

from ..config import config


class HeadlessClient:
    root = "https://2550505.com/"

    @staticmethod
    def build_http_client(*args, **kwargs) -> AsyncClient:
        if headers := kwargs.get("headers"):
            headers["User-Agent"] = config.club255_ua
        else:
            kwargs["headers"] = {
                "User-Agent": config.club255_ua, "authorization": kwargs.get("uuid") or str(uuid1())
            }
        return AsyncClient(*args, **kwargs)

    def get_http_client(self, *args, **kwargs) -> AsyncClient:
        if http := getattr(self, "http", None):
            return http
        else:
            return self.build_http_client(*args, **kwargs)

    async def get(self, api: str, **kwargs) -> Response:
        http = self.get_http_client()
        resp = await http.get(urljoin(self.root, api), **kwargs)
        if resp.status_code == 403:
            raise Exception("你被ban了！")
        return resp

    async def post(self, api: str, **kwargs) -> Response:
        http = self.get_http_client()
        resp = await http.post(urljoin(self.root, api), **kwargs)
        if resp.status_code == 403:
            raise Exception("你被ban了！")
        return resp

    async def check_token(self, *, token: Optional[str] = None) -> bool:
        token = token or getattr(self, "token", None) or self.get_token_from_cookies()
        resp = await self.get(
            urljoin(self.root, "sign/signed"), cookies={"token": token}
        )
        if resp.status_code != 200:
            return False
        try:
            return resp.json()["code"] == 0
        except:
            return False

    def get_token_from_cookies(self) -> Optional[str]:
        return self.get_http_client().cookies.get("token")

    async def get_token(
            self, *, token: Optional[str] = None, account: Optional[str] = None, password: Optional[str] = None,
            if_check_token: bool = True
    ) -> Optional[str]:
        token = token or getattr(self, "token", None) or self.get_token_from_cookies()
        account = account or getattr(self, "account")
        password = password or getattr(self, "password")

        if token and if_check_token:
            if await self.check_token(token=token):
                return token
        if account and password:
            data = (await self.post(
                urljoin(self.root, "auth/login"), json={
                    "account": account, "password": password
                }
            )).json()
            if data["code"] == 0:
                return data["token"]
            else:
                return None

    async def login(
            self, *, token: Optional[str] = None, account: Optional[str] = None, password: Optional[str] = None
            , if_check_token: bool = True
    ) -> bool:
        http = self.get_http_client()
        token = await self.get_token(
            token=token, account=account, password=password, if_check_token=if_check_token
        )

        if token:
            http.cookies.set("token", token, domain="2550505.com")
            return True
        else:
            return False
