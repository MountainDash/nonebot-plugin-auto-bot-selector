# nonebot-plugin-auto-bot-selector

## 使用

```python
from nonebot import on_message
from nonebot.exception import ActionFailed
from nonebot_plugin_alconna.uniseg import Target, UniMessage
from nonebot_plugin_auto_bot_selector import get_bots
from nonebot_plugin_auto_bot_selector.expection import NoBotFoundError
from nonebot_plugin_auto_bot_selector.target import PlatformTarget, TargetQQGroup
from nonebot_plugin_auto_bot_selector.utils.alconna import create_target, extract_target

foo = on_message()


@foo.handle()
async def _recive_target(alc_target: Target):
    # 使用 alconna 提取目标
    abs_target = extract_target(alc_target)
    # 手动创建目标
    qq_group = TargetQQGroup(group_id=123456)
    # do something
    await foo.finish(f"用户 {abs_target} 已保存")


async def _send_msg_to_target(abs_target: PlatformTarget, msg: UniMessage):
    alc_target = create_target(abs_target)
    try:
        bots = get_bots(abs_target)
    except NoBotFoundError:
        return "没有可用的推送 Bot"

    for bot in get_bots(abs_target):
        try:
            await msg.send(target=alc_target, bot=bot)
            return "发送成功"
        except ActionFailed:
            # 发送失败
            continue
    else:
        return "全部推送 Bot 发送失败"
```
