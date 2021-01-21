import discord
import json
from discord.ext import commands
from helpers import build_link_list
from config import res_dir


class LinkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def linki(self, ctx, message="all"):
        embed_var = discord.Embed(title=":shushing_face: Nieoficjalne linki:", description="semestr "+message,
                                  color=0xff770f)
        await build_link_list(ctx, embed_var, "linki", message)

    @commands.command()
    async def oflinki(self, ctx, message="all"):
        embed_var = discord.Embed(title=":mortar_board: Oficjalne linki:", color=0xff770f)
        await build_link_list(ctx, embed_var, "oflinki", message)

    @commands.command()
    async def link(self, ctx, sem, message):
        with open(f"{res_dir}/subject_aliases.txt", "r") as rd:
            subject_alias_dict = json.loads(rd.read())[sem]
        for key in subject_alias_dict:
            if message in subject_alias_dict[key] or message == key:
                subject = key
                break
        print(subject_alias_dict[sem][subject])
        embed_var = discord.Embed(title=subject, description=subject_alias_dict[sem][subject], color=0xff770f)
        await ctx.send(embed=embed_var)


def setup(bot):
    bot.add_cog(LinkCog(bot))
