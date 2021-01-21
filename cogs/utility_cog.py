import discord
from discord.ext import commands, tasks
from helpers import fetch_sv_data
from loguru import logger
import os
from urllib.request import urlopen
from urllib.error import URLError


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_channel = ""

    @commands.Cog.listener()
    async def on_ready(self):
        if os.path.exists("update.sh"):
            os.remove("update.sh")
        if os.path.exists("update.bat"):
            os.remove("update.bat")
        print(f"Logged in as {self.bot.user}")
        logger.info(f"Logged in as {self.bot.user}")
        if not os.path.exists('dumps/errors.log'):
            logger.add('dumps/errors.log', rotation="10 MB")
        # self.check_discord_connection.start()
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game('infiltruje discorda'))

    @commands.Cog.listener()
    async def on_guild_join(self, ctx, guild):
        await fetch_sv_data(ctx, guild)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound):
            logger.exception("Invalid command used.")
            logger.add('dumps/errors.log', rotation="10 MB")
            await ctx.send("Niepoprawna komenda.")
        else:
            logger.error(err)

    # @tasks.loop(minutes=1.0)
    # async def check_discord_connection(self):
    #     try:
    #         urlopen('http://216.58.192.142', timeout=20)
    #     except URLError:
    #         logger.exception("Disconnected")
    #         logger.add('dumps/errors.log', rotation="10 MB")
    #         await self.bot.close()


def setup(bot):
    bot.add_cog(UtilityCog(bot))
