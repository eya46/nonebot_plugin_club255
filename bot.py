#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.console.adapter import Adapter as ConsoleAdapter
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ConsoleAdapter)
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_plugin("nonebot_plugin_club255")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
