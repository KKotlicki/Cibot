import discord
from discord.ext import commands, tasks
import os
from config import LOGS_PATH
from loguru import logger
from .rasp_config import *


class RaspberryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if TEMPERATURE_LIMIT:
            self.raspberry_temp_check.start()

    @tasks.loop(minutes=5.0)
    async def raspberry_temp_check(self):
        if discord.Client.is_ready(self.bot):
            temp = os.popen("vcgencmd measure_temp").readline()
            if float(temp.replace("temp=", "").replace("'C", "")) > TEMPERATURE_LIMIT:
                logger.error("Server overheated.")
                logger.add(f'{LOGS_PATH}/errors.log', rotation="10 MB")
                await self.bot.close()

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def temp(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send(os.popen("vcgencmd measure_temp").readline().replace("temp=", ""))


def setup(bot):
    bot.add_cog(RaspberryCog(bot))
