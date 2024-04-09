from random import random
from typing import Dict, List, Set, cast
from nonebot import require, get_driver, get_bots as nonebot_get_bots, logger
from nonebot.adapters import Bot

from .registries import PlatformTarget

try:
    require("nonebot_plugin_saa")
except ImportError:
    USE_SAA = False
else:
    USE_SAA = True

if USE_SAA:
    from nonebot_plugin_saa.auto_select_bot import (
        enable_auto_select_bot,
        BOT_CACHE as BOT_CACHE,
        _info_current as info_current,
        NoBotFound as NoBotFoundError,
        refresh_bots as refresh_bots,
    )

    enable_auto_select_bot()
else:
    from .registries import BOT_CACHE as BOT_CACHE, BOT_CACHE_LOCK, info_current, refresh_bot, hook_register
    from .expection import NoBotFoundError

    hook_register()

    driver = get_driver()

    async def refresh_bots():
        """刷新缓存的 Bot 数据"""
        logger.debug("start refresh bot cache")
        async with BOT_CACHE_LOCK:
            BOT_CACHE.clear()
            for bot in list(nonebot_get_bots().values()):
                await refresh_bot(bot)
        logger.debug("refresh bot cache complete")

BOT_CACHE = cast(Dict[Bot, Set[PlatformTarget]], BOT_CACHE)

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
