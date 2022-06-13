from io import BytesIO
from typing import Union
from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot import on_command, on_message, require
from nonebot.adapters.onebot.v11 import MessageSegment
from configs.path_config import DATA_PATH

require("nonebot_plugin_imageutils")

from .depends import regex
from .data_source import memes
from .utils import Meme, help_image

__zx_plugin_name__ = "表情包制作"
__plugin_usage__ = """
usage：
    触发方式：指令 +文字(表情包内有几段文字就加几段中间加空格)
    发送“表情包制作”查看表情包列表
    示例：
        举牌 大佬带带我
        王境泽.gif 我就是饿死 死外边，从这里跳下去 不会吃你们一点东西 真香
""".strip()
__plugin_des__ = "生成各种表情包"
__plugin_type__ = ("群内小游戏",)
__plugin_cmd__ = ["表情包制作", ]
__plugin_version__ = 0.1
__plugin_author__ = "yajiwa"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    'cmd': __plugin_cmd__
}
__plugin_resources__ = {
    "resources": DATA_PATH / "zhenxun_plugin_memes", }

help_cmd = on_command("表情包制作", block=True, priority=5)


@help_cmd.handle()
async def _():
    img = await help_image(memes)
    if img:
        await help_cmd.finish(MessageSegment.image(img))


def create_matchers():
    def handler(meme: Meme) -> T_Handler:
        async def handle(
                matcher: Matcher, res: Union[str, BytesIO] = Depends(meme.func)
        ):
            matcher.stop_propagation()
            if isinstance(res, str):
                await matcher.finish(res)
            await matcher.finish(MessageSegment.image(res))

        return handle

    for meme in memes:
        on_message(
            regex(meme.pattern),
            block=True,
            priority=5,
        ).append_handler(handler(meme))


create_matchers()
