import discord
from discord.ext import commands
from helpers import fetch_sv_data
from loguru import logger
import os


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
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game('udaje studenta...'))

    @commands.Cog.listener()
    async def on_guild_join(self, ctx, guild):
        await fetch_sv_data(ctx, guild)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound):
            logger.exception("Invalid command used.")
            await ctx.send("Invalid command used.")
        else:
            logger.error(err)


def setup(bot):
    bot.add_cog(UtilityCog(bot))
