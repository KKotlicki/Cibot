from discord.ext import commands
from config import *
from helpers import get_random_number_unless_specified, send_pic_or_txt_on_choice, read_lines


class Fun(commands.Cog):
    co_alias = read_lines(f'{res_dir}/co_aliases')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=co_alias)
    async def co(self, ctx, *, question=''):
        choice = get_random_number_unless_specified(question)
        await send_pic_or_txt_on_choice(ctx, choice)


def setup(bot):
    bot.add_cog(Fun(bot))
