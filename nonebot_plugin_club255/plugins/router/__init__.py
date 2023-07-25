from pathlib import Path
from typing import Union

from fastapi import FastAPI
from nonebot import get_app, load_plugins


def load(name: Union[str, Path]):
    return load_plugins(
        str(Path(__file__).parent.joinpath(name).resolve())
    )


load("api")
load("view")

from .app import APP
from ...static import PLUGIN_NAME

app: FastAPI = get_app()
app.mount(f"/{PLUGIN_NAME}", APP)
