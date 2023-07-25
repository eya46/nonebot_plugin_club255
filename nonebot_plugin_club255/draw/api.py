import json
from datetime import datetime
from pathlib import Path
from typing import List, Any, Optional

import jinja2
from sqlalchemy import desc

from nonebot import require

from nonebot_plugin_htmlrender import html_to_pic

from ..config import config
from ..types import themes, Theme

dir_path = Path(__file__).parent
template_path = dir_path / "templates"
static_path = template_path / "static"
pic_path = static_path / "img"
bg_path = pic_path / "bg"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)

env.globals.update(static=lambda p: (static_path / p).as_uri())
env.globals.update(pic=lambda p: (pic_path / p).as_uri())
env.globals.update(bg=lambda p: (bg_path / {
    "white": "white.png",
    "dark": "dark.png",
    "2022": "2022.jpg",
    "2023": "2023.png"
}[p]).as_uri())

# ["white", "dark", "2022", "2023"]
env.globals.update(
    theme=lambda t: [themes.index(t)]
)


def get_color(theme: Theme) -> str:
    return {
        "white": "grey",
        "dark": "#88b7f6",
        "2022": "#ffb769",
        "2023": "#ffb769"
    }[theme]


def get_bg_color(theme: Theme) -> str:
    return {
        "white": "#ffb769",
        "dark": "#527fba",
        "2022": "#d93b44",
        "2023": "#d93b44"
    }[theme]


async def show_template(template_name: str, **kwargs) -> Optional[bytes]:
    template = env.get_template(template_name + ".html.jinja2")

    return await html_to_pic(await template.render_async(**kwargs), wait=0)


def get_theme() -> Theme:
    if globals().get("theme"):
        return globals()["theme"]
    return config.club255_theme


async def render_template(template_name: str, **kwargs) -> str:
    theme = get_theme()
    template = env.get_template(template_name + ".html.jinja2")
    data = {
        "theme": theme,
        "color": get_color(theme),
        "bg_color": get_bg_color(theme),
    }
    print(data)
    kwargs.update(data)
    return await template.render_async(**kwargs)
