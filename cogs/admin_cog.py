import discord
from discord.ext import commands
from helpers import fetch_sv_data, open_help
from config import sv_dir
import json


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_channel = ""
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await fetch_sv_data(guild)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def adm(self, ctx):
        await open_help(ctx, "adm_help")
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def shutdown(self):
        await self.bot.close()

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def sv(self, ctx):
        guild = ctx.message.guild
        await fetch_sv_data(guild)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_anns(self, ctx, *, message=''):
        with open(f'{sv_dir}/{ctx.message.guild.name}_config.txt', 'w+') as wr:
            wr.write(message)
        await ctx.send(f"channel set to {message}")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, message):
        sv_text_channel_dict = {}
        keys = []
        values = []
        with open(f'{sv_dir}/{ctx.message.guild.name}_config.txt', "r") as rd:
            self.message_channel = rd.read()
        with open(f"{sv_dir}/{ctx.message.guild.name}.json", "r") as rd:
            sv_data = json.loads(rd.read())["text"]
        for elem in sv_data:
            keys.append(elem.split(" => ")[0])
            values.append(elem.split(" => ")[1])
        for x in range(0, len(keys)):
            sv_text_channel_dict[keys[x]] = values[x]
        channel = self.bot.get_channel(int(sv_text_channel_dict[self.message_channel]))
        embed_var = discord.Embed(title=f"{message}", color=0x00ff00)
        await channel.send(embed=embed_var)


def setup(bot):
    bot.add_cog(AdminCog(bot))
