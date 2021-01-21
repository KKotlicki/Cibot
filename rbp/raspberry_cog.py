import discord
from discord.ext import commands
from helpers import fetch_sv_data, open_help
from config import *
import json
from loguru import logger
import os


class RaspberryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("f")

    # @commands.Cog.listener()
    # async def on_ready(self):
    #
    #
    # @commands.Cog.listener()
    # async def on_guild_join(self, guild):
    #     await fetch_sv_data(guild)


def setup(bot):
    bot.add_cog(RaspberryCog(bot))
