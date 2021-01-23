import discord
from discord.ext import commands
from helpers import open_help
from config import res_dir, logs_dir
import json
from loguru import logger


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command()
    async def thx(self, ctx):
        embed_var = discord.Embed(title=":evergreen_tree: Contributed to Cibot:", description="https://github.com"
                                                                                              "/KKotlicki/Cibot",
                                  color=0xff770f)
        with open(f'{res_dir}/credits.json', 'r') as rd:
            link_dict = json.loads(rd.read())
        for name, cont in link_dict.items():
            embed_var.add_field(name=f'**{name}**', value=cont, inline=False)
        await ctx.send(embed=embed_var)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def help(self, ctx):
        await open_help(ctx, "help")

    @commands.command()
    async def bug(self, ctx, *, message):
        logger.info("\n<" + str(ctx.author) + "> said:\n<" + message + ">")
        logger.add(f'{logs_dir}/bugs.log', rotation="5 MB")


def setup(bot):
    bot.add_cog(MainCog(bot))
