import discord
from discord.ext import commands
from config import *
import json
from helpers import build_link_list, read_lines


class LinkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    async def link(self, ctx, *, subject_alias):
        subject = ""
        with open(f"{res_dir}/subject_aliases.txt", "r") as rd:
            subject_alias_dict = json.loads('{' + rd.read() + '}')
        print(subject_alias_dict)
        print(subject_alias)
        for key in subject_alias_dict:
            if subject_alias in subject_alias_dict[key] or subject_alias == key:
                subject = key
                break
        print(subject)
        help_json = "".join(read_lines(f'{res_dir}/linki'))
        print(help_json)
        embed_var = discord.Embed(title=subject, description=json.loads('{' + help_json + '}')[subject], color=0xff770f)
        await ctx.send(embed=embed_var)


def setup(bot):
    bot.add_cog(LinkCog(bot))
