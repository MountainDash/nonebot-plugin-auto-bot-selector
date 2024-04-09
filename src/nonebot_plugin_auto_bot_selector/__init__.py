from nonebot.plugin import PluginMetadata

from importlib.metadata import version

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

from .compat import get_bot, get_bots, NoBotFoundError
from .target import (
    PlatformTarget,
    TargetDoDoChannel,
    TargetDoDoPrivate,
    TargetKaiheilaChannel,
    TargetKaiheilaPrivate,
    TargetOB12Unknow,
    TargetQQGroup,
    TargetQQGuildChannel,
    TargetQQGuildDirect,
    TargetQQPrivate,
)

__all__ = [
    "get_bot",
    "get_bots",
    "NoBotFoundError",
    "PlatformTarget",
    "TargetDoDoChannel",
    "TargetDoDoPrivate",
    "TargetKaiheilaChannel",
    "TargetKaiheilaPrivate",
    "TargetOB12Unknow",
    "TargetQQGroup",
    "TargetQQGuildChannel",
    "TargetQQGuildDirect",
    "TargetQQPrivate",
]
