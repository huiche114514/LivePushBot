from nonebot import on_command, get_plugin_config
from pydantic import BaseModel

get_bot_info = on_command("关于", priority=10, block=True)
get_current_info = on_command("当前", priority=10, block=True)


class Config(BaseModel):
    uname: str = ""
    room_id: int = 0
    group_id: int = 0


config = get_plugin_config(Config)

UNAME = config.uname
ROOM_ID = config.room_id
GROUP_ID = config.group_id


@get_bot_info.handle()
async def command_bot_info():
    await get_bot_info.finish(
        "项目:\nbilibili主播开播推送\n\n"
        "简介:\n本项目会自动监听设定好的主播, 如果该主播开播后, 会自动向设定好的群组推送提醒\n\n"
        "开发:\n雪碧要兑七喜\n\n"
        "仓库:\nhttps://github.com/huiche114514/LivePushBot\n\n"
        "框架:\n本项目使用NoneBot2 + NapCat框架进行开发"
    )


@get_current_info.handle()
async def command_current_info():
    await get_current_info.finish(
        f"正在监听的主播:\n{UNAME}\n"
        f"正在监听的房间:\n{ROOM_ID}\n"
        f"当前设定的群组:\n{GROUP_ID}"
    )
