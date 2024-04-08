from nonebot_plugin_alconna.uniseg import SupportScope, Target

from ..target import (
    PlatformTarget,
    TargetDoDoChannel,
    TargetDoDoPrivate,
    TargetKaiheilaChannel,
    TargetKaiheilaPrivate,
    TargetQQGroup,
    TargetQQGuildChannel,
    TargetQQGuildDirect,
    TargetQQPrivate,
)


def extract_target(target: Target) -> PlatformTarget:
    if not target.scope:
        raise ValueError("target does not have scope")
    # QQ UnOfficial
    if target.scope == SupportScope.qq_client:
        if target.private:
            return TargetQQPrivate(user_id=int(target.id))
        else:
            return TargetQQGroup(group_id=int(target.id))
    # QQ Official
    elif target.scope == SupportScope.qq_api:
        if target.private:
            return TargetQQGuildDirect(
                recipient_id=int(target.id), source_guild_id=int(target.parent_id)
            )
        else:
            return TargetQQGuildChannel(channel_id=int(target.id))
    # DODO
    elif target.scope == SupportScope.dodo:
        if target.private:
            return TargetDoDoPrivate(
                island_source_id=target.parent_id, dodo_source_id=target.id
            )
        else:
            return TargetDoDoChannel(
                channel_id=target.id, dodo_source_id=target.parent_id
            )
    # KOOK
    elif target.scope == SupportScope.kook:
        if target.private:
            return TargetKaiheilaPrivate(user_id=target.id)
        else:
            return TargetKaiheilaChannel(channel_id=target.id)
    # Other
    else:
        raise NotImplementedError(f"Unsupported target type {target.scope}")


def create_target(t: PlatformTarget) -> Target:
    # QQ UnOfficial
    if isinstance(t, TargetQQGroup):
        return Target(id=str(t.group_id), scope=SupportScope.qq_client, private=False)
    elif isinstance(t, TargetQQPrivate):
        return Target(id=str(t.user_id), scope=SupportScope.qq_client, private=True)
    # QQ Official
    elif isinstance(t, TargetQQGuildChannel):
        return Target(id=str(t.channel_id), scope=SupportScope.qq_guild, private=False)
    elif isinstance(t, TargetQQGuildDirect):
        return Target(
            id=str(t.recipient_id),
            scope=SupportScope.qq_guild,
            private=True,
            parent_id=str(t.source_guild_id),
        )
    # DODO
    elif isinstance(t, TargetDoDoChannel):
        return Target(id=str(t.channel_id), scope=SupportScope.dodo, private=False)
    elif isinstance(t, TargetDoDoPrivate):
        return Target(
            id=str(t.dodo_source_id),
            scope=SupportScope.dodo,
            private=True,
            parent_id=str(t.island_source_id),
        )
    # KOOK
    elif isinstance(t, TargetKaiheilaChannel):
        return Target(id=str(t.channel_id), scope=SupportScope.kook, private=False)
    elif isinstance(t, TargetKaiheilaPrivate):
        return Target(id=str(t.user_id), scope=SupportScope.kook, private=True)
    # Other
    else:
        raise NotImplementedError("Unsupported platform type")
