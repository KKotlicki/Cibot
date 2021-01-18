import discord
from discord.ext import commands
from config import *
import json
from helpers import read_lines, build_link_list


class MainCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    @commands.command()
    async def thx(self, ctx):
        embed_var = discord.Embed(title=":evergreen_tree: Contributed to Cibot:", description="https://github.com/KKotlicki/Cibot",
                                  color=0xff770f)
        await build_link_list(ctx, embed_var, "credits")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.client.latency * 1000)}ms')

    @commands.command()
    async def help(self, ctx):
        embed_var = discord.Embed(title=":ledger: Komendy:", color=0xff770f)
        help_json = "".join(read_lines(f'{res_dir}/help'))
        for name, value in json.loads('{' + help_json + '}').items():
            embed_var.add_field(name=f'**{name}**', value=f'```{prefix}{value}```', inline=False)
        await ctx.send(embed=embed_var)


def setup(client):
    client.add_cog(MainCog(client))
