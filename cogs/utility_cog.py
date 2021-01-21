import discord
from discord.ext import commands
from helpers import fetch_sv_data
from loguru import logger
import os


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_channel = ""

    @commands.Cog.listener(pass_context=True)
    async def on_ready(self, ctx):
        if os.path.exists("update.sh"):
            os.remove("update.sh")
        if os.path.exists("update.bat"):
            os.remove("update.bat")
        print(f"Logged in as {self.bot.user}")
        logger.info(f"Logged in as {self.bot.user}")
        await ctx.invoke(self.bot.rasp_temp())
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game('Infiltruje studentów...'))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await fetch_sv_data(guild)


def setup(bot):
    bot.add_cog(UtilityCog(bot))
