import discord
from discord.ext import commands
from helpers import fetch_sv_data
import os


class AdminCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await fetch_sv_data(guild)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def sv(self, ctx):
        guild = ctx.message.guild
        await fetch_sv_data(guild)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def say(self, *, message):
        channel = self.client.get_channel(int(1))
        embed_var = discord.Embed(title=f"{message}", color=0x00ff00)
        await channel.send(embed=embed_var)


def setup(client):
    client.add_cog(AdminCog(client))
