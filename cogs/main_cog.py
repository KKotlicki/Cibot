import discord
from discord.ext import commands
from helpers import open_help
from config import RES_PATH, LOGS_PATH
import json
from loguru import logger


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def thx(self, ctx):
        embed_var = discord.Embed(title="🌲 Contributed to Cibot:", description="https://github.com/KKotlicki/Cibot",
                                  color=0xff770f)
        with open(f'{RES_PATH}/credits.json', encoding='utf-8') as rd:
            link_dict = json.loads(rd.read())
        for name, cont in link_dict.items():
            embed_var.add_field(name=f'**{name}**', value=cont, inline=False)
        await ctx.send(embed=embed_var)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def help(self, ctx):
        await ctx.channel.purge(limit=1)
        await open_help(ctx, "help")

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def bug(self, ctx, *, message):
        await ctx.channel.purge(limit=1)
        logger.success("\n<" + str(ctx.author) + "> said:\n<" + message + ">")
        logger.add(f'{LOGS_PATH}/bugs.log', rotation="5 MB")


def setup(bot):
    bot.add_cog(MainCog(bot))
