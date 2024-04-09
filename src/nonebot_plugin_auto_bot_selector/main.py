import random
from typing import List

import nonebot
from nonebot.adapters import Bot

try:
    from nonebot import require

    require("nonebot_plugin_saa")

    from nonebot_plugin_saa.auto_select_bot import (  # noqa: E402
        BOT_CACHE,
        PlatformTarget,
        enable_auto_select_bot,
    )
    from nonebot_plugin_saa.auto_select_bot import (  # noqa: E402
        NoBotFound as NoBotFoundError,
    )
    from nonebot_plugin_saa.auto_select_bot import (  # noqa: E402
        _info_current as info_current,
    )

    enable_auto_select_bot()

    def get_bot(target: PlatformTarget) -> Bot:
        """获取 Bot"""
        return random.choice(get_bots(target=target))

    def get_bots(target: PlatformTarget) -> List[Bot]:
        """获取 Bot 列表"""
        bots = []
        for bot, targets in BOT_CACHE.items():
            if target in targets:
                bots.append(bot)
        if not bots:
            info_current()
            raise NoBotFoundError(target)
        return bots

except ImportError:
    from nonebot import logger

    from . import adapters  # noqa: F401
    from .expection import NoBotFoundError
    from .registries import BOT_CACHE, BOT_CACHE_LOCK, info_current, refresh_bot
    from .target import PlatformTarget

    driver = nonebot.get_driver()

    @driver.on_bot_connect
    async def _(bot: Bot):
        logger.info(f"refresh platform target cache of {bot}")
        async with BOT_CACHE_LOCK:
            await refresh_bot(bot)

    @driver.on_bot_disconnect
    async def _(bot: Bot):
        logger.info(f"pop bot {bot}")
        async with BOT_CACHE_LOCK:
            BOT_CACHE.pop(bot, None)

    async def refresh_bots():
        """刷新缓存的 Bot 数据"""
        logger.debug("start refresh bot cache")
        async with BOT_CACHE_LOCK:
            BOT_CACHE.clear()
            for bot in list(nonebot.get_bots().values()):
                await refresh_bot(bot)
        logger.debug("refresh bot cache complete")

    def get_bot(target: PlatformTarget) -> Bot:
        """获取 Bot"""
        return random.choice(get_bots(target=target))

    def get_bots(target: PlatformTarget) -> List[Bot]:
        """获取 Bot 列表"""
        bots = []
        for bot, targets in BOT_CACHE.items():
            if target in targets:
                bots.append(bot)
        if not bots:
            info_current()
            raise NoBotFoundError(target)
        return bots