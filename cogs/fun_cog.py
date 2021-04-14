import random
from discord.ext import commands
from config import *
from helpers import get_random_number_unless_specified, send_pic_or_txt_on_choice, read_lines


class Fun(commands.Cog):
    co_alias = read_lines(f'{RES_PATH}/co_aliases')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=co_alias)
    async def co(self, ctx, *, question=''):
        choice = get_random_number_unless_specified(question)
        await send_pic_or_txt_on_choice(ctx, choice)

    @commands.Cog.listener()
    async def on_message(self, message):
        if random.randint(1, 10) == 1 and not message.author.bot and not message.content.startswith(PREFIX):
            emoji_dict = {
                1: "👍",
                2: "❤",
                3: "🙂",
                4: "🤯",
                5: "👀",
                6: "🧠",
                7: "🫀",
                8: "🧐",
                9: "🥳",
                10: "😀",
                11: "😮",
                12: "🎓",
                13: "⭐",
                14: "☢",
                15: "☣",
                16: "🧡",
                17: "💛",
                18: "💚",
                19: "💙",
                20: "💜",
                21: "🖤",
                22: "🤍",
                23: "😃",
                24: "😄",
                25: "😲"
            }
            await message.add_reaction(emoji_dict[random.randint(1, 16)])


def setup(bot):
    bot.add_cog(Fun(bot))
