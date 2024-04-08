import random
from typing import List

import nonebot
from nonebot import logger
from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata

from . import adapters  # noqa: F401
from .expection import NoBotFoundError
from .registries import BOT_CACHE, BOT_CACHE_LOCK, info_current, refresh_bot
from .target import PlatformTarget

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

try:
    __version__ = version("nonebot_plugin_auto_bot_selector")
except Exception:
    __version__ = None

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-auto-bot-selector",
    description="自动Bot选择器，消息推送好帮手",
    usage="如果你需要主动发送消息，那么这款插件将会免去你找不到合适推送 Bot 的烦恼",
    homepage="https://github.com/MountainDash/nonebot-plugin-auto-bot-selector",
    type="library",
    supported_adapters={
        "~onebot.v11",
        "~onebot.v12",
        "~qq",
        "~kaiheila",
        "~red",
        "~dodo",
        "~satori",
    },
    extra={
        "author": "Well404",
        "version": __version__,
    },
)

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
