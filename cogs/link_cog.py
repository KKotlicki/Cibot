import discord
from discord.ext import commands
from config import *
import json
from helpers import build_link_list, read_lines


class LinkShare(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def linki(self, ctx):
        embed_var = discord.Embed(title=":shushing_face: Linki pochodzą z:", description="https://tiny.cc/szukamlinku",
                                  color=0xff770f)
        await build_link_list(ctx, embed_var, "linki")

    @commands.command()
    async def oflinki(self, ctx):
        embed_var = discord.Embed(title=":mortar_board: Oficjalne linki:", color=0xff770f)
        await build_link_list(ctx, embed_var, "oflinki")

    @commands.command()
    async def link(self, ctx, *, subject):
        help_json = "".join(read_lines(f'{res_dir}/linki'))
        embed_var = discord.Embed(title=subject, description=json.loads('{' + help_json + '}')[subject], color=0xff770f)
        await ctx.send(embed=embed_var)


def setup(client):
    client.add_cog(LinkShare(client))
