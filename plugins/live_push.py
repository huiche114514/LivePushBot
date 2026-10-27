import httpx
from nonebot import on_command, require, get_bot, get_plugin_config
from pydantic import BaseModel

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

live_push = on_command("查询", priority=10, block=True)


class Config(BaseModel):
    uname: str = ""
    room_id: int = 0
    group_id: int = 0


config = get_plugin_config(Config)

UNAME = config.uname
ROOM_ID = config.room_id
GROUP_ID = config.group_id
CHECK_INTERVAL_SECONDS = 30

last_status = None


async def get_live_info():
    url = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={ROOM_ID}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://live.bilibili.com/{ROOM_ID}",
    }

    async with httpx.AsyncClient(headers=headers) as client:
        resp = await client.get(url, timeout=10)
        data = resp.json()

    info = data.get("data", {})
    return {
        "status": info.get("live_status"),
        "title": info.get("title"),
    }


def build_message(state: dict) -> str:
    status = state["status"]
    title = state["title"]

    if status == 1:
        return (
            f"{UNAME}\n\n"
            f"状态:\n正在直播中\n"
            f"标题:\n{title}\n"
            f"房间:\nhttps://live.bilibili.com/{ROOM_ID}"
        )
    elif status == 2:
        return f"{UNAME}\n\n状态:\n正在轮播中\n标题:\n{title}"
    else:
        return f"{UNAME}\n\n状态:\n当前未开播"


@live_push.handle()
async def command_send_message():
    state = await get_live_info()
    await live_push.finish(build_message(state))


@scheduler.scheduled_job("interval", seconds=CHECK_INTERVAL_SECONDS)
async def auto_send_message():
    global last_status
    state = await get_live_info()
    status = state["status"]
    if status == 1 and last_status != 1:
        bot = get_bot()
        await bot.send_group_msg(group_id=GROUP_ID, message=build_message(state))
    last_status = status
