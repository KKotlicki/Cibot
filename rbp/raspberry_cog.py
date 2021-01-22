import discord
from discord.ext import commands, tasks
import os
from loguru import logger
from .rasp_config import *


class RaspberryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if temperature_limit is not None:
            self.raspberry_temp.start()

    @tasks.loop(minutes=5.0)
    async def raspberry_temp(self):
        if discord.Client.is_ready(self.bot):
            temp = os.popen("vcgencmd measure_temp").readline()
            if float(temp.replace("temp=", "").replace("'C", "")) > temperature_limit:
                logger.exception("Server overheated.")
                logger.add('dumps/errors.log', rotation="10 MB")
                exit()

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def temp(self, ctx):
        await ctx.send(os.popen("vcgencmd measure_temp").readline().replace("temp=", "").replace("'C", ""))


def setup(bot):
    bot.add_cog(RaspberryCog(bot))
